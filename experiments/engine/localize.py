"""LOCALIZE: when a candidate breaks, measure WHERE, not just THAT.

FALSIFY returns a verdict: does a candidate relation hold across the database or
not. That binary throws away the most useful information. A relation that holds
on every rank-0 and rank-1 curve and breaks only at rank 2 has not merely failed;
it has pointed at the rank-1 -> rank-2 cliff, which is the Detector-1 signature of
a property that belongs to the one-point proven regime rather than to BSD. A
relation that breaks at one bad prime has pointed at a missing local condition.
LOCALIZE is the operator that reads those pointers.

It works on a residual rather than a boolean. A residual is 0 when the candidate
holds exactly and grows with the distance from holding, so a near miss is a
gradient instead of a flat False. Over the bundled curve ladder (ranks 0/1/2/3)
LOCALIZE produces two heat-maps:

  curve x rank   -- one residual per curve, grouped by rank, with the smallest
                    rank at which the candidate first breaks (the break-rank) and
                    an automatic diagnosis: cliff, proven-regime break, or survivor.
  curve x prime  -- for a candidate with per-prime structure, a grid of residuals
                    over small primes, isolating the primes that carry the heat
                    (e.g. the primes of bad reduction).

LOCALIZE proves nothing. It turns a failed FALSIFY into a diagnosis that feeds the
next PROPOSE: the heat-map says which regime or which prime the next candidate has
to handle. It is the FALSIFY/LOCALIZE half of the engine loop made mechanical,
built on the same bundled invariants the miner uses, fully offline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isqrt
from typing import Callable, Dict, List, Optional

from experiments._shared import all_curves, get_curve

from .mine import Relation


# --------------------------------------------------------------------------
# A candidate: a residual over a curve (0 = holds), plus optional prime structure.
# --------------------------------------------------------------------------

@dataclass
class Candidate:
    """A relation expressed as a residual so near misses are visible.

    residual(E) returns 0.0 when the candidate holds exactly on E, a positive
    magnitude measuring how far it is from holding, or None when the candidate
    does not apply to E. A curve counts as HOLDING when its residual is <= tol.

    prime_residual(E, p), when supplied, gives a per-prime residual so LOCALIZE
    can build the curve x prime heat-map; primes is the column set to scan.
    """

    name: str
    description: str
    residual: Callable[[object], Optional[float]]
    tol: float = 1e-9
    prime_residual: Optional[Callable[[object, int], Optional[float]]] = None
    primes: Optional[List[int]] = None


def from_relation(rel: Relation, tol: float = 0.5) -> Candidate:
    """Adapt a boolean mine.Relation into a coarse 0/1 Candidate.

    True -> residual 0.0 (holds), False -> 1.0 (breaks), None -> None. The
    gradient is lost (a boolean carries none), but the rank-cut localization and
    the break-rank diagnosis still work, so every relation in the miner's library
    can be localized for free.
    """
    def residual(E) -> Optional[float]:
        v = rel.predicate(E)
        if v is None:
            return None
        return 0.0 if v else 1.0

    return Candidate(rel.name, rel.description, residual, tol=tol)


# --------------------------------------------------------------------------
# Heat glyphs. Absolute bands chosen for residuals of order 0.01 to 1.
# --------------------------------------------------------------------------

_LEGEND = "legend:  ' '=N/A   .=holds(<=tol)   :<0.05   +<0.2   *<1.0   #>=1.0"


def _glyph(res: Optional[float], tol: float) -> str:
    if res is None:
        return " "
    if res <= tol:
        return "."
    if res < 0.05:
        return ":"
    if res < 0.2:
        return "+"
    if res < 1.0:
        return "*"
    return "#"


# --------------------------------------------------------------------------
# curve x rank localization.
# --------------------------------------------------------------------------

@dataclass
class CurveResidual:
    label: str
    rank: Optional[int]
    residual: Optional[float]
    holds: Optional[bool]


@dataclass
class LocalizeResult:
    candidate: str
    description: str
    per_curve: List[CurveResidual]
    by_rank: Dict[int, dict]
    break_rank: Optional[int]
    diagnosis: str


def localize(candidate: Candidate, curves=None) -> LocalizeResult:
    """Localize where a candidate breaks across the rank ladder.

    Computes a residual per curve, aggregates by rank, finds the smallest rank at
    which the candidate first breaks (the break-rank), and diagnoses the pattern:

      cliff               -- holds through rank <= 1, first breaks at rank >= 2.
                             The proven-regime ceiling caught in the act.
      proven-regime break -- breaks at rank <= 1, where BSD is a theorem; suspect
                             the candidate or the data, not the open regime.
      survivor            -- never breaks; a necessary condition, not a proof.
    """
    if curves is None:
        curves = all_curves()

    per_curve: List[CurveResidual] = []
    for E in curves:
        res = candidate.residual(E)
        holds = None if res is None else (res <= candidate.tol)
        per_curve.append(CurveResidual(E.label, E.rank, res, holds))

    by_rank: Dict[int, dict] = {}
    for cr in per_curve:
        if cr.rank is None or cr.residual is None:
            continue
        bucket = by_rank.setdefault(
            cr.rank,
            {"n": 0, "n_hold": 0, "max_residual": 0.0, "holds_all": True},
        )
        bucket["n"] += 1
        if cr.holds:
            bucket["n_hold"] += 1
        else:
            bucket["holds_all"] = False
        bucket["max_residual"] = max(bucket["max_residual"], cr.residual)

    broken_ranks = [r for r, b in by_rank.items() if not b["holds_all"]]
    break_rank = min(broken_ranks) if broken_ranks else None

    diagnosis = _diagnose(candidate, by_rank, break_rank)
    return LocalizeResult(
        candidate.name, candidate.description, per_curve, by_rank, break_rank, diagnosis
    )


def _diagnose(candidate: Candidate, by_rank: Dict[int, dict],
              break_rank: Optional[int]) -> str:
    if not by_rank:
        return "NO DATA: the candidate did not apply to any curve."
    if break_rank is None:
        return (
            "NO BREAK LOCALIZED: residual within tolerance on every curve, all "
            "ranks. Survivor (a necessary condition, not a rank >= 2 proof)."
        )
    if break_rank <= 1:
        return (
            f"BREAKS INSIDE THE PROVEN REGIME (first at rank {break_rank}, where "
            "BSD is a theorem). Not a rank-cliff phenomenon: the candidate is "
            "false where the answer is known, so suspect the candidate or the data."
        )
    # break_rank >= 2 and, by minimality, every rank <= 1 present held.
    gradient = ", ".join(
        f"rank {r}: max {by_rank[r]['max_residual']:.4f}"
        for r in sorted(by_rank)
    )
    return (
        f"LOCALIZED AT THE CLIFF: holds through the proven regime (rank <= 1) and "
        f"first breaks at rank {break_rank}. This is the Detector-1 signature, a "
        f"property of the one-point proven regime and not of BSD in the open "
        f"regime. Residual gradient [{gradient}]."
    )


def render(result: LocalizeResult) -> str:
    """A curve x rank heat-map: residual and glyph per curve, then the diagnosis."""
    lines: List[str] = []
    lines.append(f"LOCALIZE  {result.candidate}")
    lines.append(f"  {result.description}")
    lines.append("  " + _LEGEND)
    lines.append("  " + "-" * 50)
    lines.append(f"  {'rank':>4}  {'curve':<8} {'residual':>12}  heat")
    lines.append("  " + "-" * 50)
    ordered = sorted(
        result.per_curve,
        key=lambda cr: (cr.rank if cr.rank is not None else 99, cr.label),
    )
    last_rank = None
    for cr in ordered:
        if cr.rank != last_rank and last_rank is not None:
            lines.append("")
        last_rank = cr.rank
        res_str = "  n/a" if cr.residual is None else f"{cr.residual:12.6f}"
        glyph = _glyph(cr.residual, _tol_of(result))
        rank_str = "?" if cr.rank is None else str(cr.rank)
        lines.append(f"  {rank_str:>4}  {cr.label:<8} {res_str}  {glyph}")
    lines.append("  " + "-" * 50)
    lines.append(f"  break-rank: {result.break_rank}")
    lines.append(f"  diagnosis : {result.diagnosis}")
    return "\n".join(lines)


def _tol_of(result: LocalizeResult) -> float:
    # The glyph threshold reuses the candidate tolerance; results that held are
    # exactly those with residual <= tol, so recover tol from a held curve, else
    # fall back to a tight default. Kept here so render needs only the result.
    for cr in result.per_curve:
        if cr.holds and cr.residual is not None:
            return max(cr.residual, 1e-9)
    return 1e-9


# --------------------------------------------------------------------------
# curve x prime localization.
# --------------------------------------------------------------------------

@dataclass
class PrimeRow:
    label: str
    rank: Optional[int]
    cells: Dict[int, Optional[float]]
    bad_primes: List[int]


@dataclass
class PrimeLocalizeResult:
    candidate: str
    description: str
    primes: List[int]
    rows: List[PrimeRow]
    heat_by_prime: Dict[int, float]
    diagnosis: str


def localize_primes(candidate: Candidate, curves=None,
                    primes: Optional[List[int]] = None) -> PrimeLocalizeResult:
    """Build the curve x prime heat-map for a candidate with per-prime structure.

    Requires candidate.prime_residual. For each curve and each scanned prime it
    records the residual, marks the primes of bad reduction (p | conductor), and
    ranks the columns by total heat so the diagnosis can name where the residual
    concentrates.
    """
    if candidate.prime_residual is None:
        raise ValueError(f"{candidate.name} has no prime_residual to localize")
    if curves is None:
        curves = all_curves()
    primes = primes or candidate.primes or [2, 3, 5, 7, 11, 13]

    rows: List[PrimeRow] = []
    heat_by_prime: Dict[int, float] = {p: 0.0 for p in primes}
    for E in curves:
        cells: Dict[int, Optional[float]] = {}
        for p in primes:
            res = candidate.prime_residual(E, p)
            cells[p] = res
            if res is not None:
                heat_by_prime[p] += res
        bad = [p for p in primes if E.conductor % p == 0]
        rows.append(PrimeRow(E.label, E.rank, cells, bad))

    hot = sorted((p for p in primes if heat_by_prime[p] > 0),
                 key=lambda p: (-heat_by_prime[p], p))
    if hot:
        named = ", ".join(f"{p}(heat {heat_by_prime[p]:.2f})" for p in hot)
        diagnosis = (
            f"HEAT CONCENTRATES AT primes {named}. For this probe those are exactly "
            "each curve's primes of bad reduction; a genuine candidate that needed a "
            "missing local condition at a bad prime would light up the same column, "
            "which is how a single inconsistent local a_p is caught."
        )
    else:
        diagnosis = "NO PRIME HEAT: the candidate holds at every scanned prime."

    return PrimeLocalizeResult(
        candidate.name, candidate.description, primes, rows, heat_by_prime, diagnosis
    )


def render_primes(result: PrimeLocalizeResult) -> str:
    """A curve x prime grid: a heat glyph per cell, bad-reduction primes starred."""
    lines: List[str] = []
    lines.append(f"LOCALIZE (primes)  {result.candidate}")
    lines.append(f"  {result.description}")
    lines.append("  " + _LEGEND + "   (bad-reduction prime marked < > around the column)")
    header = "  " + f"{'curve':<8}" + " " + " ".join(f"{p:>3}" for p in result.primes)
    lines.append(header)
    lines.append("  " + "-" * (len(header) - 2))
    for row in result.rows:
        cells = []
        for p in result.primes:
            g = _glyph(row.cells[p], 1e-9)
            if p in row.bad_primes:
                cells.append(f"<{g}>")
            else:
                cells.append(f" {g} ")
        lines.append("  " + f"{row.label:<8}" + " " + " ".join(cells))
    lines.append("  " + "-" * (len(header) - 2))
    lines.append(f"  diagnosis: {result.diagnosis}")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Demo candidates, reused by the driver and exercised by the self-test.
# --------------------------------------------------------------------------

def _resid_regulator_cliff(E) -> Optional[float]:
    """Continuous form of the miner's R4: max(0, regulator - 0.1).

    A single Heegner generator has small canonical height, so a rank-1 curve's
    1x1 regulator is < 0.1 and the residual is 0. A rank >= 2 regulator is a Gram
    determinant of independent heights and is larger, so the residual grows across
    the cliff. Rank 0 is vacuously in-regime (no generator height to be small).
    """
    if E.regulator is None or E.rank is None:
        return None
    if E.rank == 0:
        return 0.0
    return max(0.0, E.regulator - 0.1)


def _resid_sha_to_square(E) -> Optional[float]:
    """Distance from #Sha to the nearest perfect square (Cassels-Tate).

    Zero on every bundled curve (#Sha is 1 throughout), so this localizes to a
    survivor with no break: a necessary condition that holds across all ranks.
    """
    if E.sha_order is None:
        return None
    n = E.sha_order
    r = isqrt(n)
    return float(min(n - r * r, (r + 1) * (r + 1) - n))


def _presid_bad_reduction(E, p: int) -> float:
    """Per-prime probe: residual 1 at a prime of bad reduction, 0 at good primes.

    A trivially true local-condition probe whose only purpose is to show that the
    curve x prime heat-map isolates, per curve, exactly the primes dividing the
    conductor. A real candidate whose validity hinged on a local condition at a
    bad prime would localize identically.
    """
    return 1.0 if (E.conductor % p == 0) else 0.0


DEMO_CLIFF = Candidate(
    "R4_regulator_above_cliff",
    "max(0, regulator - 0.1): the one-point height ceiling, continuous",
    _resid_regulator_cliff,
    tol=1e-9,
)

DEMO_SURVIVOR = Candidate(
    "sha_to_nearest_square",
    "distance from #Sha to the nearest perfect square (Cassels-Tate)",
    _resid_sha_to_square,
    tol=1e-9,
)

DEMO_PRIME_LOCATOR = Candidate(
    "bad_reduction_locator",
    "per-prime probe: residual 1 at primes of bad reduction (p | N)",
    residual=lambda E: None,
    tol=0.5,
    prime_residual=_presid_bad_reduction,
    primes=[2, 3, 5, 7, 11, 13],
)


if __name__ == "__main__":
    # Self-test. Run: python -m experiments.engine.localize
    cliff = localize(DEMO_CLIFF)
    assert cliff.break_rank == 2, f"cliff break-rank should be 2, got {cliff.break_rank}"
    assert "CLIFF" in cliff.diagnosis, "cliff candidate must diagnose the cliff"
    # rank <= 1 must all hold (residual 0) for the cliff reading to be honest.
    for cr in cliff.per_curve:
        if cr.rank is not None and cr.rank <= 1:
            assert cr.holds, f"{cr.label} (rank {cr.rank}) should hold for DEMO_CLIFF"

    survivor = localize(DEMO_SURVIVOR)
    assert survivor.break_rank is None, "sha-to-square must never break on bundled data"
    assert "SURVIVOR" in survivor.diagnosis or "NO BREAK" in survivor.diagnosis

    # A relation that breaks inside the proven regime must be diagnosed as such.
    broken = Candidate(
        "always_breaks_rank1",
        "toy: residual 1 exactly on rank-1 curves",
        lambda E: (1.0 if E.rank == 1 else 0.0) if E.rank is not None else None,
        tol=0.5,
    )
    br = localize(broken)
    assert br.break_rank == 1, f"toy must break at rank 1, got {br.break_rank}"
    assert "PROVEN REGIME" in br.diagnosis

    primes = localize_primes(
        DEMO_PRIME_LOCATOR,
        curves=[get_curve(l) for l in ("11a1", "14a1", "15a1", "26a1")],
    )
    # Each curve must light up exactly its in-range bad primes.
    by_label = {row.label: row for row in primes.rows}
    assert by_label["14a1"].bad_primes == [2, 7], by_label["14a1"].bad_primes
    assert by_label["15a1"].bad_primes == [3, 5], by_label["15a1"].bad_primes
    assert by_label["11a1"].bad_primes == [11], by_label["11a1"].bad_primes

    print("localize self-test OK")
    print()
    print(render(cliff))
    print()
    print(render(survivor))
    print()
    print(render_primes(primes))
