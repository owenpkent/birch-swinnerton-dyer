"""Phase 0 smoke test: does the EllipticCurve / L-function substrate work?

Validates:
  1. Point counting: a_p from #E(F_p) matches known small values (Hasse bound).
  2. Multiplicativity: a_n built from a_p satisfies a_4 = a_2^2 - 2 for a good
     prime 2, and a_6 = a_2 a_3.
  3. L-value at s = 1: rank-0 curve 11a1 has L(E, 1) != 0 (analytic rank 0).
  4. L-vanishing at s = 1: rank-1 curve 37a1 has L(E, 1) ~ 0 (analytic rank 1).
  5. Parity detector: the root number gives the correct rank parity for the
     bundled curves, and the parity-only wrong-approach flag fires.
  6. Sha-finiteness flag: fires (open) for the rank-2 control, clean for rank 1.
  7. Exact functional equation off the center: g(1/(N y)) = w N y^2 g(y) with
     g(y) = sum a_n e^{-2 pi n y}, to 9 digits, for every bundled curve. This
     check sees EVERY coefficient with weight ~ e^{-2 pi n / (2 sqrt N)}, so a
     single wrong a_p (even at p = N, invisible to the central-value tests)
     fails it. It caught nine wrong bundled bad-prime signs on 2026-06-09.
  8. 2-isogeny descent engine (experiment j): on bundled rank-0 curves with a
     rational 2-torsion point the descent upper bound equals the known rank
     (and Sha = 1); on the congruent curve E_34 it gives the rank-2 upper bound;
     every Selmer group has 2-power order; and the rank >= 2 (f) curves have no
     rational 2-torsion, so the elementary descent provably does not start.
"""

from __future__ import annotations

import mpmath as mp

from experiments._shared import (
    get_curve,
    all_curves,
    root_number_parity,
    parity_detector,
    sha_finiteness_flag,
    control_pair,
)


def check(label, ok, info=""):
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {label}{(' - ' + info) if info else ''}")
    return ok


def test_point_counting():
    print("Test 1: a_p from point counting (11a1)")
    E = get_curve("11a1")
    # Known LMFDB a_p for 11a1: a_2=-2, a_3=-1, a_5=1, a_7=-2, a_13=4
    expected = {2: -2, 3: -1, 5: 1, 7: -2, 13: 4}
    ok_all = True
    for p, exp in expected.items():
        got = E.a_p(p)
        ok = got == exp
        # Hasse bound sanity: |a_p| <= 2 sqrt(p)
        hasse = abs(got) <= 2 * (p ** 0.5) + 1e-9
        ok_all = ok_all and check(f"a_{p} = {exp}", ok and hasse, f"got {got}")
    return ok_all


def test_multiplicativity():
    print("Test 2: a_n multiplicativity (11a1)")
    E = get_curve("11a1")
    a2 = E.a_p(2)
    a3 = E.a_p(3)
    # good prime 2: a_4 = a_2^2 - 2 (since a_{p^2} = a_p^2 - p)
    ok4 = check("a_4 = a_2^2 - 2", E.a_n(4) == a2 * a2 - 2, f"got {E.a_n(4)}")
    # a_6 = a_2 * a_3 (coprime)
    ok6 = check("a_6 = a_2 a_3", E.a_n(6) == a2 * a3, f"got {E.a_n(6)}")
    return ok4 and ok6


def test_L_nonzero_rank0():
    print("Test 3: L(E,1) != 0 for rank 0 (11a1)")
    mp.mp.dps = 25
    E = get_curve("11a1")
    val = E.L_value(mp.mpc(1))
    # LMFDB special value L(11a1, 1) ~ 0.2538418609
    ok = abs(val) > 0.1 and abs(val.imag) < 1e-6
    return check("L(11a1, 1) ~ 0.2538 (nonzero, real)", ok, f"got {complex(val)}")


def test_L_zero_rank1():
    print("Test 4: L(E,1) ~ 0 for rank 1 (37a1)")
    mp.mp.dps = 25
    E = get_curve("37a1")
    val = E.L_value(mp.mpc(1))
    ok = abs(val) < 1e-6
    return check("L(37a1, 1) ~ 0 (analytic rank >= 1)", ok, f"|L| = {float(abs(val)):.2e}")


def test_parity_detector():
    print("Test 5: parity detector and rank parity")
    ok_all = True
    for E in all_curves():
        par = root_number_parity(E)
        ok = (par == (E.rank % 2))
        ok_all = ok_all and check(
            f"{E.label}: w-parity {par} = rank%2 {E.rank % 2}", ok
        )
    verdict = parity_detector(claims_full_rank=True, uses_only_root_number=True)
    ok_flag = check("parity-only flag fires on full-rank-from-w", verdict.is_parity_only)
    return ok_all and ok_flag


def test_sha_flag():
    print("Test 6: Sha-finiteness detector on the control pair")
    cp = control_pair()  # 37a1 (proven) vs 389a1 (open)
    flag_proven = sha_finiteness_flag(cp.proven, analytic_rank=1, method_assumes_finite=True)
    flag_open = sha_finiteness_flag(cp.open_, analytic_rank=2, method_assumes_finite=True)
    ok1 = check("rank-1 control: Sha finite is PROVEN", flag_proven.in_proven_regime)
    ok2 = check("rank-2 control: Sha finiteness flagged OPEN", not flag_open.in_proven_regime)
    return ok1 and ok2


def test_functional_equation():
    print("Test 7: exact functional equation off the center (all curves)")
    mp.mp.dps = 25
    ok_all = True
    for E in all_curves():
        N = E.conductor
        y0 = mp.mpf(2) / mp.sqrt(N)
        ylo = 1 / (N * y0)
        n_max = int(30 / (2 * mp.pi * ylo)) + 20

        def g(y):
            acc = mp.mpf(0)
            u = mp.exp(-2 * mp.pi * y)
            upow = mp.mpf(1)
            for n in range(1, n_max + 1):
                upow *= u
                an = E.a_n(n)
                if an:
                    acc += an * upow
            return acc

        ratio = g(ylo) / (N * y0 * y0 * g(y0))
        ok = abs(ratio - E.root_number) < 1e-9
        ok_all = ok_all and check(
            f"{E.label}: g(1/(Ny)) / (N y^2 g(y)) = w = {E.root_number:+d}",
            ok, f"ratio {mp.nstr(ratio, 12)}"
        )
    return ok_all


def test_descent_engine():
    print("Test 8: 2-isogeny descent engine (experiment j)")
    from experiments._shared.descent import (
        descent_rank_bound, selmer_phi, isogenous_curve, to_2torsion_form,
        rational_two_torsion_x,
    )
    ok_all = True
    # bundled rank-0 curves with rational 2-torsion: upper bound == known rank
    for label in ("14a1", "15a1", "17a1"):
        E = get_curve(label)
        ab = to_2torsion_form(E.a_invariants)
        up = descent_rank_bound(*ab)["rank_upper_bound"]
        ok_all = ok_all and check(
            f"{label}: descent upper {up} = rank {E.rank} (Sha={E.sha_order})",
            up == E.rank,
        )
    # congruent curve E_34: rank-2 upper bound
    up34 = descent_rank_bound(0, -34 * 34)["rank_upper_bound"]
    ok_all = ok_all and check("E_34: descent upper bound = 2", up34 == 2, f"got {up34}")
    # Selmer groups have 2-power order (a wrong local decision breaks this)
    for n in (5, 6, 17, 34):
        a, b = 0, -n * n
        ap, bp = isogenous_curve(a, b)
        sizes = (len(selmer_phi(a, b)), len(selmer_phi(ap, bp)))
        pow2 = all(s > 0 and (s & (s - 1)) == 0 for s in sizes)
        ok_all = ok_all and check(f"E_{n}: Selmer orders {sizes} are 2-powers", pow2)
    # the (f) rank >= 2 curves carry no rational 2-isogeny
    for label in ("389a1", "433a1", "571a1", "643a1", "5077a1"):
        E = get_curve(label)
        none = (rational_two_torsion_x(E.a_invariants) == []
                and to_2torsion_form(E.a_invariants) is None)
        ok_all = ok_all and check(f"{label}: E[2] irreducible, descent does not start", none)
    return ok_all


def main():
    results = [
        test_point_counting(),
        test_multiplicativity(),
        test_L_nonzero_rank0(),
        test_L_zero_rank1(),
        test_parity_detector(),
        test_sha_flag(),
        test_functional_equation(),
        test_descent_engine(),
    ]
    print()
    n_pass = sum(results)
    print(f"Smoke test: {n_pass}/{len(results)} passed")
    return 0 if n_pass == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
