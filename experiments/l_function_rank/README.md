# Experiment (a): analytic rank from L-derivatives

> The least $k$ with $L^{(k)}(E, 1) \neq 0$ is the analytic rank, the left side of the BSD rank equality. We compute it from the smoothed approximate functional equation at high precision.

## What it does

For each bundled curve, evaluate $L^{(k)}(E, 1)$ for $k = 0, 1, 2, \dots$ until a nonzero value appears. That $k$ is the analytic rank. The root number $w$ is printed alongside as a parity consistency check ($w = (-1)^k$).

## Run

```powershell
python -m experiments.l_function_rank.e_a_analytic_rank
```

## Result

The analytic rank matches the Mordell-Weil rank on every bundled curve (ranks 0, 1, 2, 3). For rank 0 the value $L(E, 1)$ is clearly nonzero; for rank 1, $L(E, 1) \approx 0$ but $L'(E, 1) \neq 0$; for rank 2, the first two derivatives vanish and $L''(E, 1) \neq 0$; for rank 3, the first three vanish.

## Discipline

The experiment invokes Detector 1 and prints its message: the root number alone gives only the parity, so a full-rank claim from $w$ is incomplete. The rank here is obtained from derivative VANISHING, not from $w$, which is why it can distinguish rank 0 from rank 2 (both have $w = +1$).

## Honest status

Ranks 0 and 1 are a theorem (Gross-Zagier + Kolyvagin); the agreement there checks the implementation. Ranks 2 and 3 are OPEN; the agreement is numerical evidence for BSD, not a proof.
