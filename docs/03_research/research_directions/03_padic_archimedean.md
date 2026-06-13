# Direction 03: from the p-adic main conjecture to the archimedean leading term

> Open question. The Iwasawa main conjecture (Kato; Skinner-Urban) gives the $p$-part of strong BSD in many cases. The archimedean leading-coefficient formula and unconditional Sha-finiteness in rank $\geq 2$ remain out of reach. Can the $p$-adic information be assembled across all $p$ to constrain the archimedean term?

## The target

Strong BSD pins the leading Taylor coefficient $L^{(r)}(E,1)/r!$ to $\Omega_E \operatorname{Reg}_E \prod_p c_p \#\operatorname{Sha}(E) / (\#E(\mathbb{Q})_{\mathrm{tors}})^2$. The $p$-adic main conjecture controls the $p$-part of $\#\operatorname{Sha}$ and the $p$-adic regulator. The open piece is the archimedean (real, transcendental) leading term and the global finiteness of $\operatorname{Sha}$.

The question: do the known $p$-adic BSD results, taken over all $p$ simultaneously, plus the Mazur-Tate-Teitelbaum $p$-adic BSD for the order of vanishing, constrain the archimedean leading term enough to make progress in rank $\geq 2$?

## Architecture-3 detector scorecard (Iwasawa theory)

Scored against the three detectors and the rank control pair. The reading notes behind each row: [Skinner-Urban 2014](../reading_notes/Skinner-Urban-2014-Iwasawa-Main-GL2.md) (the main conjecture, reverse divisibility), [Mazur-Tate-Teitelbaum 1986 + Greenberg-Stevens 1993](../reading_notes/Mazur-Tate-Teitelbaum-1986-p-adic-BSD.md) (the $p$-adic $L$-function and the exceptional zero), and [Coates-Wiles 1977](../reading_notes/Coates-Wiles-1977-BSD.md) (the elliptic-unit ancestor).

| Detector | Verdict | Where exactly |
|---|---|---|
| **1 (parity-only)** | PASSES | The $p$-adic $L$-function gives the exact $p$-adic valuation of the leading term (Skinner-Urban Thm 2(a)) and the $\mathcal{L}$-invariant (MTT/GS), both far finer than rank mod 2. The exceptional zero even separates the $p$-adic order from the parity-controlled complex order by a known $+1$. |
| **2 (Sha-finiteness)** | THE WALL, flagged honestly | The main conjecture PROVES (not assumes) $\#\mathrm{Sha}[p^\infty]<\infty$ and computes $v_p(\#\mathrm{Sha})$, but only for *one ordinary $p$ at a time*, under irreducibility/ramification hypotheses, and only in analytic rank $0$ (a one-sided corank statement at rank $1$). Global finiteness in rank $\geq 2$ needs all $p$ at once plus a bound on the contributing primes. Not delivered. |
| **3 (function-field mirage)** | PASSES | The cyclotomic $\mathbf{Z}_p$-extension, $GU(2,2)$ Eisenstein congruences, and weight deformations are number-field objects. No elliptic surface, no geometric Frobenius, no Brauer group. |
| **Control pair** | proven side, one prime over | The whole architecture caps where the $p$-adic $L$-function's order is controlled: rank $0$ unconditionally, a $p$-adic "half" of rank $1$. The single Hida family feeding the Eisenstein congruence, like the single $\mathcal{L}$-invariant, is a rank-$\leq 1$ object. |

## Computational evidence: experiment (k)

[Experiment (k)](../../../experiments/padic_lfunction/e_k_padic_lfunction.py) makes the MTT layer concrete on the bundled curves, exactly and offline (engine: [`_shared/padic.py`](../../../experiments/_shared/padic.py), guarded by smoke check 9):

- **The exceptional zero is exhibited, not assumed.** Every split-multiplicative prime-conductor curve (11a1 rank 0; 389a1, 433a1, 571a1, 643a1 rank 2) has $a_N = +1$, unit root $\alpha = 1$, interpolation factor $0$: an extra zero of $L_p$ with no Mordell-Weil cause. The non-split curves (37a1, 43a1, 53a1, 5077a1) have factor $2$, none.
- **The $\mathcal{L}$-invariant is computed** to 20 base-$p$ digits, with $\operatorname{ord}_p(q) = v_p(\Delta)$ verified on each curve. It is a genuinely $p$-adic number with no archimedean shadow.
- **The Greenberg-Stevens right-hand side is assembled** on 11a1: $L(11a1,1)/\Omega_E = 1/5$ (from the substrate) embeds in $\mathbf{Z}_{11}$, giving the predicted $L_p'(E,1) = \mathcal{L}_p(E)\cdot 1/5$ as an explicit $11$-adic number.
- **The open regime is named precisely.** For the rank-2 curves $L_p$ vanishes to order $\operatorname{rank}+1 = 3$; the $\mathcal{L}$-invariant is one factor of the leading $p$-adic coefficient, the rest being the $p$-adic height regulator (Bernardi / Perrin-Riou), which is NOT built.

## The missing computational objects

1. The full $p$-adic $L$-function value/derivative via overconvergent modular symbols (Pollack-Stevens). Experiment (k) supplies the $\mathcal{L}$-invariant and the exceptional-zero structure, i.e. the whole MTT phenomenon at the level of the leading term, but not $L_p(E,s)$ itself.
2. The $p$-adic height regulator $\operatorname{Reg}_p$ (Mazur-Tate / Schneider), the $p$-adic analog of $\operatorname{Reg}_E$, needed for the leading term in rank $\geq 1$.

## Why it is hard

Assembling $p$-adic data across all $p$ into an archimedean (characteristic 0, transcendental) statement is not a formal operation. The periods $\Omega_E$ and the regulator are real transcendentals; the $p$-adic theory speaks to $p$-adic valuations and $p$-adic regulators. Bridging the two is the content of the conjectures of Beilinson-Bloch-Kato, themselves largely open.

## Falsifiability trigger

If it is shown that the known $p$-adic inputs are formally insufficient to bound the archimedean term in rank $\geq 2$ (e.g. a precise obstruction in the comparison of $p$-adic and archimedean periods), the direction is retired with that obstruction recorded.

## Deliverable status

DONE (2026-06-12): the detector scorecard above; the [MTT/Greenberg-Stevens reading note](../reading_notes/Mazur-Tate-Teitelbaum-1986-p-adic-BSD.md) mapping each result to the strong-BSD factor it controls; and experiment (k), the computational anchor. OPEN: the two missing computational objects above, and the all-$p$-to-archimedean comparison.
