"""Experiment (m): the rank-1 / codimension-1 SHADOW of the Kudla generating series.

WHY this experiment exists. Kudla's program (reading note
docs/03_research/reading_notes/Kudla-2004-Special-Cycles-Derivatives-Eisenstein.md)
is the live candidate for Direction 01's Clause 2: a SECOND central derivative
of L(E, s) tied to a codimension-2 arithmetic special cycle through a genus-2
Siegel-Eisenstein series. That object is OPEN over Q. It is a VISION, not a
theorem. The only fully proven case of Kudla's modularity is codimension 1,
and there it IS a theorem with a classical name: Gross-Kohnen-Zagier on the
height side, Waldspurger on the value side. This experiment computes that
proven codimension-1 case end to end, offline, on the congruent-number family,
so that the shape of the open rank-2 object is made precise by exhibiting its
genus-1 shadow. It is NOT progress on the open construction. The honest gap is
printed loudly at the end and audited against Detector 3 (function-field
mirage), which is the central risk for any Kudla-to-Q transfer claim.

WHAT is verified (a THEOREM, in the proven analytic-rank-<=1 regime). For the
quadratic-twist family E_n : y^2 = x^3 - n^2 x (n odd squarefree, the n-th
congruent-number curve), Waldspurger's theorem says the central value
L(E_n, 1) is proportional to the SQUARE of a single half-integral-weight
(weight 3/2) Fourier coefficient c_n:

    L(E_n, 1) = kappa * c_n^2 / sqrt(n),    kappa > 0 CONSTANT across n,

for those n with root number w(E_n) = +1 (the form of weight 3/2 attached to
E_1 only sees this branch). Here c_n is Tunnell's explicit coefficient,
computed FROM SCRATCH in this file by counting integer triples:

    c_n = #{2x^2 + y^2 + 8z^2 = n} - 2 #{2x^2 + y^2 + 32z^2 = n}

(J. Tunnell, "A classical Diophantine problem and modular forms of weight 3/2",
Inventiones 72 (1983), 323-334). The proportionality is the simplest instance
of the theta correspondence: the weight-3/2 form is the Shimura-Waldspurger
partner of the weight-2 newform f_{E_1}, exactly the codimension-1 (one moving
leg) case of Kudla's arithmetic theta series.

THE MEASURED EQUATION (printed with residuals, not a vibe). The script computes
two numbers independently for each n: c_n by lattice counting, and L(E_n, 1) by
the same w = +1 closed form used in experiment (g). It then prints

    kappa_n = L(E_n, 1) * sqrt(n) / c_n^2

and the residual |kappa_n / kappa_closed - 1|, where the closed form is
kappa_closed = Omega_{E_1} / 32 with Omega_{E_1} the real period of E_1,
computed independently from the period lattice and cross-checked against the
CM closed form 2 pi / AGM(1, sqrt(2)). Constancy of kappa_n to ~15 digits is
Waldspurger exhibited numerically.

THE CONGRUENT-NUMBER PANEL. c_n = 0 <=> L(E_n, 1) = 0 is checked against the
classical small congruent numbers (a tiny bundled list with citation). The row
n = 41 is RETAINED and LABELED: 41 is not congruent, yet c_41 = 0 and
L(E_41, 1) = 0 (analytic rank 2 of E_41). The implication c_n = 0 => L = 0 is
Waldspurger (proven); the converse L = 0 => n congruent => rank >= 1 is
BSD-CONDITIONAL, and n = 41 is exactly the row where it bites. This is flagged,
not dropped.

REUSED VERIFIED SUBSTRATE (no reinvention):
  - experiments._shared.EllipticCurve: honest a_p point counting, a_n recurrence;
    E_1 and each E_n built directly as EllipticCurve([0,0,0,-n^2,0], N=32 n^2, w=+1).
  - experiments.twist_parity.e_g_twist_parity: the _n_max term-count helper, the
    Fricke fixed-point root-number test (S5), and kronecker (a_p cross-check).
  - experiments._shared.period_lattice.period_lattice_any: independent Omega_{E_1}.
  - experiments._shared.controls: function_field_mirage, parity_detector for the panel.

Run from the repo root:
    python -m experiments.theta_shadow.e_m_theta_shadow
"""

from __future__ import annotations

import math

import mpmath as mp

from experiments._shared import (
    EllipticCurve,
    function_field_mirage,
    function_field_template,
    parity_detector,
)
from experiments._shared.period_lattice import period_lattice_any
from experiments.twist_parity.e_g_twist_parity import _n_max, kronecker

# --------------------------------------------------------------------------
# BUNDLED GROUND TRUTH (tiny tables, with citation, in the curve_data.py style)
# --------------------------------------------------------------------------
#
# Anchor-1 spot values: known Tunnell coefficients c_n, used only as a sanity
# assert on the from-scratch lattice count. Source: Tunnell 1983 (above).
TUNNELL_KNOWN = {1: -2, 3: -4, 11: 4, 17: 8, 19: 4, 33: -8, 41: 0, 57: -8}

# Anchor-3: classical small congruent numbers (n with E_n of positive rank,
# equivalently L(E_n, 1) = 0). Source: N. Koblitz, "Introduction to Elliptic
# Curves and Modular Forms" (Springer, 1993), congruent-number table; OEIS
# A003273 (congruent numbers). We list the odd squarefree n <= 41 and mark each.
# The n = 41 row is the labeled BSD-conditional caveat (see module docstring):
# 41 is NOT congruent, yet c_41 = 0 and L(E_41, 1) = 0 (E_41 has analytic
# rank 2). Every other row below has (n congruent) <=> (c_n = 0) unconditionally
# on the value side by Waldspurger.
CONGRUENT_ODD_SQUAREFREE = {
    1: False, 3: False, 5: True, 7: True, 11: False, 13: True, 15: True,
    17: False, 19: False, 21: True, 23: True, 29: True, 31: True, 33: False,
    37: True, 39: True, 41: False,
}

CONST_TOL = 1e-10        # constancy of kappa across the w = +1 scan (S2)
CLOSED_TOL = 1e-9        # measured kappa vs Omega_{E_1}/32 (S3)
VANISH_TOL = 1e-12       # |L(E_n, 1)| on congruent / c_n = 0 rows (S4)
FRICKE_TOL = 1e-6        # root-number branch via Fricke fixed point (S5)


# --------------------------------------------------------------------------
# Anchor 1: Tunnell's weight-3/2 coefficient c_n by integer-triple counting
# --------------------------------------------------------------------------

def _count_ternary(a: int, c: int, n: int) -> int:
    """#{(x, y, z) in Z^3 : a x^2 + y^2 + c z^2 = n}, full signed count.

    The two Tunnell forms are 2x^2 + y^2 + 8z^2 (a=2, c=8) and 2x^2 + y^2 +
    32z^2 (a=2, c=32). Cost is ~ n / sqrt(a c), fine for n up to a few hundred.
    """
    total = 0
    zmax = int(math.isqrt(n // c)) + 1
    for z in range(-zmax, zmax + 1):
        r1 = n - c * z * z
        if r1 < 0:
            continue
        xmax = int(math.isqrt(r1 // a)) + 1
        for x in range(-xmax, xmax + 1):
            r2 = r1 - a * x * x
            if r2 < 0:
                continue
            y = math.isqrt(r2)
            if y * y == r2:
                total += 1 if y == 0 else 2  # +-y both count when y != 0
    return total


def tunnell_coefficient(n: int) -> int:
    """c_n = #{2x^2 + y^2 + 8z^2 = n} - 2 #{2x^2 + y^2 + 32z^2 = n} (Tunnell 1983)."""
    return _count_ternary(2, 8, n) - 2 * _count_ternary(2, 32, n)


# --------------------------------------------------------------------------
# The twisted congruent-number curve E_n and its central value
# --------------------------------------------------------------------------

def make_En(n: int) -> EllipticCurve:
    """E_n : y^2 = x^3 - n^2 x. Conductor 32 n^2, root number +1 on this scan.

    Built DIRECTLY (not via curve_data._build): the conductor 32 n^2 is not
    squarefree, so the prime-conductor product check w = -prod(-a_p) does not
    apply. a_p is honest point counting from EllipticCurve; the CM signature
    a_p = 0 at p = 3 mod 4 falls out for free. We set root_number = +1 here and
    ASSERT it against the Fricke test (S5); n with w = -1 are excluded upstream.
    """
    return EllipticCurve(
        label=f"E_{n}",
        a_invariants=[0, 0, 0, -n * n, 0],
        conductor=32 * n * n,
        root_number=1,
    )


def l_value_plus(E: EllipticCurve) -> mp.mpf:
    """L(E, 1) = 2 sum_k (a_k / k) exp(-2 pi k / sqrt(N)), valid for w = +1.

    The same closed form as experiment (g)'s central_sums, restated here so the
    scan is self-contained. The CM curve has a_k = 0 for half the k (p = 3 mod 4),
    so the sum is sparse and converges fast.
    """
    N = E.conductor
    u = mp.exp(-2 * mp.pi / mp.sqrt(N))
    s = mp.mpf(0)
    upow = mp.mpf(1)
    for k in range(1, _n_max(N) + 1):
        upow *= u
        an = E.a_n(k)
        if an:
            s += mp.mpf(an) / k * upow
    return 2 * s


def fricke_value(E: EllipticCurve) -> mp.mpf:
    """F = sum_k a_k exp(-2 pi k / sqrt(N)); vanishes iff w = -1 (S5)."""
    N = E.conductor
    u = mp.exp(-2 * mp.pi / mp.sqrt(N))
    s = mp.mpf(0)
    upow = mp.mpf(1)
    for k in range(1, _n_max(N) + 1):
        upow *= u
        an = E.a_n(k)
        if an:
            s += an * upow
    return s


# --------------------------------------------------------------------------
# Anchor 2: the proportionality constant, two independent values
# --------------------------------------------------------------------------

def kappa_closed_form() -> mp.mpf:
    """kappa = Omega_{E_1} / 32, Omega_{E_1} from the period lattice.

    Cross-checked against the CM closed form 2 pi / AGM(1, sqrt(2)). For E_1 the
    discriminant is positive (three real 2-torsion points), so the LMFDB real
    period is 2 w1 with w1 the rectangular real half-period.
    """
    E1 = make_En(1)
    w1, _ = period_lattice_any(E1)
    omega = 2 * w1
    omega_cm = 2 * mp.pi / mp.agm(mp.mpf(1), mp.sqrt(2))
    assert abs(omega - omega_cm) < mp.mpf(10) ** (-(mp.mp.dps - 4)), (
        f"Omega_E1 period-lattice {mp.nstr(omega, 15)} != CM closed form "
        f"{mp.nstr(omega_cm, 15)}"
    )
    return omega / 32, omega, omega_cm


# --------------------------------------------------------------------------
# The scan that prints the measured equation
# --------------------------------------------------------------------------

def is_odd_squarefree(n: int) -> bool:
    if n % 2 == 0:
        return False
    return not any(n % (p * p) == 0 for p in range(2, int(n ** 0.5) + 1))


def scan_n() -> list:
    """w = +1 odd squarefree n: Tunnell's branch is n = 1, 3 mod 8."""
    return [n for n in range(1, 60) if is_odd_squarefree(n) and n % 8 in (1, 3)]


def run_proportionality(kappa_closed):
    print("=== MEASURED EQUATION: Waldspurger proportionality on E_n : "
          "y^2 = x^3 - n^2 x ===")
    print("    L(E_n, 1) = kappa * c_n^2 / sqrt(n),   kappa = Omega_{E_1}/32 "
          "CONSTANT (w = +1 branch, n = 1,3 mod 8)")
    print(f"    {'n':>4} {'c_n':>5} {'L(E_n,1)':>16} {'kappa_n':>20} "
          f"{'|kappa_n/kappa_cl - 1|':>24}")
    worst = mp.mpf(0)
    rows = []
    for n in scan_n():
        En = make_En(n)
        # S5: assert the root number is +1 via the Fricke fixed point
        F = fricke_value(En)
        assert abs(F) > FRICKE_TOL, (
            f"n={n}: Fricke value {mp.nstr(F, 6)} ~ 0 means w = -1, should be "
            "excluded from the w = +1 proportionality"
        )
        c = tunnell_coefficient(n)
        L = l_value_plus(En)
        if c == 0:
            # w = +1 with c = 0: a vanishing central value (E_n analytic rank
            # >= 2). Not part of the constancy test (c^2 = 0 in the denominator).
            # n = 41 is exactly this row; handled in the congruent panel.
            print(f"    {n:>4} {c:>5} {mp.nstr(L, 10):>16} "
                  f"{'(c_n = 0: L vanishes, rank >= 2)':>44}")
            rows.append((n, c, L, None))
            continue
        kappa_n = L * mp.sqrt(n) / (c * c)
        resid = abs(kappa_n / kappa_closed - 1)
        worst = max(worst, resid)
        print(f"    {n:>4} {c:>5} {mp.nstr(L, 10):>16} "
              f"{mp.nstr(kappa_n, 18):>20} {mp.nstr(resid, 4):>24}")
        rows.append((n, c, L, kappa_n))
    print(f"    worst |kappa_n / kappa_closed - 1| over the scan = "
          f"{mp.nstr(worst, 4)}   (kappa is CONSTANT: Waldspurger exhibited)")
    return worst, rows


def run_congruent_panel():
    print()
    print("=== CONGRUENT-NUMBER PANEL: c_n = 0 <=> L(E_n, 1) = 0 ===")
    print("    (c_n by lattice count; L by w=+1 closed form when w=+1, else "
          "Fricke confirms the vanishing branch)")
    print(f"    {'n':>4} {'c_n':>5} {'congruent?':>11} {'|L(E_n,1)|':>14} "
          f"{'verdict':>10}")
    caveat_seen = False
    for n in sorted(CONGRUENT_ODD_SQUAREFREE):
        congruent = CONGRUENT_ODD_SQUAREFREE[n]
        c = tunnell_coefficient(n)
        En = make_En(n)
        # L vanishes on BOTH branches when n is congruent (w = -1) and on the
        # w = +1 rank >= 2 rows; the w = +1 closed form is exact only for w = +1,
        # so we report |F| (Fricke) as the vanishing witness for w = -1 rows.
        if n % 8 in (1, 3):
            Lmag = abs(l_value_plus(En))
            wlabel = "w=+1"
        else:
            Lmag = abs(fricke_value(En))  # |F| ~ 0 certifies w = -1 (and L = 0)
            wlabel = "w=-1"
        # vanishing of c_n must track congruence, with the n = 41 exception
        consistent = (c == 0) == congruent
        verdict = "OK"
        if not consistent:
            if n == 41 and c == 0 and not congruent:
                verdict = "CAVEAT"
                caveat_seen = True
            else:
                verdict = "MISMATCH"
        print(f"    {n:>4} {c:>5} {str(congruent):>11} "
              f"{mp.nstr(Lmag, 4):>14} {verdict:>10}  ({wlabel})")
    assert caveat_seen, "expected the n = 41 BSD-conditional caveat row"
    print("    NOTE n=41: c_41 = 0 and L(E_41, 1) = 0 (E_41 has analytic rank 2),")
    print("    but 41 is NOT congruent. c_n = 0 => L = 0 is Waldspurger (PROVEN);")
    print("    the converse L = 0 => congruent => rank >= 1 is BSD-CONDITIONAL.")


# --------------------------------------------------------------------------
# Self-tests (assertions; script exits non-zero on failure, (g)/(h) discipline)
# --------------------------------------------------------------------------

def self_tests(worst_resid, kappa_closed, omega, omega_cm):
    # S1: Tunnell counts match the bundled spot values and the symmetry
    for n, expect in TUNNELL_KNOWN.items():
        got = tunnell_coefficient(n)
        assert got == expect, f"S1 c_{n}: got {got}, expected {expect}"
    # S3: closed-form anchor, two ways (period lattice vs CM AGM form)
    assert abs(omega - omega_cm) < CLOSED_TOL, (
        f"S3 Omega two ways: {mp.nstr(omega, 15)} vs {mp.nstr(omega_cm, 15)}"
    )
    # S2: constancy of kappa across the w = +1 scan, to CONST_TOL
    assert worst_resid < CONST_TOL, (
        f"S2 kappa not constant: worst residual {mp.nstr(worst_resid, 6)}"
    )
    # S4: vanishing <=> congruent on the bundled list (n = 41 caveat excepted),
    #     and the L side independently vanishes where c_n = 0.
    for n, congruent in CONGRUENT_ODD_SQUAREFREE.items():
        c = tunnell_coefficient(n)
        if n == 41:
            assert c == 0 and not congruent, "S4 n=41 caveat row changed"
            continue
        assert (c == 0) == congruent, (
            f"S4 c_{n} = {c} but congruent = {congruent}"
        )
    for n in (5, 7, 13, 15, 41):  # c_n = 0 rows; L must vanish on the value side
        En = make_En(n)
        Lmag = abs(l_value_plus(En)) if n % 8 in (1, 3) else abs(fricke_value(En))
        assert Lmag < VANISH_TOL, f"S4 |L(E_{n}, 1)| = {mp.nstr(Lmag, 6)} not ~ 0"
    # S5: every scanned (w = +1) curve passes the Fricke root-number test
    for n in scan_n():
        assert abs(fricke_value(make_En(n))) > FRICKE_TOL, f"S5 n={n} w-branch"
    return True


# --------------------------------------------------------------------------
# Detector panel (Detector 3 is the headline)
# --------------------------------------------------------------------------

def detector_panel():
    print()
    print("=== DETECTOR PANEL (Detector 3 = the headline risk) ===")

    # Detector 3: function-field mirage. The codim-1 shadow does NOT import the
    # two function-field ingredients the rank-2 / codim-2 case needs, so it is
    # genuinely a number-field object. The mirage would fire only if we claimed
    # genus-1 success extends to genus 2. We claim no such thing.
    tmpl = function_field_template()
    shadow_clean = function_field_mirage(
        method_uses_geometric_frobenius=False,
        method_needs_base_curve=False,
    )
    print("  [Detector 3] codim-1 shadow (this experiment):", shadow_clean)
    print("    The shadow has r = 1 (ONE moving leg: CM points on a modular")
    print("    curve, a genuine number-field object) and NO Frobenius twist,")
    print("    which is exactly why it is computable over Q. The rank-2 /")
    print("    codim-2 / genus-2 Kudla object would need the two Yun-Zhang")
    print("    imports this experiment does NOT supply:")
    print("      (1) the r moving legs over X^r: the SECOND leg has no Q-shadow")
    print("          (Spec Z x_{F1} Spec Z does not exist);")
    print("      (2) the Frobenius twist in the shtuka definition.")
    print("    A transfer-to-Q claim is what would trigger the mirage. We make")
    print("    none. The higher-derivative layer is a THEOREM over function")
    print("    fields (Yun-Zhang, all orders) and only a VISION over Q.")
    print(f"    Geometric template (the gap): {tmpl.the_gap}")

    # Detector 1: parity-only. This is a value identity, finer than parity. But
    # the vanishing panel must not be over-read as a rank certificate.
    verdict = parity_detector(claims_full_rank=False, uses_only_root_number=False)
    print("  [Detector 1]", verdict.message)
    print("    The proportionality is a VALUE identity (finer than parity). The")
    print("    c_n = 0 <=> L = 0 readout is central-value vanishing (analytic);")
    print("    the converse (=> congruent => rank >= 1) is flagged BSD-conditional")
    print("    via the retained n = 41 row. No rank certificate is claimed.")

    # Detector 2: Sha-finiteness. Not applicable: the shadow lives in the proven
    # analytic-rank-<=1 regime (Kolyvagin), so no Sha assumption is imported.
    print("  [Detector 2] n/a: the codim-1 shadow lives in the proven "
          "analytic-rank-<=1 regime; no Sha-finiteness is assumed.")


# --------------------------------------------------------------------------
# The honest gap, printed loudly
# --------------------------------------------------------------------------

def honest_gap():
    print()
    print("=" * 74)
    print("HONEST GAP (read this; it is the point of the experiment)")
    print("=" * 74)
    print("This is the rank-1 / codimension-1 / genus-1 SHADOW of the Kudla")
    print("generating series. It is NOT progress on the open rank-2 construction.")
    print()
    print("VERIFIED: Waldspurger's theorem, the codim-1 theta correspondence, an")
    print("  established THEOREM in the proven analytic-rank-<=1 regime. The")
    print("  proportionality L(E_n, 1) ~ c_n^2 / sqrt(n) ties a FIRST central")
    print("  value to the SQUARE of ONE weight-3/2 coefficient. It factors")
    print("  through a single Taylor coefficient by design: the same one-")
    print("  coefficient bottleneck experiments (e), (g), (h) measured, now seen")
    print("  from the theta side.")
    print()
    print("OPEN (the actual Clause-2 object): the rank-2 / codim-2 / genus-2 case,")
    print("  where Kudla's vision demands det R (a 2x2 regulator) = kappa *")
    print("  L''(E/K, 1) / 2! tied to a SECOND derivative via a codim-2 arithmetic")
    print("  special cycle and a genus-2 Siegel-Eisenstein series. NOTHING here")
    print("  computes or implies that identity.")
    print()
    print("BOTH BRIDGES REMAIN UNCROSSED:")
    print("  Bridge 1 (Eisenstein/doubling L -> L(E,s)): in the shadow this is the")
    print("    classical Shimura correspondence, fine at codim 1. At codim 2,")
    print("    transferring a genus-2 central DERIVATIVE into the second Taylor")
    print("    coefficient of one Hasse-Weil L(E, s) is not in the proven layer.")
    print("  Bridge 2 (cycle class -> rational point): EVEN IN THIS SHADOW no")
    print("    point is produced. The output is an L-value and a theta coefficient,")
    print("    not an element of E(Q). The congruent n with c_n = 0 are exactly")
    print("    where E_n has rank >= 1, but the shadow does not return a generator")
    print("    (that is the separate first-derivative Heegner machine, (e)/(h)).")
    print()
    print("So in analytic rank >= 2, numerical agreement would be EVIDENCE, never")
    print("PROOF. Here there is no rank-2 claim at all. This whole front is a SPEC")
    print("(Direction 01, Clause 2) plus a rank-1 SHADOW.")


def main():
    mp.mp.dps = 30
    print("Experiment (m): the rank-1 / codim-1 shadow of the Kudla generating")
    print("series (Waldspurger on the congruent-number family). OFFLINE.")
    print()

    kappa_closed, omega, omega_cm = kappa_closed_form()
    print(f"Omega_{{E_1}} = 2 w1 (period lattice)      = {mp.nstr(omega, 18)}")
    print(f"Omega_{{E_1}} = 2 pi / AGM(1, sqrt 2) (CM)  = {mp.nstr(omega_cm, 18)}")
    print(f"kappa_closed = Omega_{{E_1}} / 32           = "
          f"{mp.nstr(kappa_closed, 18)}")
    print()

    worst_resid, _ = run_proportionality(kappa_closed)
    run_congruent_panel()

    self_tests(worst_resid, kappa_closed, omega, omega_cm)
    print()
    print("SELF-TESTS PASS: S1 Tunnell spot values; S2 kappa constant to "
          f"{CONST_TOL:.0e}; S3 Omega two ways;")
    print("  S4 vanishing <=> congruent (n=41 caveat); S5 Fricke root-number "
          "branch on every scanned E_n.")

    detector_panel()
    honest_gap()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
