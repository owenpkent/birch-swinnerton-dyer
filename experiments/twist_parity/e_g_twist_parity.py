"""Experiment (g): a quadratic twist family, and exactly where parity goes blind.

Detector 1 (parity-only) says: the root number w fixes the rank mod 2 and
nothing more, so w cannot separate rank 0 from rank 2, or rank 1 from rank 3.
This experiment turns that abstract warning into DATA. Take a base curve E
and scan its quadratic twists E_d over fundamental d (squarefree, d = 1 mod 4,
coprime to 2N, so the twisted conductor is N d^2):

  - the root number transforms by w(E_d) = chi_d(-N) w(E), a closed formula;
  - the central value has a closed form needing no AFE machinery:
        w = +1:  L(E_d, 1)  = 2 sum_n (a_n(E_d)/n) exp(-2 pi n / sqrt(N d^2))
        w = -1:  L'(E_d, 1) = 2 sum_n (a_n(E_d)/n) E1(2 pi n / sqrt(N d^2))
    (E1 the exponential integral; both standard, e.g. Cremona, Algorithms).

The interesting rows are the ones where PARITY SAYS EVEN but the L-value
VANISHES: those twists have analytic rank >= 2 (confirmed by L''(1) != 0 via
the full AFE), i.e. they sit in the open BSD regime, and the root number is
structurally incapable of seeing them. Detector 1, exhibited in a family.
Rows with w = -1 and L'(1) = 0 are the rank >= 3 analogue.

Self-validation built in (per the repo discipline):
  - the Kronecker symbol is checked against the Euler criterion;
  - the closed forms reproduce L(11a1, 1) = 0.2538418 and
    L'(37a1, 1) = 0.3059998 = Omega * Reg (strong BSD with Sha = 1);
  - the root-number formula is cross-checked for EVERY twist against the
    Fricke fixed-point test: w = -1 forces f(i/sqrt(N_d)) = 0, so
    F = sum a_n exp(-2 pi n / sqrt(N_d)) vanishes iff w = -1.

Run from the repo root:
    python -m experiments.twist_parity.e_g_twist_parity
"""

from __future__ import annotations

import math

import mpmath as mp

from experiments._shared import EllipticCurve, get_curve, parity_detector

VANISH_TOL = 1e-8
THETA_TOL = 1e-6


# --------------------------------------------------------------------------
# Kronecker symbol (a/n), with the Euler-criterion self-test
# --------------------------------------------------------------------------

def kronecker(a: int, n: int) -> int:
    if n == 0:
        return 1 if abs(a) == 1 else 0
    if a % 2 == 0 and n % 2 == 0:
        return 0
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    k = 1
    if v % 2 == 1 and a % 8 not in (1, 7):
        k = -1
    if n < 0:
        n = -n
        if a < 0:
            k = -k
    a %= n
    while a:
        v = 0
        while a % 2 == 0:
            a //= 2
            v += 1
        if v % 2 == 1 and n % 8 in (3, 5):
            k = -k
        if a % 4 == 3 and n % 4 == 3:
            k = -k
        a, n = n % a, a
    return k if n == 1 else 0


def _selftest_kronecker():
    for p in (3, 5, 7, 11, 13, 37, 389):
        for a in range(1, 25):
            if a % p == 0:
                continue
            euler = pow(a, (p - 1) // 2, p)
            expect = 1 if euler == 1 else -1
            assert kronecker(a, p) == expect, (a, p)


# --------------------------------------------------------------------------
# The twisted curve: a_p inherited from the base curve times chi_d
# --------------------------------------------------------------------------

class TwistedCurve(EllipticCurve):
    """Quadratic twist E_d with coefficients pulled from the base curve.

    a_p(E_d) = chi_d(p) a_p(E) at p not dividing d, and 0 at p | d (additive
    reduction). Pulling a_p from the base curve's point counts avoids ever
    counting points on a non-minimal twisted model (which would be wrong at
    the model's spurious bad primes).

    The a_invariants stored here are the integral twisted model
    Y^2 = X^3 + b2 d X^2 + 8 b4 d^2 X + 16 b6 d^3, used only for rational
    point search (heights are model-independent); the L-machinery uses only
    conductor, root number and the inherited a_p.
    """

    def __init__(self, base: EllipticCurve, d: int):
        a1, a2, a3, a4, a6 = base.a_invariants
        b2 = a1 * a1 + 4 * a2
        b4 = 2 * a4 + a1 * a3
        b6 = a3 * a3 + 4 * a6
        super().__init__(
            label=f"{base.label}x{d}",
            a_invariants=[0, b2 * d, 0, 8 * b4 * d * d, 16 * b6 * d ** 3],
            conductor=base.conductor * d * d,
            root_number=kronecker(d, -base.conductor) * base.root_number,
        )
        self.base = base
        self.d = d

    def a_p(self, p: int) -> int:
        if p in self._ap_cache:
            return self._ap_cache[p]
        ap = 0 if self.d % p == 0 else kronecker(self.d, p) * self.base.a_p(p)
        self._ap_cache[p] = ap
        return ap


# --------------------------------------------------------------------------
# Closed-form central values (no AFE, no gammainc: fast family scans)
# --------------------------------------------------------------------------

def _n_max(N: int) -> int:
    x0 = 2 * mp.pi / mp.sqrt(N)
    return int((mp.mp.dps + 4) * mp.log(10) / x0) + 20


def central_sums(E):
    """(L(E,1) if w=+1 else exact 0, F) with F the Fricke fixed-point value.

    L(E, 1) = (1 + w) sum (a_n/n) e^{-2 pi n / sqrt N}; the sum itself is
    returned scaled by 2 for the w = +1 case. F = sum a_n e^{-2 pi n/sqrt N}
    vanishes iff w = -1 (weight-2 Fricke eigenvalue), our root-number check.
    """
    N = E.conductor
    u = mp.exp(-2 * mp.pi / mp.sqrt(N))
    s_weighted = mp.mpf(0)
    s_plain = mp.mpf(0)
    upow = mp.mpf(1)
    for n in range(1, _n_max(N) + 1):
        upow *= u
        an = E.a_n(n)
        if an:
            s_weighted += mp.mpf(an) / n * upow
            s_plain += an * upow
    return 2 * s_weighted, s_plain


def l_prime_closed(E):
    """L'(E, 1) = 2 sum (a_n/n) E1(2 pi n / sqrt N), valid when w = -1."""
    N = E.conductor
    x0 = 2 * mp.pi / mp.sqrt(N)
    total = mp.mpf(0)
    for n in range(1, _n_max(N) + 1):
        an = E.a_n(n)
        if an:
            total += mp.mpf(an) / n * mp.e1(x0 * n)
    return 2 * total


def fundamental_twists(N: int, bound: int):
    """Fundamental d = 1 mod 4, squarefree, coprime to 2N, 1 < |d| <= bound."""
    out = []
    for d in range(-bound, bound + 1):
        if d in (0, 1) or d % 4 != 1:
            continue
        if math.gcd(d, 2 * N) != 1:
            continue
        ad = abs(d)
        if any(ad % (p * p) == 0 for p in range(2, int(ad ** 0.5) + 1)):
            continue
        out.append(d)
    return sorted(out, key=abs)


# --------------------------------------------------------------------------
# The scan
# --------------------------------------------------------------------------

def scan_base(label: str, bound: int):
    base = get_curve(label)
    N = base.conductor
    print(f"=== twists of {label} (N = {N}, w = {base.root_number:+d}, "
          f"rank {base.rank}), fundamental d = 1 mod 4, |d| <= {bound} ===")
    counts = {0: 0, 1: 0}
    blind = []   # (d, kind) rows parity cannot classify
    rows = 0
    for d in fundamental_twists(N, bound):
        Ed = TwistedCurve(base, d)
        L1, F = central_sums(Ed)
        w_theta = -1 if abs(F) < THETA_TOL else 1
        assert w_theta == Ed.root_number, (
            f"root-number formula vs Fricke test disagree at d={d}: "
            f"formula {Ed.root_number}, |F|={float(abs(F)):.2e}"
        )
        rows += 1
        if Ed.root_number == 1:
            if abs(L1) < VANISH_TOL:
                blind.append((d, 2, Ed))
                print(f"  d={d:>5}  w=+1  L(1)={float(L1):>12.8f}  "
                      f"<-- VANISHES: analytic rank >= 2, PARITY-BLIND")
            else:
                counts[0] += 1
        else:
            Lp = l_prime_closed(Ed)
            if abs(Lp) < VANISH_TOL:
                blind.append((d, 3, Ed))
                print(f"  d={d:>5}  w=-1  L'(1)={float(Lp):>11.8f}  "
                      f"<-- VANISHES: analytic rank >= 3, parity says only 'odd'")
            else:
                counts[1] += 1
    print(f"  scanned {rows} twists: analytic rank 0: {counts[0]}, "
          f"rank 1: {counts[1]}, parity-blind (>= 2): {len(blind)}")
    print()
    return blind


def confirm(Ed: TwistedCurve, kind: int):
    """Confirm a flagged twist with the full AFE: next derivative nonzero."""
    old = mp.mp.dps
    mp.mp.dps = 13
    try:
        order = kind  # rank >= 2 candidate: check L''; rank >= 3: check L'''
        val = Ed.L_derivative_at_one(order)
        below = [float(abs(Ed.L_derivative_at_one(k))) for k in range(order)]
    finally:
        mp.mp.dps = old
    return below, val


def main():
    mp.mp.dps = 15
    _selftest_kronecker()

    # closed-form self-checks against strong-BSD values in the proven regime
    E11 = get_curve("11a1")
    L1, _ = central_sums(E11)
    expect_11 = E11.real_period * E11.tamagawa_product / E11.torsion_order ** 2
    assert abs(float(L1) - expect_11) < 1e-6, (float(L1), expect_11)
    E37 = get_curve("37a1")
    Lp = l_prime_closed(E37)
    expect_37 = E37.real_period * E37.regulator
    assert abs(float(Lp) - expect_37) < 1e-6, (float(Lp), expect_37)
    print("SELF-CHECKS PASS: kronecker == Euler criterion; "
          f"L(11a1,1) = {float(L1):.7f} (= Omega c / tors^2 = {expect_11:.7f}); "
          f"L'(37a1,1) = {float(Lp):.7f} (= Omega Reg = {expect_37:.7f})")
    print()

    blind_all = []
    blind_all += scan_base("11a1", 200)
    blind_all += scan_base("37a1", 150)

    # confirm the flagged twists with the heavyweight AFE machinery
    print("=== confirmation of parity-blind rows (full AFE, derivative test) ===")
    for d, kind, Ed in blind_all[:4]:
        below, val = confirm(Ed, kind)
        below_s = ", ".join(f"|L^({k})(1)|={b:.2e}" for k, b in enumerate(below))
        print(f"  {Ed.label} (N={Ed.conductor}): {below_s}, "
              f"L^({kind})(1) = {float(val.real):.5f} != 0")
        print(f"    => analytic rank EXACTLY {kind} (numerical): "
              f"open BSD regime reached by a twist, invisible to the root number")
    if len(blind_all) > 4:
        print(f"  (+ {len(blind_all) - 4} more flagged twists left at screen level)")
    print()

    # the detector, fired on the thing the scan exhibits
    verdict = parity_detector(claims_full_rank=True, uses_only_root_number=True)
    print("DISCIPLINE (Detector 1):", verdict.message)
    print()
    print("READING: in this family the root number classifies most twists, and")
    print("a method built on w alone would silently call every flagged row 'rank 0'")
    print("(or 'rank 1'). The vanishing central value is invisible to parity: the")
    print("rank >= 2 regime starts exactly where the root number's information ends.")
    print("Goldfeld's minimalist conjecture says rank 0 and 1 each have density 1/2")
    print("in such families; the flagged rows are the density-zero exceptional set")
    print("where all of BSD's open content lives.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
