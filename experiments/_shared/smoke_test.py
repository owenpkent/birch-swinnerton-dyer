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


def main():
    results = [
        test_point_counting(),
        test_multiplicativity(),
        test_L_nonzero_rank0(),
        test_L_zero_rank1(),
        test_parity_detector(),
        test_sha_flag(),
    ]
    print()
    n_pass = sum(results)
    print(f"Smoke test: {n_pass}/{len(results)} passed")
    return 0 if n_pass == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
