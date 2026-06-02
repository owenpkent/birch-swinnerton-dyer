"""Experiment (a): analytic rank from L(E, s) and its derivatives at s = 1.

For each bundled curve we estimate the analytic rank as the least k with
L^{(k)}(E, 1) != 0, computed from the smoothed approximate functional equation
at high mpmath precision. The root number gives the parity for free, so we
print it next to the estimate as a consistency check.

This is the central experiment for WEAK BSD: the analytic rank is the left-hand
side of the rank equality. Experiment (b) compares it to the Mordell-Weil rank.

Run from the repo root:
    python -m experiments.l_function_rank.e_a_analytic_rank
"""

from __future__ import annotations

import mpmath as mp

from experiments._shared import all_curves, parity_detector


def estimate_rank(E, max_order=4, tol=1e-5):
    derivs = []
    for k in range(max_order + 1):
        v = E.L_derivative_at_one(k)
        derivs.append(v)
        if abs(v) > tol:
            return k, derivs
    return max_order + 1, derivs


def main():
    mp.mp.dps = 25
    print(f"{'curve':>8} {'cond':>6} {'w':>3} {'parity':>7} {'an.rank':>8} {'MW rank':>8} {'match':>6}")
    print("-" * 56)
    n_match = 0
    total = 0
    for E in all_curves():
        # rank 3 derivative-finding at dps 25 is expensive; cap the search order
        max_order = 3 if E.rank <= 2 else 4
        r_an, _ = estimate_rank(E, max_order=max_order, tol=1e-4)
        parity = 0 if E.root_number == 1 else 1
        match = (r_an == E.rank)
        n_match += int(match)
        total += 1
        print(f"{E.label:>8} {E.conductor:>6} {E.root_number:>3} {parity:>7} "
              f"{r_an:>8} {E.rank:>8} {('YES' if match else 'no'):>6}")

    print("-" * 56)
    print(f"analytic rank == Mordell-Weil rank on {n_match}/{total} curves")

    # Wrong-approach discipline: the parity alone is NOT the rank.
    v = parity_detector(claims_full_rank=True, uses_only_root_number=True)
    print()
    print("DISCIPLINE:", v.message)
    print("The table above used derivative VANISHING, not just w, to get the rank.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
