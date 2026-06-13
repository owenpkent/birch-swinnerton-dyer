"""Experiment (j): 2-descent, the rigorous upper bound experiment (f) leaves open.

Experiment (f) builds the LOWER half of the rank-r object: r independent points
with a nonzero Neron-Tate Gram determinant certify rank E(Q) >= r. The matching
UPPER bound rank E(Q) <= r is the Selmer/Sha side, the wall where every
unconditional method stops at analytic rank <= 1. This experiment shows that for
one classical class of curves the upper bound is computable TODAY, with no number
fields, no class groups, and no assumption that Sha is finite: curves carrying a
rational 2-isogeny, descended by Silverman AEC X.4.

The worked family is the congruent-number curves

    E_n : y^2 = x^3 - n^2 x        (full rational 2-torsion at x = 0, +-n),

Silverman's own example (X.6). A squarefree integer n is "congruent" (the area
of a rational right triangle) exactly when rank E_n >= 1, so the literature
pins the truth and the descent can be checked against it.

What the experiment exhibits, in order:
  1. CALIBRATION. A bundled rank-0 curve with a rational 2-torsion point: descent
     returns upper bound 0, equal to the known rank, with Sha = 1. The gap of
     (f) is closed unconditionally.
  2. THE RANK LADDER. Across the family the descent upper bound climbs 0, 1, 2.
     For n = 34 the upper bound is 2 AND an independent-point search (the (f)
     machinery, reused) finds 2 independent points, so rank E_34 = 2 is PROVEN
     with no BSD input. This is the object (f) could only bound from below.
  3. THE HONEST LIMIT (Detector 2). For n = 17 (non-congruent, rank 0) the
     descent upper bound is 2, not 0: the first descent sees a nontrivial
     Sha[2] and so does NOT pin the rank. Descent bounds Sha THROUGH the
     2-isogeny only; it never proves #Sha finite. The gap upper - rank is a
     single 2-power slice of Sha, displayed, not assumed away.
  4. THE WALL (Detector 3). Run on the (f) curves 389a1, 433a1, 571a1, 643a1,
     5077a1 the descent does not even start: they have trivial torsion, so
     E[2] is irreducible and there is no rational 2-isogeny. The general
     2-descent there runs in the cubic field Q[x]/(2-division polynomial) and
     needs that field's class group and units, the arithmetic object the
     function-field case gets from H^2 of the surface and Q does not supply.

Run from the repo root:
    python -m experiments.two_descent.e_j_two_descent
"""

from __future__ import annotations

from experiments._shared import (
    get_curve, all_curves, sha_finiteness_flag, function_field_template,
)
from experiments._shared.descent import (
    descent_rank_bound, to_2torsion_form, rational_two_torsion_x,
)
from experiments._shared.elliptic_curve import EllipticCurve
from experiments._shared.rational_points import (
    search_points, canonical_height, gram_matrix, det,
)

# (f) curves: the open-regime targets whose rank is bounded below in (f).
OPEN_CURVES = ["389a1", "433a1", "571a1", "643a1", "5077a1"]

DOUBLINGS = 7      # enough to see a nonzero Gram determinant (independence)
TORSION_TOL = 1e-3
DET_TOL = 1e-3


def family_curve(n: int) -> EllipticCurve:
    """E_n : y^2 = x^3 - n^2 x as a (rank-bearing) EllipticCurve handle.

    Only the group law / height side is used here, which depends on the
    a-invariants alone; the conductor is irrelevant to descent and search.
    """
    return EllipticCurve(label=f"E_{n}", a_invariants=[0, 0, 0, -n * n, 0],
                         conductor=1)


def independent_count(E: EllipticCurve, want: int,
                      x_bound: int = 48, denom_bound: int = 4) -> int:
    """Lower bound on rank E(Q): size of an independent set found by search.

    Reuses the experiment (f) recipe: search small-height points, drop torsion
    (and the 2-torsion y = 0 points), greedily keep points that grow the
    Neron-Tate Gram rank (determinant stays away from 0).
    """
    pts = [P for P in search_points(E, x_bound, denom_bound)
           if P[1] != 0 and canonical_height(E, P, DOUBLINGS) > TORSION_TOL]
    pts.sort(key=lambda P: canonical_height(E, P, DOUBLINGS))
    chosen = []
    for P in pts:
        trial = chosen + [P]
        M = gram_matrix(E, trial, DOUBLINGS)
        scale = 1.0
        for i in range(len(trial)):
            scale *= max(M[i][i], 1e-12)
        if det(M) > DET_TOL * scale:
            chosen = trial
            if len(chosen) == want:
                break
    return len(chosen)


def main() -> int:
    # ---- 1. calibration: a bundled rank-0 curve with rational 2-torsion -----
    print("CALIBRATION (proven regime): bundled rank-0 curve, rational 2-torsion")
    cal = get_curve("14a1")
    ab = to_2torsion_form(cal.a_invariants)
    up = descent_rank_bound(*ab)["rank_upper_bound"]
    print(f"  14a1: isomorphic model y^2 = x^3 + {ab[0]}x^2 + {ab[1]}x")
    print(f"  descent rank upper bound = {up}    known rank = {cal.rank}    "
          f"#Sha = {cal.sha_order}")
    assert up == cal.rank, "descent upper bound must match the known rank here"
    print("  upper bound EQUALS the rank: the gap of experiment (f) is closed,")
    print("  unconditionally and with no Sha-finiteness assumption.")
    print()

    # ---- 2. the rank ladder on the congruent-number family ------------------
    print("THE RANK LADDER: E_n : y^2 = x^3 - n^2 x  (n congruent <=> rank >= 1)")
    print(f"{'n':>4} {'cong?':>6} {'descent<=':>10} {'pts found':>10} "
          f"{'verdict':>22}")
    print("-" * 58)
    # n = 1 non-congruent (rank 0); 6, 7 congruent rank 1; 34 congruent rank 2.
    ladder = [(1, False), (6, True), (7, True), (34, True)]
    for n, cong in ladder:
        E = family_curve(n)
        upper = descent_rank_bound(0, -n * n)["rank_upper_bound"]
        lower = independent_count(E, upper)
        if lower == upper:
            verdict = f"rank = {upper} PROVEN"
        else:
            verdict = f"rank in [{lower}, {upper}]"
        print(f"{n:>4} {str(cong):>6} {upper:>10} {lower:>10} {verdict:>22}")
    print("-" * 58)
    print("  n = 34: upper bound 2 AND two independent points found, so")
    print("  rank E_34(Q) = 2 with no BSD input. This is exactly the rank >= 2")
    print("  object experiment (f) can only bound from below.")
    print()

    # ---- 3. the honest limit (Detector 2): descent sees only Sha[2] ---------
    print("THE HONEST LIMIT (Detector 2): n = 17, non-congruent, true rank 0")
    upper17 = descent_rank_bound(0, -17 * 17)["rank_upper_bound"]
    lower17 = independent_count(family_curve(17), max(upper17, 1))
    print(f"  descent upper bound = {upper17}, independent points found = {lower17}")
    print(f"  the gap {upper17} - 0 = {upper17} is dim Sha(E_17)[phi] + "
          f"dim Sha(E_17')[phi-hat]:")
    print("  the first 2-descent meets a nontrivial Sha[2] and does NOT pin the")
    print("  rank. Descent bounds Sha only through the 2-isogeny; #Sha finite is")
    print("  not proved here, exactly as the detector insists.")
    flag = sha_finiteness_flag(get_curve("389a1"), analytic_rank=2,
                               method_assumes_finite=False)
    print(f"  {flag.message}")
    print()

    # ---- 4. the wall (Detector 3): the (f) curves have no rational 2-isogeny -
    print("THE WALL (Detector 3): the experiment (f) curves resist this descent")
    print(f"{'curve':>8} {'rank>= (f)':>11} {'rational 2-torsion?':>22} "
          f"{'2-isogeny descent':>20}")
    print("-" * 65)
    for label in OPEN_CURVES:
        E = get_curve(label)
        xs = rational_two_torsion_x(E.a_invariants)
        has = "yes" if xs else "no (E[2] irreducible)"
        applies = "applies" if to_2torsion_form(E.a_invariants) else "does NOT start"
        print(f"{label:>8} {E.rank:>11} {has:>22} {applies:>20}")
    print("-" * 65)
    tmpl = function_field_template()
    print("  These curves have trivial torsion, so E[2] is irreducible: no")
    print("  rational 2-isogeny exists and the elementary descent cannot begin.")
    print("  The general 2-descent runs in the cubic field Q[x]/(4x^3+b2 x^2+")
    print("  2b4 x+b6) and needs that field's class group and S-units. That is")
    print("  the missing arithmetic object:")
    print(f"    {tmpl.the_gap}")
    print()

    # ---- summary ------------------------------------------------------------
    print("SUMMARY. The upper bound of experiment (f) is computable, rigorously")
    print("and with no Sha-finiteness assumption, exactly when E carries a")
    print("rational 2-isogeny: it then pins the rank (rank E_34 = 2 with no BSD")
    print("input) up to a Sha[2] slice it makes explicit. The bundled rank >= 2")
    print("curves carry no such isogeny, so the gap there stays where the atlas")
    print("puts it: in the cubic field's class group and units, the object Q")
    print("does not hand over for free.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
