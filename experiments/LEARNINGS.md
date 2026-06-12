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

## L7. The rank-1 ceiling, measured (experiment e)

The Heegner machine was implemented end to end on the substrate (modular parametrization $\phi(\tau) = \sum (a_n/n)q^n$ from our own point counts, CM points from binary quadratic forms, AGM period lattice checked against the bundled period, Weierstrass parametrization inverted exactly) and run with ONE code path on three curves:

- **37a1** (rank 1, $w = -1$, $D = -67$): output NON-TORSION, rationalized exactly to $(1357/841,\, 28888/24389) \in E(\mathbb{Q})$, canonical height $= 144.000 \times$ regulator, i.e. the machine manufactured $\pm 12 \cdot$ generator (Heegner index 12) out of modularity and CM alone.
- **389a1** (rank 2, $w = +1$, $D = -67$): output the ZERO point ($|z| < 10^{-10}$ mod $\Lambda$). Rank 2 kills $L'(E/K, 1)$, and Gross-Zagier makes $\hat{h}(y_K)$ proportional to it.
- **5077a1** (rank 3, $w = -1$, $D = -163$): output the ZERO point, despite the root number being IDENTICAL to 37a1's.

The 5077a1 row is the experiment's thesis: the ceiling is not parity. The machine outputs one point whose nonvanishing is equivalent to $L'(E/K,1) \neq 0$, so it is structurally silent on every curve of analytic rank $\geq 2$. This gives the program its operational bar: a Research Direction 01 candidate is interesting exactly when it produces non-torsion output on 389a1, where this machine provably cannot.

## L8. Lower bounds are search problems; the upper bound is the wall (experiment f)

Exact-arithmetic point search plus Neron-Tate heights by exact doubling (no bundled rank data used) found generators on every open-regime curve: $(0,0), (1,0)$ on 389a1, $(0,1), (-1,1)$ on 433a1, $(1,0), (0,1)$ on 571a1, $(1,0), (2,1)$ on 643a1, and $(1,0), (2,0), (0,2)$ on 5077a1. The Gram determinant of the height pairing reproduces the LMFDB regulator to $\approx 10^{-5}$ relative at index 1 on all five, certifying rank $\geq r$ numerically and independently validating the regulator input to experiment (c). The asymmetry is the lesson: the rank lower bound took a few seconds of search; the matching upper bound rank $\leq r$ needs the Selmer/Sha input that does not exist unconditionally in this regime. The missing object is one-sided.

## L9. The parity-blind locus, mapped in a family (experiment g)

Scanning 131 quadratic twists of 11a1 and 37a1 (fundamental $d \equiv 1 \bmod 4$, $|d| \leq 200$ resp. $150$) with closed-form central values ($L(1) = 2\sum (a_n/n)e^{-2\pi n/\sqrt{N}}$ for $w = +1$; $L'(1) = 2\sum (a_n/n)E_1(2\pi n/\sqrt{N})$ for $w = -1$): the root number classifies 120 rows, and 11 rows have $w = +1$ with $L(E_d, 1) = 0$, i.e. analytic rank $\geq 2$ (11a1: $d = -47, -103, -119, -159$; 37a1: $d = 61, 69, -95, 97, -107, 113, -139$). The four 11a1 hits were confirmed at analytic rank exactly 2 by the full AFE ($|L(1)| \sim 10^{-15}$, $|L'(1)| \sim 10^{-24}$, $L''(1) \neq 0$). Every twist's root number was double-checked against the Fricke fixed-point test, $f(i/\sqrt{N_d}) = 0$ iff $w = -1$ (this cross-check is what exposed the bad-prime data error below). The open BSD regime is not exotic: it shows up at $d = -47$ in the very first twist family, and parity is structurally blind to every such row.

## L10. Gross-Zagier is now a measured equation, not a citation (experiment h)

The exact identity behind the only proven BSD regime, $L'(E/K, 1) = \|\omega\|^2 \hat{h}_K(y_K) / (u^2\sqrt{|D|})$, was verified with every factor computed independently on the substrate: $L'(E, 1)$ by the $w = -1$ closed form (cross-checked against the AFE), $L(E_D, 1)$ by the twisted closed form from experiment (g), the Heegner point by experiment (e)'s machine, and its canonical height by new $\sigma$-function local-height machinery accurate to $\sim 20$ digits (the $10^{-5}$ doubling limit is structurally too coarse for this check). In directly computed quantities the identity reads $L'(E,1)\,L(E_D,1) = \mathrm{Vol}(\Lambda)\,\hat{h}(P)/\sqrt{|D|}$ with $P = 2y_K$ the trace. Results: 37a1 over $\mathbb{Q}(\sqrt{-67})$ and $\mathbb{Q}(\sqrt{-11})$, 43a1 and 53a1 over $\mathbb{Q}(\sqrt{-163})$, worst $|ratio - 1| = 1.1 \times 10^{-20}$, and the Heegner indices land on exact integers ($m = 6, 1, 7, 5$; over $\mathbb{Q}(\sqrt{-11})$ the machine outputs 37a1's generator $(1,0)$ on the nose). Two pieces of new substrate fell out: the period lattice now covers $\Delta < 0$ (rhombic case, direct period integrals; 43a1 and 53a1 are the first such curves exercised), and `analytic_height.py` computes $\hat{h}$ to working precision via theta functions, with the normalization pinned by computation (quadraticity $\hat{h}(2P) = 4\hat{h}(P)$ to $10^{-20}$, agreement with three bundled regulators) rather than by convention citation. The program-level lesson sharpens experiment (e): the machine's entire output, not just its nonvanishing, is one first derivative of one $L$-function. Any Research Direction 01 candidate whose output size is proportional to $L'(E/K,1)$ is the old machine in disguise; the rank-2 object must carry a second Taylor coefficient.

## Data-integrity note

During scaffolding, three bundled rank-2 records had incorrect Weierstrass models (one was a copy of 37a1's coefficients, two had discriminants inconsistent with their conductors), and produced nonzero $L(1)$. They were replaced with verified rank-2 models (433a1 = [1,0,0,0,1], 571a1 = [0,1,1,-4,2], 643a1 = [1,0,0,-4,3]) for which $L(1) \approx L'(1) \approx 0$ and $L''(1) \neq 0$, restoring 15/15 agreement. Lesson: validate every bundled model by an independent $L$-value computation, not just by label.

**Third instance (2026-06-10), found by re-running experiment (c) with corrected $a_p$: the bundled regulators of 57a1 and 58a1 were wrong, and 58a1's Tamagawa product too.** With the corrected low coefficients ($a_3(57a1) = -1$, $a_2(58a1) = -1$), strong BSD gave $\#\operatorname{Sha} = 0.93$ resp. $0.75$. Exact point search found the true generators ($(2,1)$ on 57a1, $\hat{h} = 0.0375746$; $(0,1)$ on 58a1, $\hat{h} = 0.0424203$; multiples scale exactly $1:4:9:16$), and $\Delta(58a1) = -116$ gives nonsplit $I_2$ at 2, so $c_2 = 2$ (bundled said 1). With these values $\#\operatorname{Sha} = 1.0000$ on all fifteen curves. The original table had passed because the wrong $a_p$ and the wrong regulator cancelled in the check: **two compensating errors are invisible to a single end-to-end test; only independent recomputation of each factor separates them.** (43a1 and 53a1 regulators were re-derived the same way and match the bundle to 7 digits.)

**Second instance (2026-06-09), found by experiment (g)'s self-checks: nine of fifteen bundled bad-prime $a_p$ had the wrong sign** (37a1, 43a1, 53a1, 57a1, 58a1 are non-split where the table said split; 433a1, 571a1, 643a1 are split where it said non-split; 5077a1 non-split). Three independent confirmations: the split criterion ($a_p = +1$ iff $-c_6$ is a square mod $p$), the prime-level Atkin-Lehner identity $a_N = w$, and the exact off-center functional equation $g(1/(Ny)) = w N y^2 g(y)$, which now passes to 12 digits on all 15 curves and is permanently installed as smoke-test check 7. The central-value experiments (a)-(d) never noticed because the AFE weight at $n = N$ is $e^{-2\pi\sqrt{N}}$-level, i.e. invisible: **a wrong $a_N$ is undetectable at the center of the strip and instantly fatal off it.** The deeper lesson generalizes the first one: every consistency check the theory offers (here, the functional equation as an exact identity, not just the central value) should be wired into the substrate as a permanent test, because each one sees errors the others structurally cannot.
