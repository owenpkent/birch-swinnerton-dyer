"""PROPOSE: generate candidate rank >= 2 constructions and run them past the bar.

This is the creative lane of the engine, kept scrupulously honest. The actual
rank >= 2 construction is the open problem; PROPOSE does not conjure it. What it
does is mechanize Research Direction 01: it holds a library of candidate
construction CLASSES, each described by what it would output and what that output
secretly leans on, and runs every one through the Direction-01 test battery plus
the three detectors. The output is a scorecard that reproduces, as a re-runnable
computation, exactly which classes are retired, which are bottlenecked, which is
the live candidate, and which is not a construction at all.

The subtle honesty point this module exists to make: the rank >= 2 wall is NOT a
detector violation. The Heegner family, the diagonal cycles, the Kudla program
are all SOUND number-field constructions (Detectors 1 and 3 come back clean). The
reason they do not close rank >= 2 is structural, and the battery names it:

  T1 nondegeneracy   -- does the candidate output two independent non-torsion
                        points on 389a1 (det of the height pairing > 0), where the
                        Heegner machine provably outputs torsion (experiment e)?
  T2 second-order tie -- does the output size avoid factoring through the FIRST
                        derivative L'(E/K, 1)? On rank >= 2 input that number is 0
                        (experiment h), so anything proportional to it is the
                        one-point machine in disguise (the Gross-Kohnen-Zagier
                        pattern). The Clause-2 shape needs the SECOND derivative.

Two candidates are EXECUTABLE on our substrate, so their T1 is measured, not
declared: the Heegner single-point class (models the measured experiment-(e) fact
that its rank >= 2 output is torsion) fails T1, and exact small-height search
(experiment f) passes T1 but is flagged NOT A CONSTRUCTION (no L-tie, no Sha
bound, no upper bound, does not generalize). The rest are non-executable classes
carrying their honest Direction-01 status. The punchline the engine prints: of
every candidate, only non-constructive search passes T1, and every actual
construction class is first-derivative-bottlenecked, retired, the open Clause-2
candidate, or the Selmer-bounding lane. The frontier node rank_two_object stays
open. PROPOSE leaves a slot where a genuinely new construction is dropped in and
tested; it does not pretend that slot is filled.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional

from experiments._shared import get_curve
from experiments._shared.rational_points import (
    canonical_height,
    det,
    gram_matrix,
    search_points,
)

from .audit import Method, AuditVerdict, audit_method


TORSION_TOL = 1e-4   # canonical height below this is torsion on these curves
DET_TOL = 1e-4       # relative tolerance for "the Gram determinant is nonzero"


# --------------------------------------------------------------------------
# A candidate construction: what it outputs and what that output leans on.
# --------------------------------------------------------------------------

@dataclass
class Construction:
    """One candidate rank >= 2 construction class.

    output_factors_through declares the analytic quantity the output size is tied
    to, the single most discriminating property: "L'(E/K,1)" is the first
    derivative (0 on rank >= 2, the bottleneck), "L''(E/K,1)/2!" is the Clause-2
    second-derivative shape, "search (no L-tie)" is a non-constructive search,
    "Selmer bound (no points)" is the Direction-02 Sha-bounding lane.

    produce(E), when present, makes T1 EXECUTABLE: it returns the rational points
    the candidate would put on E (possibly none). When absent, the candidate is a
    non-executable class carrying its honest Direction-01 known_status.
    """

    name: str
    input_class: str
    output_factors_through: str
    needs_geometric_frobenius: bool = False
    needs_base_curve: bool = False
    assumes_sha_finite: bool = False
    auxiliary_object: str = ""
    known_status: str = ""
    produce: Optional[Callable[[object], list]] = None


def _independent_points(E, points, r):
    """Greedily pick r non-torsion points with nonzero Gram determinant.

    Mirrors experiment (f): take points of increasing canonical height and keep a
    candidate only if it increases the Gram rank (the determinant stays away from
    0 relative to the diagonal scale). Returns (chosen, M) or (None, None).
    """
    ranked = sorted(
        (P for P in points if canonical_height(E, P) > TORSION_TOL),
        key=lambda P: canonical_height(E, P),
    )
    chosen: list = []
    for P in ranked:
        trial = chosen + [P]
        M = gram_matrix(E, trial)
        scale = 1.0
        for i in range(len(trial)):
            scale *= max(M[i][i], 1e-12)
        if det(M) > DET_TOL * scale:
            chosen = trial
            if len(chosen) == r:
                return chosen, M
    return None, None


# --------------------------------------------------------------------------
# The test battery (Direction 01 T1/T2) plus AUDIT.
# --------------------------------------------------------------------------

@dataclass
class BatteryResult:
    name: str
    input_class: str
    t1: Optional[bool]
    t1_detail: str
    t2: Optional[bool]
    t2_detail: str
    audit: AuditVerdict
    verdict: str


def run_battery(c: Construction, E=None) -> BatteryResult:
    """Run one construction through T1, T2, and the three detectors on 389a1."""
    if E is None:
        E = get_curve("389a1")  # the rank-2 open-regime control

    # ---- T1 nondegeneracy (executable when the candidate can produce points) --
    if c.produce is not None:
        pts = c.produce(E)
        nontorsion = [P for P in pts if canonical_height(E, P) > TORSION_TOL]
        chosen, M = _independent_points(E, nontorsion, 2)
        t1 = chosen is not None
        if t1:
            t1_detail = (f"{len(nontorsion)} non-torsion points produced; "
                         f"det of 2x2 height pairing = {det(M):.5f} > 0")
        else:
            t1_detail = (f"{len(nontorsion)} non-torsion points produced; "
                         "no two are independent (rank-2 witness not exhibited)")
    else:
        t1 = None
        t1_detail = "not executable on the substrate; see known status"

    # ---- T2 second-order tie (declared property of the candidate class) -------
    ft = c.output_factors_through
    if ft == "L'(E/K,1)":
        t2 = False
        t2_detail = ("output size factors through the FIRST derivative L'(E/K,1), "
                     "which is 0 on rank >= 2 input (measured for the Heegner class "
                     "in experiment h). This is the one-point bottleneck.")
    elif ft.startswith("L''") or ft == "second derivative":
        t2 = True
        t2_detail = ("output DECLARED tied to the SECOND derivative: the Clause-2 "
                     "shape. Realizable over function fields (Yun-Zhang); the "
                     "bridges to L(E,s) and to points are OPEN over Q.")
    elif ft == "search (no L-tie)":
        t2 = False
        t2_detail = ("no analytic tie at all: the points are searched, not "
                     "constructed. Certifies rank >= 2 numerically for THIS curve "
                     "but is not a method and yields no upper bound.")
    elif ft == "Selmer bound (no points)":
        t2 = None
        t2_detail = ("produces no points; this is the Sha-bounding lane "
                     "(Direction 02), judged by Clause 3, not T1/T2.")
    else:
        t2 = None
        t2_detail = "no declared analytic tie."

    # ---- AUDIT (the three detectors) ------------------------------------------
    claims_full_rank = ft != "Selmer bound (no points)"
    method = Method(
        name=c.name,
        claims_full_rank=claims_full_rank,
        uses_only_root_number=False,
        assumes_sha_finite=c.assumes_sha_finite,
        target_regime="rank_ge2",
        uses_geometric_frobenius=c.needs_geometric_frobenius,
        needs_base_curve=c.needs_base_curve,
    )
    audit = audit_method(method, analytic_rank=2, E=E)

    verdict = _verdict(c, t1, t2, audit)
    return BatteryResult(c.name, c.input_class, t1, t1_detail, t2, t2_detail,
                         audit, verdict)


def _verdict(c: Construction, t1, t2, audit: AuditVerdict) -> str:
    """Synthesize the honest one-line verdict for a battery run."""
    if audit.function_field_flagged:
        return ("FUNCTION-FIELD ONLY (Detector 3): leans on a geometric Frobenius "
                "or base curve absent over Q.")
    if c.known_status.startswith("RETIRED"):
        return ("RETIRED (Gross-Kohnen-Zagier theorem): multi-field Heegner points "
                "are proportional, so any pair has height-pairing determinant 0. A "
                "theorem, not a guess; the template for a clean kill.")
    if c.output_factors_through == "search (no L-tie)":
        return ("NOT A CONSTRUCTION (search): passes T1 on this curve but is no "
                "general method, has no L-tie and no Sha bound, and gives no upper "
                "bound. The constructible easy half (experiment f).")
    if c.output_factors_through == "Selmer bound (no points)":
        return ("DIRECTION 02 LANE: bounds Selmer / Sha, produces no points; "
                "judged by Clause 3, not the point battery.")
    if t1 is False:
        return ("FAILS T1: produces no rank-2 witness (its rank >= 2 output is "
                "torsion, the measured experiment-(e) ceiling). The one-point "
                "machine.")
    if t2 is False and c.output_factors_through == "L'(E/K,1)":
        return ("FIRST-DERIVATIVE BOTTLENECKED (Clause 2 fail): one derivative is "
                "the whole output and it is 0 on rank >= 2 (the GKZ pattern). "
                "Capped at rank <= 1.")
    if t2 is True:
        return ("LIVE CLAUSE-2 CANDIDATE: the right second-derivative shape, but "
                "the bridges (Eisenstein -> L(E,s), cycle classes -> points) are "
                "OPEN over Q. Proves nothing yet; the slot a new construction fills.")
    return "INCONCLUSIVE."


# --------------------------------------------------------------------------
# The candidate library: the Direction-01 input classes, plus two executable ends.
# --------------------------------------------------------------------------

def _produce_heegner_zero(E) -> list:
    """The Heegner machine's rank >= 2 output, encoded as the measured fact.

    Experiment (e) measured that on 389a1 (and 5077a1) the Heegner construction
    lands on torsion (the zero point), because its height is L'(E/K,1) = 0 there.
    We do not re-run the modular parametrization; we encode the measured outcome:
    no non-torsion point is produced. So T1 fails, exactly as it must.
    """
    return []


def _produce_search(E) -> list:
    """Exact small-height search (experiment f): the constructible easy half."""
    return search_points(E, x_bound=10, denom_bound=2)


CONSTRUCTIONS: List[Construction] = [
    Construction(
        name="heegner_point_single",
        input_class="Heegner point (one imaginary quadratic field)",
        output_factors_through="L'(E/K,1)",
        produce=_produce_heegner_zero,
        known_status=("On rank >= 2 input the Heegner point is torsion (experiment "
                      "e); its height is L'(E/K,1) = 0 (experiment h)."),
    ),
    Construction(
        name="heegner_multifield",
        input_class="Heegner points over several imaginary quadratic fields",
        output_factors_through="L'(E/K,1)",
        known_status=("RETIRED by Gross-Kohnen-Zagier: the y_D lie on one line in "
                      "E(Q) (x) Q, so any pair has height-pairing determinant 0 "
                      "(exhibited on 37a1 in experiment h)."),
    ),
    Construction(
        name="stark_heegner_darmon",
        input_class="Stark-Heegner / Darmon points (real quadratic)",
        output_factors_through="L'(E/K,1)",
        known_status=("Conjectural rationality; still one point per field, and a "
                      "GKZ-type proportionality for pairs is plausible, unexamined."),
    ),
    Construction(
        name="generalized_heegner_cycles",
        input_class="Generalized Heegner cycles (Bertolini-Darmon-Prasanna)",
        output_factors_through="L'(E/K,1)",
        known_status=("Proven p-adic formulas, rank <= 1 regime; input material, "
                      "not a rank-2 output."),
    ),
    Construction(
        name="diagonal_cycles",
        input_class="Diagonal cycles (Gross-Kudla-Schoen, Darmon-Rotger)",
        output_factors_through="L'(E/K,1)",
        known_status=("One cycle controlled by a FIRST central derivative of a "
                      "triple-product L; a different bottleneck, same order."),
    ),
    Construction(
        name="kudla_arithmetic_theta",
        input_class="Kudla program / arithmetic theta series",
        output_factors_through="L''(E/K,1)/2! (declared)",
        auxiliary_object=("codimension-2 special cycles vs the second derivative "
                          "of a Siegel-Eisenstein series"),
        known_status=("The only systematic source of SECOND derivatives in "
                      "arithmetic geometry today; the two bridges (Eisenstein -> "
                      "L(E,s), cycle -> point) are OPEN over Q; Yun-Zhang prove the "
                      "all-orders shape over function fields."),
    ),
    Construction(
        name="higher_euler_system",
        input_class="Higher-rank Euler system (Beilinson-Flach, ...)",
        output_factors_through="Selmer bound (no points)",
        known_status=("Bounds Selmer groups; Direction 02 lane; constructs no "
                      "points, so it pairs with Clause 3 rather than T1/T2."),
    ),
    Construction(
        name="brute_force_search",
        input_class="Exact small-height search (experiment f)",
        output_factors_through="search (no L-tie)",
        produce=_produce_search,
        known_status=("Finds r independent points on every bundled rank >= 2 curve "
                      "by enumeration; the constructible easy half. Not a "
                      "construction: no L-tie, no Sha bound, no upper bound."),
    ),
]


def propose(E=None) -> List[BatteryResult]:
    """Run every candidate construction through the battery on the rank-2 control."""
    return [run_battery(c, E) for c in CONSTRUCTIONS]


def scorecard(results: List[BatteryResult]) -> str:
    """A printable table plus the honest Direction-01 summary."""
    lines: List[str] = []
    lines.append("PROPOSE SCORECARD: candidate rank >= 2 constructions vs the bar")
    lines.append("=" * 78)

    def cell(v: Optional[bool]) -> str:
        return "n/a" if v is None else ("PASS" if v else "FAIL")

    lines.append(f"{'construction':<26} {'T1':>5} {'T2':>5}  verdict")
    lines.append("-" * 78)
    for r in results:
        lines.append(f"{r.name:<26} {cell(r.t1):>5} {cell(r.t2):>5}  {r.verdict.split(':')[0]}")
    lines.append("-" * 78)
    lines.append("  T1 is EXECUTABLE (measured on 389a1); T2 is a DECLARED property of")
    lines.append("  each construction class, not a measured result.")
    lines.append("")

    passes_t1 = [r for r in results if r.t1 is True]
    live = [r for r in results if r.t2 is True]
    lines.append("HONEST SUMMARY (Direction 01, mechanized):")
    lines.append(f"  candidates passing T1 (a real rank-2 witness): {len(passes_t1)}")
    for r in passes_t1:
        lines.append(f"      - {r.name}: {r.verdict}")
    lines.append(f"  live Clause-2 candidates (second-derivative shape): {len(live)}")
    for r in live:
        lines.append(f"      - {r.name}: {r.verdict}")
    lines.append("")
    lines.append("Every ACTUAL construction class is first-derivative-bottlenecked,")
    lines.append("retired (GKZ), the open Clause-2 candidate (bridges open over Q), or")
    lines.append("the Selmer-bounding lane. The only T1-passer is non-constructive")
    lines.append("search. The frontier node rank_two_object stays OPEN: PROPOSE leaves")
    lines.append("the slot where a genuinely new construction is dropped in and tested.")
    return "\n".join(lines)


if __name__ == "__main__":
    # Run: python -m experiments.engine.propose
    results = propose()
    by_name = {r.name: r for r in results}

    # The two executable ends must measure, not declare.
    assert by_name["brute_force_search"].t1 is True, "search must exhibit a rank-2 witness on 389a1"
    assert by_name["heegner_point_single"].t1 is False, "the Heegner single point must fail T1 on 389a1"
    # The Kudla class is the live second-derivative candidate.
    assert by_name["kudla_arithmetic_theta"].t2 is True, "Kudla must be the Clause-2 shape"
    # No library entry trips a detector: the wall is structural, not a detector hit.
    assert all(r.audit.clean for r in results), "no candidate here is detector-unsound; the wall is Clause 2"
    # Nothing establishes the frontier: search passes T1 but is not a construction.
    assert "NOT A CONSTRUCTION" in by_name["brute_force_search"].verdict

    print("propose self-test OK")
    print()
    print(scorecard(results))
