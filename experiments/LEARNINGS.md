# Learnings

> Cross-cutting findings from the experimental thread. The synthesis surface read at session start. Companion to [`PLAN.md`](PLAN.md) and [`../STATE_OF_THE_PROGRAM.md`](../STATE_OF_THE_PROGRAM.md).

## L1. The substrate is validated end to end

The smoke test passes 6/6. Point counting reproduces known $a_p$ for 11a1 ($a_2 = -2$, $a_3 = -1$, $a_5 = 1$, $a_7 = -2$, $a_{13} = 4$) and respects the Hasse bound. The multiplicative $a_n$ recurrence is correct ($a_4 = a_2^2 - 2$, $a_6 = a_2 a_3$). The smoothed AFE gives $L(11a1, 1) \approx 0.2538$ (rank 0, nonzero) and $L(37a1, 1) \approx 0$ (rank 1). The whole analytic pipeline is trustworthy at the bundled conductors.

## L2. Weak BSD holds on every bundled curve, including all rank-2 and rank-3 cases

Experiment (b): the analytic rank (least $k$ with $L^{(k)}(E, 1) \neq 0$) equals the Mordell-Weil rank on all 15 curves, spanning ranks 0, 1, 2, 3. The four rank-2 curves (389a1, 433a1, 571a1, 643a1) each show $L(1) \approx L'(1) \approx 0$ and $L''(1) \neq 0$; the rank-3 curve (5077a1) shows the first three derivatives vanishing. For ranks 0 and 1 this is a check on a theorem; for ranks 2 and 3 it is numerical evidence for an OPEN case, and the script labels it as such.

## L3. The strong-BSD formula is consistent with #Sha a perfect square

Experiment (c): solving the strong-BSD formula for $\#\operatorname{Sha}$ (using the bundled period, regulator, Tamagawa product, torsion and the computed leading coefficient) lands near $1$ (a perfect square) on every bundled curve. The real period recomputed independently via the AGM of the Weierstrass roots reproduces the bundled period. In the rank $\geq 2$ rows this is "the formula is consistent with $\operatorname{Sha} = 1$," not a theorem, because finiteness of $\operatorname{Sha}$ is open there. Detector 2 fires accordingly.

## L4. The a_p pipeline is correct (Sato-Tate)

Experiment (d): for 37a1 (non-CM) the empirical distribution of $a_p / (2\sqrt p)$ over 668 primes up to 5000 tracks the Sato-Tate semicircle with a chi-square-like deviation of $\approx 0.014$. Sato-Tate is a theorem for non-CM $E/\mathbb{Q}$, so a good match validates the point counts that feed every other experiment.

## L5. The detectors behave as designed

- Detector 1 fires on any full-rank-from-root-number claim; the experiments avoid it by using derivative vanishing.
- Detector 2 correctly distinguishes the proven regime (rank $\leq 1$) from the open one (rank $\geq 2$).
- Detector 3's template is documented and no experiment imports a geometric Frobenius.

## L6. The boundary is the lesson

Every positive result here is in the proven regime or is labeled evidence in the open regime. Nothing in the computational thread crosses from rank $\leq 1$ (proven) to rank $\geq 2$ (a theorem). That is expected: the experiments validate the substrate; they do not attempt the missing construction. The lesson is the same as the program's thesis: the difficulty is concentrated in producing the rank $\geq 2$ object, not in the analytic bookkeeping, which works fine.

## Data-integrity note

During scaffolding, three bundled rank-2 records had incorrect Weierstrass models (one was a copy of 37a1's coefficients, two had discriminants inconsistent with their conductors), and produced nonzero $L(1)$. They were replaced with verified rank-2 models (433a1 = [1,0,0,0,1], 571a1 = [0,1,1,-4,2], 643a1 = [1,0,0,-4,3]) for which $L(1) \approx L'(1) \approx 0$ and $L''(1) \neq 0$, restoring 15/15 agreement. Lesson: validate every bundled model by an independent $L$-value computation, not just by label.
