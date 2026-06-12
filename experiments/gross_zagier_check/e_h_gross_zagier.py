"""Experiment (h): the Gross-Zagier formula verified numerically, both sides.

Experiment (e) ran the Heegner machine and watched WHERE it dies (rank >= 2).
This experiment measures WHAT the machine outputs where it lives: the exact
Gross-Zagier identity that powers the only proven BSD regime,

    L'(E/K, 1) = ||omega||^2 hhat_K(y_K) / (u^2 sqrt(|D|)),

for E/Q of analytic rank 1 and K = Q(sqrt(D)) a Heegner field. Every factor
is computed independently on our substrate and the two sides are compared to
high precision:

  ANALYTIC SIDE.  L(E/K, s) = L(E, s) L(E_D, s), so with w(E) = -1 (which
  forces L(E, 1) = 0) the derivative collapses to the product of two numbers
  this codebase already knows how to compute:
      L'(E/K, 1) = L'(E, 1) * L(E_D, 1),
  the first by the w = -1 closed form (experiment g), the second by the
  closed-form central value of the quadratic twist E_D (same machinery that
  scanned the twist family, conductor N D^2, a_p inherited times chi_D).

  HEIGHT SIDE.  The same Heegner-point code as experiment (e): CM points on
  X_0(N) summed through the modular parametrization phi(tau) = sum a_n/n q^n,
  traced to E(Q), rationalized EXACTLY, and the canonical height computed to
  working precision with the new sigma-function local-height machinery
  (analytic_height.py; the 1e-5 doubling limit is not good enough here).
  These curves are torsion-free, so the trace P satisfies P = 2 y_K and
      hhat_K(y_K) = 2 hhat_Q(y_K) = hhat_Q(P) / 2,
  while ||omega||^2 = 2 Vol(C/Lambda) and u = 1 (D < -4). The identity
  under test, in directly computed quantities:

      L'(E, 1) * L(E_D, 1)  =  Vol(Lambda) * hhat_Q(P) / sqrt(|D|).

  Manin constant 1 for these optimal curves (proven for this range), so no
  hidden rational factor.

Why this matters for the program: Gross-Zagier is the quantitative form of
the rank-1 ceiling. The check turns "the machine's output factors through
L'(E/K, 1)" from a theorem citation into a measured equality on 37a1 (two
different Heegner fields), 43a1 and 53a1 (rhombic lattices, Delta < 0). The
boundary case is then exact: on 389a1 / 5077a1 both sides are 0 = 0, which
is experiment (e)'s torsion output restated as an equation. A rank >= 2
construction must produce a point whose height is NOT this number.

Run from the repo root (about a minute):
    python -m experiments.gross_zagier_check.e_h_gross_zagier
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import List, Tuple

import mpmath as mp

from experiments._shared import get_curve, parity_detector
from experiments._shared.analytic_height import SigmaLattice, canonical_height_sigma
from experiments._shared.rational_points import canonical_height, lift_x, on_curve
from experiments.heegner_ceiling.e_e_heegner_ceiling import (
    heegner_representatives,
    is_fundamental,
    phi,
)
from experiments.twist_parity.e_g_twist_parity import (
    TwistedCurve,
    central_sums,
    kronecker,
    l_prime_closed,
)

# (label, number of Heegner discriminants to test): 37a1 gets two fields to
# show the identity is about (E, K) jointly, not a single lucky constant.
RUNS: List[Tuple[str, int]] = [("37a1", 2), ("43a1", 1), ("53a1", 1)]

RATIO_TOL = mp.mpf("1e-12")


def cheapest_discriminants(N: int, count: int):
    """The `count` cheapest admissible Heegner discriminants for prime N.

    Same admissibility and cost metric as experiment (e)'s pick_discriminant,
    but keeping the top `count` so 37a1 can be checked over two fields.
    """
    ranked = []
    for D in range(-7, -600, -1):
        if not is_fundamental(D) or D in (-3, -4):
            continue
        if gcd(D, 2 * N) != 1:
            continue
        if kronecker(D, N) != 1:
            continue
        reps = heegner_representatives(N, D)
        cost = float(sum(A for A, _ in reps) / mp.sqrt(-D))
        ranked.append((cost, D, reps))
    ranked.sort()
    assert len(ranked) >= count, f"not enough Heegner discriminants for N={N}"
    return [(D, reps) for _, D, reps in ranked[:count]]


def rationalize(x, max_den: int = 10 ** 12) -> Fraction:
    """Exact Fraction from an mpf known to high precision (not via float)."""
    scaled = Fraction(int(mp.nint(x * mp.mpf(10) ** 20)), 10 ** 20)
    xr = scaled.limit_denominator(max_den)
    err = abs(x - mp.mpf(xr.numerator) / xr.denominator)
    assert err < mp.mpf("1e-15") * max(1, abs(x)), \
        f"rationalization failed: x = {x}"
    return xr


def heegner_trace_point(E, L: SigmaLattice, D: int, reps):
    """Run the Heegner machine, return (P exact, z polished, q-terms used)."""
    yK = mp.mpc(0)
    terms = 0
    for A, B in reps:
        zi, n_used = phi(E, A, B, D)
        yK += zi
        terms = max(terms, n_used)

    # w = -1 and trivial torsion force y_K into E(Q): the anti-trace must be
    # a lattice point. This is the eigenvalue structure, checked, not cited.
    da, db = L.reduce(yK - mp.conj(yK))
    assert abs(da) < 1e-8 and abs(db) < 1e-8, \
        f"{E.label}, D={D}: anti-trace is not a lattice point"

    a, b = L.reduce(yK + mp.conj(yK))
    assert abs(a) > 1e-4 or abs(b) > 1e-4, \
        f"{E.label}, D={D}: trace is torsion; expected non-torsion in rank 1"
    zz = a * L.w1 + b * L.w2
    x = mp.re(L.x_of_z(zz))
    P = lift_x(E, rationalize(x))
    assert P is not None and on_curve(E, P), \
        f"{E.label}, D={D}: trace did not rationalize to a point on E"

    # polish z against the exact x-coordinate (kills phi truncation error)
    x_exact = mp.mpf(P[0].numerator) / P[0].denominator
    try:
        zz = mp.findroot(lambda t: L.x_of_z(t) - x_exact, zz)
    except Exception:
        pass  # unpolished z is already good to ~1e-20
    return P, zz, terms


def main():
    mp.mp.dps = 25

    print("Numerical Gross-Zagier: L'(E,1) L(E_D,1) = Vol(Lambda) hhat(P) / sqrt|D|")
    print("(P = trace of the Heegner point y_K to E(Q); P = 2 y_K, torsion-free)")
    print()

    rows = []
    for label, n_disc in RUNS:
        E = get_curve(label)
        N = E.conductor
        assert E.root_number == -1 and E.rank == 1 and E.torsion_order == 1
        L = SigmaLattice(E)

        # analytic L'(E, 1): closed form, cross-checked against the AFE once
        lp = l_prime_closed(E)
        lp_afe = E.L_derivative_at_one(1)
        assert abs(lp - lp_afe) < mp.mpf("1e-15"), \
            f"{label}: closed-form L' disagrees with the AFE"

        for D, reps in cheapest_discriminants(N, n_disc):
            h = len(reps)
            P, zz, terms = heegner_trace_point(E, L, D, reps)

            hh = canonical_height_sigma(E, P, zz, L)
            assert abs(hh - canonical_height(E, P)) < 5e-4, \
                f"{label}: sigma height disagrees with doubling limit"

            Ed = TwistedCurve(E, D)
            assert Ed.root_number == +1, "Heegner hypothesis must force w_D = +1"
            lD, fricke = central_sums(Ed)
            assert abs(fricke) > 1e-6, "Fricke check: w_D = +1 needs F != 0"

            lhs = lp * lD
            rhs = L.vol * hh / mp.sqrt(mp.mpf(-D))
            ratio = lhs / rhs
            m2 = hh / (4 * E.regulator)  # hhat(y_K) = m^2 Reg with m the index
            print(f"--- {label}, K = Q(sqrt({D})), h(D) = {h}, "
                  f"{terms} q-terms ---")
            print(f"  P = ({P[0]}, {P[1]})  EXACT, hhat(P) = {mp.nstr(hh, 18)}")
            print(f"  L'(E,1)  = {mp.nstr(lp, 18)}")
            print(f"  L(E_D,1) = {mp.nstr(lD, 18)}")
            print(f"  L'(E/K,1) analytic   = {mp.nstr(lhs, 18)}")
            print(f"  Vol hhat / sqrt|D|   = {mp.nstr(rhs, 18)}")
            print(f"  ratio - 1 = {mp.nstr(ratio - 1, 3)}   "
                  f"Heegner index m = {mp.nstr(mp.sqrt(m2), 8)}")
            print()
            rows.append((label, D, h, float(abs(ratio - 1)), float(mp.sqrt(m2))))

    print("=" * 74)
    print(f"{'curve':>7} {'D':>6} {'h(D)':>5} {'|ratio - 1|':>14} {'index m':>9}")
    for label, D, h, dev, m in rows:
        print(f"{label:>7} {D:>6} {h:>5} {dev:>14.2e} {m:>9.4f}")
    print("=" * 74)
    worst = max(dev for _, _, _, dev, _ in rows)
    assert worst < float(RATIO_TOL), \
        f"Gross-Zagier check FAILED: worst deviation {worst}"
    print(f"PASS: Gross-Zagier verified on {len(rows)} (E, K) pairs, "
          f"worst |ratio - 1| = {worst:.2e}")
    print()
    print("READING: the proven regime is now a measured EQUATION, not a cited")
    print("theorem. The entire output of the Heegner machine (the height of the")
    print("one point it makes) is one first derivative of one L-function. On the")
    print("rank >= 2 side the same equation reads 0 = 0 (experiment e: torsion")
    print("out, L'(E/K,1) = 0): correct, and perfectly uninformative. That is")
    print("the rank-1 ceiling stated quantitatively.")
    print()
    verdict = parity_detector(claims_full_rank=True, uses_only_root_number=True)
    print("DISCIPLINE (Detector 1):", verdict.message)
    print()
    print("CONSEQUENCE FOR THE SPEC (Research Direction 01): a rank >= 2 object")
    print("must output data whose size is NOT proportional to L'(E/K, 1). The")
    print("natural conjectural target has size proportional to a HIGHER Taylor")
    print("coefficient (regulator of a rank-2 lattice vs square of one height),")
    print("so any candidate passing this experiment's machinery unchanged is")
    print("automatically suspect: it factors through the one-derivative bottleneck.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
