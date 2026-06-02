# Experiment (b): weak BSD on a rank 0-3 table

> Weak BSD says $\operatorname{ord}_{s=1} L(E, s) = \operatorname{rank} E(\mathbb{Q})$. We check it on a table spanning the regime boundary that matters: ranks 0 and 1 are proven, ranks $\geq 2$ are open.

## What it does

For every bundled curve, compute the analytic rank (experiment (a)'s machinery) and compare it to the bundled Mordell-Weil rank, labeling each row "proven" (rank $\leq 1$) or "OPEN" (rank $\geq 2$).

## Run

```powershell
python -m experiments.weak_bsd_table.e_b_weak_bsd
```

## Result

Weak BSD holds on 15/15 bundled curves: the analytic rank equals the Mordell-Weil rank for every curve of rank 0, 1, 2, and 3. The four rank-2 curves (389a1, 433a1, 571a1, 643a1) and the rank-3 curve (5077a1) all match.

## Discipline

The script prints the honest status: ranks 0 and 1 are a THEOREM (Gross-Zagier 1986 + Kolyvagin 1990); ranks 2 and 3 are numerical EVIDENCE only, the rank equality is OPEN. It also runs the Sha-finiteness detector on a rank-2 curve to show that any strong-form claim there would be in the open regime.

## Why the table spans ranks 0-3

The rank-2 and rank-3 rows are the point. They exercise the boundary where the proven techniques run out. Agreement there is consistent with BSD and with the rank-boundary thesis, but it is not a proof, and the experiment never claims otherwise.
