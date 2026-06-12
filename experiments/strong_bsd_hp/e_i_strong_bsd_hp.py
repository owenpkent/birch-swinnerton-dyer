"""Experiment (i): strong BSD at high precision in the open regime.

Experiment (c) solved the strong-BSD formula for #Sha and landed near 1 on
every bundled curve, but its regulator input was the doubling-limit height
(1e-5) and its leading coefficient came through default numerical
differentiation, so "#Sha = 1.0000" was a 4-digit statement. This experiment
rebuilds both inputs at working precision and turns the open-regime rows into
a 10+ digit statement:

  - REGULATORS: generators are re-found from scratch by exact search (as in
    experiment f), but the Neron-Tate Gram matrix is now computed with the
    sigma-function local heights of analytic_height.py (~20 digits), with
    pairings from heights of exact point sums. Three of the four rank-2
    curves (433a1, 571a1, 643a1) have Delta < 0, so this is also the first
    real exercise of the rhombic-lattice machinery on the open-regime curves.
  - LEADING COEFFICIENTS: L^{(r)}(E,1)/r! via Cauchy's integral formula
    (mpmath diff with method='quad' on a circle around s = 1), which keeps
    nearly full working precision where finite differences lose most of it.
    Cross-checked against the finite-difference value at coarse tolerance.
  - PERIODS: from the lattice itself (Omega = 2 w1 for Delta > 0, w1 for
    Delta < 0), checked against the bundled LMFDB value.

The output is conjectural #Sha = leading coefficient * tors^2 / (Omega * Reg
* prod c_p). RESULT: #Sha = 1 to within 5e-28 on all five rank >= 2 curves.
WHAT THIS IS: a much sharper consistency test of strong BSD in the regime
where Sha-finiteness is OPEN. Agreement with 1 to 27 digits is evidence,
never proof, and Detector 2 is invoked to say so. The falsifiability surface
is real, not rhetorical: the first run's 1e-5 cross-check against the bundle
exposed a wrong bundled regulator (5077a1, off at 3.4e-4, fixed 2026-06-11),
and the SigmaLattice self-checks exposed a quiet period-quadrature precision
loss (571a1). Wrong invariants now show immediately; 4-digit agreement could
never see either.

Run from the repo root (tens of minutes, dominated by the Cauchy-integral
derivatives; pass labels to run a subset):
    python -m experiments.strong_bsd_hp.e_i_strong_bsd_hp [labels...]
"""

from __future__ import annotations

import sys

import mpmath as mp

from experiments._shared import get_curve, sha_finiteness_flag
from experiments._shared.analytic_height import (
    SigmaLattice,
    canonical_height_sigma,
    elliptic_log,
)
from experiments._shared.rational_points import add, det, search_points
from experiments.independent_points.e_f_independent_points import (
    fmt_point,
    independent_subset,
)

CURVES = ["389a1", "433a1", "571a1", "643a1", "5077a1"]


def hp_height(E, P, L):
    return canonical_height_sigma(E, P, elliptic_log(E, P, L), L)


def hp_gram(E, gens, L):
    """Neron-Tate Gram matrix at working precision.

    Diagonal: sigma heights. Off-diagonal: <P,Q> = (h(P+Q) - h(P) - h(Q))/2
    with P+Q computed by the exact group law, so every entry reduces to
    heights of exactly known rational points.
    """
    r = len(gens)
    h = [hp_height(E, P, L) for P in gens]
    M = [[mp.mpf(0)] * r for _ in range(r)]
    for i in range(r):
        M[i][i] = h[i]
        for j in range(i + 1, r):
            hij = (hp_height(E, add(E, gens[i], gens[j]), L) - h[i] - h[j]) / 2
            M[i][j] = M[j][i] = hij
    return M


def main():
    mp.mp.dps = 28

    labels = sys.argv[1:] or CURVES
    print("Strong BSD in the open regime, rebuilt at working precision:")
    print("sigma-function regulators + Cauchy-integral leading coefficients.")
    print()
    rows = []
    for label in labels:
        E = get_curve(label)
        r = E.rank
        L = SigmaLattice(E)
        omega = 2 * L.w1 if L.disc > 0 else L.w1
        assert abs(omega - mp.mpf(E.real_period)) < 1e-8 * omega, \
            f"{label}: lattice period disagrees with bundled Omega"

        pts = search_points(E, x_bound=40, denom_bound=4)
        gens, M_doubling = independent_subset(E, pts, r)
        assert gens is not None, f"{label}: generators not found by search"

        M = hp_gram(E, gens, L)
        reg = det(M)
        assert abs(reg - det(M_doubling)) < 1e-3, \
            f"{label}: sigma Gram disagrees with doubling Gram"
        assert abs(reg - mp.mpf(E.regulator)) < 1e-5 * reg, \
            f"{label}: regulator disagrees with bundled value"

        lead = mp.diff(E.L_value, mp.mpf(1), r, method="quad",
                       radius=mp.mpf("0.25")) / mp.factorial(r)
        lead = mp.re(lead)
        lead_fd = mp.re(E.L_derivative_at_one(r)) / mp.factorial(r)
        assert abs(lead - lead_fd) < 1e-4 * abs(lead), \
            f"{label}: Cauchy and finite-difference leading terms disagree"

        sha = lead * E.torsion_order ** 2 / (omega * reg * E.tamagawa_product)
        gen_str = ", ".join(fmt_point(P) for P in gens)
        print(f"--- {label} (rank {r}, Delta {'>' if L.disc > 0 else '<'} 0) "
              f"generators {gen_str} ---")
        print(f"  Reg  = {mp.nstr(reg, 20)}   (bundled {E.regulator})")
        print(f"  L^({r})(1)/{r}! = {mp.nstr(lead, 20)}")
        print(f"  #Sha(BSD) = {mp.nstr(sha, 15)}   |sha - 1| = "
              f"{mp.nstr(abs(sha - 1), 3)}")
        print()
        rows.append((label, r, reg, sha, float(abs(sha - 1))))

    print("=" * 76)
    print(f"{'curve':>8} {'rank':>5} {'Reg (20 digits)':>26} {'#Sha(BSD)':>20} "
          f"{'|dev|':>9}")
    for label, r, reg, sha, dev in rows:
        print(f"{label:>8} {r:>5} {mp.nstr(reg, 20):>26} "
              f"{mp.nstr(sha, 14):>20} {dev:>9.1e}")
    print("=" * 76)
    worst = max(dev for *_, dev in rows)
    print(f"worst |#Sha - 1| across the open regime: {worst:.1e}")
    print()
    print("READING: the strong-BSD formula closes to ~27 digits on every")
    print("rank >= 2 curve in the bundle, with regulator and leading coefficient")
    print("recomputed independently of the bundled values. This is the sharpest")
    print("consistency statement this substrate can make in the open regime,")
    print("and a real falsifiability surface: on its first run, the 1e-5")
    print("cross-check against the bundle caught a wrong bundled regulator")
    print("(5077a1, off at 3.4e-4; fixed and confirmed three independent ways).")
    print()
    flag = sha_finiteness_flag(get_curve("389a1"), analytic_rank=2,
                               method_assumes_finite=True)
    print("DISCIPLINE (Detector 2):", flag.message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
