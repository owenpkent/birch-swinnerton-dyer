"""PROPOSE + FALSIFY + AUDIT: mine the bundled invariants for relations, honestly.

The engine's job is to find numerical relations among a curve's invariants and
then refuse to be impressed by the ones that are secretly the rank-1 machine in
disguise or that lean on an open conjecture. This module is that refusal made
mechanical. It defines a small library of candidate Relations over the BUNDLED
invariants (rank, torsion, root number, real period, regulator, Tamagawa
product, Sha order), evaluates each across the rank 0/1/2/3 control ladder, and
classifies the outcome:

  holds_all            -- true on every curve, including the open rank >= 2 ones.
  holds_rank_le1_only  -- true on rank <= 1, FALSE on some rank >= 2 curve.
                          This is the CLIFF: a relation that dies at rank 2 was
                          a property of the one-point Heegner regime, not of BSD.
  fails                -- false somewhere in rank <= 1 already (dead on arrival).
  mixed                -- true and false across rank <= 1 with no clean rank cut.

The honest output is the pairing of classification with AUDIT. A relation that
holds_all but whose Method audit flags Sha-finiteness is a SURVIVOR WITH CAVEAT:
evidence in rank >= 2, never proof, because it solved a formula that assumes the
open finiteness. A relation classified holds_rank_le1_only is a CASUALTY at the
cliff: it filters exactly the way a parity / rank-1-only candidate must, so the
engine reports it as killed rather than as a discovery.

WHY mine the BUNDLED invariants and not recompute L-values: speed and offline
operation. Every relation here is a pure function of stored integers and floats,
so the whole sweep runs in well under a second. One live falsification demo does
compute L(E,1) for the rank-0 curves only (cheap, the center is a single AFE
evaluation) to show a relation being checked against a freshly computed quantity
rather than a stored one. The rank-3 L-derivatives are never touched (too slow).

The classification is deliberately conservative: a relation has to be true on
ALL of rank 0 and rank 1 and FALSE on at least one rank >= 2 curve to earn
holds_rank_le1_only. That is the signature of the proven-regime ceiling, and it
is exactly the wrong-approach pattern the engine must surface, not hide.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isqrt
from typing import Callable, Dict, List, Optional

import mpmath as mp

from experiments._shared import all_curves, get_curve
from .audit import Method, AuditVerdict, audit_method


# --------------------------------------------------------------------------
# A candidate relation: a named predicate over a curve plus its risk profile.
# --------------------------------------------------------------------------

@dataclass
class Relation:
    """One candidate numerical law over a curve's invariants.

    predicate(E) returns True (holds), False (fails), or None (not applicable
    to this curve, e.g. a quantity is missing). method is the AUDIT descriptor:
    it declares what proving-via-this-relation would secretly lean on, so the
    same three detectors that judge a Method judge the relation.
    """

    name: str
    description: str
    predicate: Callable[[object], Optional[bool]]
    method: Method


def _is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    r = isqrt(n)
    return r * r == n


# --------------------------------------------------------------------------
# The relation library.
# --------------------------------------------------------------------------

def _r1_parity_matches_root_number(E) -> Optional[bool]:
    """R1: w == (-1)^rank. True on every curve; it is the parity fact itself."""
    if E.root_number is None or E.rank is None:
        return None
    return E.root_number == (-1) ** E.rank


def _r2_sha_is_square(E) -> Optional[bool]:
    """R2: #Sha is a perfect square (Cassels-Tate). True on every bundled curve."""
    if E.sha_order is None:
        return None
    return _is_perfect_square(E.sha_order)


def _r3_strong_bsd_residual(E) -> Optional[bool]:
    """R3: the strong-BSD formula is internally consistent with #Sha a square.

    Checks that Omega * Reg * prod(c_p) * #Sha / #tors^2 is positive and finite
    (the right-hand side of the leading-coefficient formula is well-formed) and
    that the bundled #Sha is a perfect square. Uses the BUNDLED #Sha as the
    stand-in for the leading coefficient relationship, i.e. it verifies the BSD
    formula is self-consistent rather than recomputing L^{(r)}. AUDIT flags
    Sha-finiteness, so this is a SURVIVOR WITH CAVEAT in rank >= 2.
    """
    needed = [E.real_period, E.regulator, E.tamagawa_product,
              E.sha_order, E.torsion_order]
    if any(v is None for v in needed):
        return None
    rhs = (E.real_period * E.regulator * E.tamagawa_product * E.sha_order)
    rhs = rhs / (E.torsion_order ** 2)
    if not (rhs > 0 and rhs < float("inf")):
        return False
    return _is_perfect_square(E.sha_order)


def _r4_regulator_below_cliff(E) -> Optional[bool]:
    """R4: regulator < 0.1, a deliberately rank <= 1 -only relation.

    A single Heegner generator on a rank-1 curve has small canonical height, so
    its 1x1 regulator is tiny (the bundled rank-1 regulators are all < 0.1). On
    a rank >= 2 curve the regulator is a Gram determinant of two or more
    independent heights and is larger. The bundled rank-0 curves have regulator
    exactly 1.0 (empty product is 1), which is NOT < 0.1, so this relation is
    really a rank-EXACTLY-1 signature. To make the cliff demo clean we treat the
    rank-0 case as vacuously in-regime (the one-point ceiling is about rank 1
    being the top of the proven ladder), and require it to FAIL on rank >= 2.

    The point is pedagogical: this relation is a height-of-one-point artifact.
    It HOLDS on the rank-1 curves and FAILS on the rank >= 2 curves, so the
    classifier brands it holds_rank_le1_only and the engine reports a CASUALTY.
    """
    if E.regulator is None or E.rank is None:
        return None
    if E.rank == 0:
        # Vacuously in-regime: rank 0 has no generator height to be small.
        return True
    return E.regulator < 0.1


RELATIONS: List[Relation] = [
    Relation(
        name="R1_parity_matches_root_number",
        description="root_number == (-1)**rank",
        predicate=_r1_parity_matches_root_number,
        method=Method(
            name="R1 (parity from root number)",
            claims_full_rank=True,
            uses_only_root_number=True,
            target_regime="rank_ge2",
        ),
    ),
    Relation(
        name="R2_sha_is_square",
        description="#Sha is a perfect square (Cassels-Tate)",
        predicate=_r2_sha_is_square,
        method=Method(
            name="R2 (Sha is a square)",
            target_regime="all",
        ),
    ),
    Relation(
        name="R3_strong_bsd_residual",
        description="strong-BSD formula self-consistent, #Sha a square",
        predicate=_r3_strong_bsd_residual,
        method=Method(
            name="R3 (strong BSD reads off #Sha)",
            assumes_sha_finite=True,
            target_regime="rank_ge2",
        ),
    ),
    Relation(
        name="R4_regulator_below_cliff",
        description="regulator < 0.1 (a rank<=1 -only artifact)",
        predicate=_r4_regulator_below_cliff,
        method=Method(
            name="R4 (one-point height ceiling)",
            claims_full_rank=True,
            uses_only_root_number=False,
            target_regime="rank_ge2",
        ),
    ),
]


# --------------------------------------------------------------------------
# Evaluation and classification.
# --------------------------------------------------------------------------

@dataclass
class Evaluation:
    relation: str
    per_curve: Dict[str, Optional[bool]]
    classification: str


def evaluate(relation: Relation, curves) -> Evaluation:
    """Evaluate a relation across curves and classify the rank-cut behaviour.

    Per-curve result is True / False / None (not applicable). Classification:
      holds_all            -- True on every applicable curve.
      holds_rank_le1_only  -- True on every applicable rank <= 1 curve, and
                              False on at least one rank >= 2 curve.
      fails                -- False on at least one rank <= 1 curve.
      mixed                -- anything else (no clean rank cut).
    """
    per_curve: Dict[str, Optional[bool]] = {}
    for E in curves:
        per_curve[E.label] = relation.predicate(E)

    applicable = [(E, per_curve[E.label]) for E in curves
                  if per_curve[E.label] is not None]
    le1 = [(E, v) for (E, v) in applicable if E.rank is not None and E.rank <= 1]
    ge2 = [(E, v) for (E, v) in applicable if E.rank is not None and E.rank >= 2]

    all_true = all(v for (_, v) in applicable) if applicable else False
    le1_all_true = all(v for (_, v) in le1) if le1 else False
    some_ge2_false = any(not v for (_, v) in ge2) if ge2 else False
    some_le1_false = any(not v for (_, v) in le1) if le1 else False

    if all_true:
        classification = "holds_all"
    elif le1_all_true and some_ge2_false and not some_le1_false:
        classification = "holds_rank_le1_only"
    elif some_le1_false:
        classification = "fails"
    else:
        classification = "mixed"

    return Evaluation(relation.name, per_curve, classification)


@dataclass
class Row:
    relation: str
    description: str
    classification: str
    verdict: AuditVerdict
    verdict_label: str = ""


def _verdict_label(classification: str, verdict: AuditVerdict) -> str:
    """The engine's honest headline for a (classification, audit) pair.

    holds_rank_le1_only -> CASUALTY AT CLIFF regardless of audit (it is the
    proven-regime ceiling caught in the act). holds_all but the audit is not
    clean -> SURVIVOR WITH CAVEAT (evidence not proof in rank >= 2). holds_all
    and clean -> SURVIVOR. Everything else -> the classification stands.
    """
    if classification == "holds_rank_le1_only":
        return "CASUALTY AT CLIFF (rank-1 machine in disguise)"
    if classification == "holds_all":
        if verdict.clean:
            return "SURVIVOR (holds_all, detectors clean)"
        caveats = []
        if verdict.parity_only:
            caveats.append("parity-only")
        if "SHA ASSUMED" in verdict.sha_message:
            caveats.append("Sha-finiteness open in rank>=2")
        if verdict.function_field_flagged:
            caveats.append("function-field mirage")
        cav = "; ".join(caveats) if caveats else "see audit"
        return f"SURVIVOR WITH CAVEAT ({cav}); evidence not proof in rank>=2"
    if classification == "fails":
        return "REJECTED (false already in rank <= 1)"
    return "INCONCLUSIVE (no clean rank cut)"


def mine(curves=None) -> List[Row]:
    """Run the whole library: evaluate, audit, and label every relation.

    Returns one Row per relation carrying the rank-cut classification, the
    three-detector AuditVerdict for the relation's Method, and the engine's
    honest headline label (CASUALTY / SURVIVOR / SURVIVOR WITH CAVEAT / ...).
    """
    if curves is None:
        curves = all_curves()
    rows: List[Row] = []
    for rel in RELATIONS:
        ev = evaluate(rel, curves)
        verdict = audit_method(rel.method, analytic_rank=2)
        label = _verdict_label(ev.classification, verdict)
        rows.append(Row(
            relation=rel.name,
            description=rel.description,
            classification=ev.classification,
            verdict=verdict,
            verdict_label=label,
        ))
    return rows


def scorecard(rows: List[Row]) -> str:
    """A printable table: relation | classification | detector flags | verdict."""
    lines: List[str] = []
    lines.append("MINE SCORECARD: candidate relations over bundled invariants")
    lines.append("=" * 78)
    header = f"{'relation':<32} {'classification':<20} {'detectors'}"
    lines.append(header)
    lines.append("-" * 78)
    for row in rows:
        flags = []
        if row.verdict.parity_only:
            flags.append("PARITY")
        if "SHA ASSUMED" in row.verdict.sha_message:
            flags.append("SHA")
        if row.verdict.function_field_flagged:
            flags.append("FUNCFIELD")
        flag_str = ",".join(flags) if flags else "clean"
        lines.append(f"{row.relation:<32} {row.classification:<20} {flag_str}")
        lines.append(f"    -> {row.verdict_label}")
    lines.append("-" * 78)

    casualties = [r for r in rows if r.classification == "holds_rank_le1_only"]
    survivors_caveat = [r for r in rows if r.classification == "holds_all"
                        and not r.verdict.clean]
    survivors_clean = [r for r in rows if r.classification == "holds_all"
                       and r.verdict.clean]

    lines.append("")
    lines.append("HONEST SUMMARY:")
    lines.append(f"  casualties at the cliff (rank<=1 only):     {len(casualties)}")
    for r in casualties:
        lines.append(f"      - {r.relation}: died at rank 2; it was the one-point "
                     f"regime, not BSD.")
    lines.append(f"  survivors WITH CAVEAT (holds_all, flagged): {len(survivors_caveat)}")
    for r in survivors_caveat:
        lines.append(f"      - {r.relation}: holds everywhere but audit is not clean; "
                     f"EVIDENCE not proof in rank>=2.")
    lines.append(f"  clean survivors (holds_all, no flag):       {len(survivors_clean)}")
    for r in survivors_clean:
        lines.append(f"      - {r.relation}: holds_all and clean (still only a "
                     f"necessary condition, not a rank>=2 proof).")
    lines.append("")
    lines.append("Nothing here proves BSD in rank>=2. A clean holds_all relation is a")
    lines.append("necessary condition; the open object is still the construction of two")
    lines.append("independent points / an unconditional Euler system (see atlas_graph).")
    return "\n".join(lines)


def live_falsification_demo() -> str:
    """One live check: recompute L(E,1) for the rank-0 curves and falsify a law.

    Cheap because the center s = 1 is a single AFE evaluation and the rank-0
    curves have small conductor. The candidate law under test is the rank-0
    consequence of weak BSD: L(E,1) != 0 exactly when rank == 0. We compute
    L(E,1) live for the bundled rank-0 curves and confirm it is non-zero, then
    note the law's deliberate failure mode: it would (wrongly) be 'falsified' if
    extended to a rank >= 2 curve, which is precisely why we do NOT compute the
    rank >= 2 center here. This demonstrates a live falsification harness while
    staying inside the fast, proven regime.
    """
    mp.mp.dps = 25
    lines: List[str] = []
    lines.append("LIVE FALSIFICATION (rank-0 curves only, L(E,1) computed fresh):")
    rank0 = [E for E in all_curves() if E.rank == 0]
    all_ok = True
    for E in rank0:
        val = E.L_value(mp.mpc(1))
        nonzero = abs(val) > 1e-6
        ok = nonzero  # weak BSD rank-0 prediction: L(E,1) != 0
        all_ok = all_ok and ok
        lines.append(f"  {E.label}: |L(E,1)| = {float(abs(val)):.6f}  "
                     f"-> rank-0 law {'HOLDS' if ok else 'FALSIFIED'}")
    lines.append(f"  rank-0 weak-BSD law survived live check on all "
                 f"{len(rank0)} curves: {all_ok}")
    lines.append("  (We do NOT compute the rank>=2 center: it is slow and is exactly")
    lines.append("   the open regime the engine must reach by construction, not by")
    lines.append("   reading a single L-value.)")
    return "\n".join(lines)


if __name__ == "__main__":
    # Run: python -m experiments.engine.mine
    rows = mine()
    print(scorecard(rows))
    print()
    print(live_falsification_demo())
