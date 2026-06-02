"""Experiment (b): verify the weak-BSD rank equality on a table of curves.

Weak BSD: ord_{s=1} L(E, s) (the analytic rank) equals rank E(Q) (the
Mordell-Weil rank). We compute the analytic rank from experiment (a)'s machinery
and compare it to the bundled Mordell-Weil rank for curves of rank 0, 1, 2, 3.

The point of the rank-2 and rank-3 rows is the wrong-approach discipline: ranks
0 and 1 are PROVEN (Gross-Zagier + Kolyvagin), ranks >= 2 are OPEN. The numerical
agreement there is evidence for BSD, not a proof, and the script says so.

Run from the repo root:
    python -m experiments.weak_bsd_table.e_b_weak_bsd
"""

from __future__ import annotations

import mpmath as mp

from experiments._shared import all_curves, sha_finiteness_flag


def analytic_rank(E, max_order, tol=1e-4):
    for k in range(max_order + 1):
        if abs(E.L_derivative_at_one(k)) > tol:
            return k
    return max_order + 1


def main():
    mp.mp.dps = 25
    print(f"{'curve':>8} {'cond':>6} {'an.rank':>8} {'MW rank':>8} {'regime':>8} {'match':>6}")
    print("-" * 52)
    n_match = 0
    for E in all_curves():
        max_order = 3 if E.rank <= 2 else 4
        r_an = analytic_rank(E, max_order)
        regime = "proven" if E.rank <= 1 else "OPEN"
        match = (r_an == E.rank)
        n_match += int(match)
        print(f"{E.label:>8} {E.conductor:>6} {r_an:>8} {E.rank:>8} {regime:>8} "
              f"{('YES' if match else 'no'):>6}")
    print("-" * 52)
    n = len(list(all_curves()))
    print(f"weak BSD (analytic rank == MW rank) holds on {n_match}/{n} bundled curves")
    print()
    print("HONEST STATUS:")
    print("  ranks 0, 1: BSD rank equality is a THEOREM (Gross-Zagier 1986 + Kolyvagin 1990).")
    print("  ranks 2, 3: agreement is NUMERICAL EVIDENCE only; the rank equality is OPEN.")

    # Sha discipline on a rank-2 curve in the table.
    rank2 = next(E for E in all_curves() if E.rank == 2)
    flag = sha_finiteness_flag(rank2, analytic_rank=2, method_assumes_finite=False)
    print()
    print(f"  {rank2.label}: {flag.message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
