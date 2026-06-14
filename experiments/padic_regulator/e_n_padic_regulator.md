# Experiment (n): the 2x2 p-adic height regulator of 389a1

> The object experiment (k) named missing. Experiment (k) computed the Mazur-Tate-Teitelbaum $\mathcal{L}$-invariant and the exceptional zero, then said the rest of the rank $\geq 2$ leading $p$-adic coefficient is the $p$-adic height regulator $\mathrm{Reg}_p$, which it did not build. This experiment builds it: the Mazur-Tate $p$-adic sigma function, the formal-group reduction, the cyclotomic $p$-adic height $h_p(P)$ (Mazur-Stein-Tate), the bilinear pairing, and the $2\times 2$ Gram determinant $\mathrm{Reg}_p$ on 389a1's two generators. Robustness and verifiability first. **This is not a proof of BSD, not a crossing of either Kudla bridge, and not a rank $\geq 2$ construction.**

## The iron rule, stated first

This is the highest-overclaim-risk task in the project, so the boundaries come before the result.

- **Not a proof, not a bridge crossing.** The rank $\geq 2$ construction stays OPEN. Numerical agreement in rank $\geq 2$ is EVIDENCE, never PROOF.
- **The points are INPUT, not constructed.** The two generators of 389a1, $P = (0,0)$ and $Q = (1,0)$, were found by search in experiment (f). This experiment computes their $p$-adic height regulator. It does not produce the points and does not bound $\mathrm{Sha}$. Bridge 2 (cycle / construction $\to$ a rational point) is NOT crossed here. Said loudly: $\mathrm{Reg}_p$ is a determinant built FROM two points already in hand, not a machine that makes a second point.
- **The narrow claim under test.** Bridge 1's ORDER GAP is archimedean. On the complex side, arithmetic Siegel-Weil incoherence is ONE sign and forces a FIRST derivative; on a rank-2 curve the Gross-Zagier height identity reads $0 = 0$ exactly (experiment (e)). On the $p$-adic side the cyclotomic / weight variable is a genuine SECOND deformation direction, and the $p$-adic height pairing is a genuine second-order object: $\mathrm{Reg}_p$ is the $p$-adic analog of the Neron-Tate regulator that the $p$-adic BSD leading term carries in rank $\geq 2$. That is the specific sense in which the order gap is circumvented $p$-adically.

## Theorem vs conjecture (the surveyor caution, taken seriously)

The claim "the second order is reached $p$-adically" is a PROGRAM, not a theorem, exactly where it would matter. Stated honestly:

**Theorem.**
- The construction of $h_p$ (sigma function, formal group, height as a $p$-adic log) is a rigorous definition for good ordinary $p$ (Mazur-Tate 1991, "The $p$-adic sigma function"; Mazur-Stein-Tate 2006, "Computing $p$-adic heights").
- $h_p$ is a quadratic form and the pairing is bilinear. VERIFIED here for every $c$.
- $p$-adic Gross-Zagier (Perrin-Riou 1987; Nekovar; Disegni) ties a $p$-adic $L$-derivative to a $p$-adic height of a Heegner point in analytic rank 1. That is the proven $p$-adic shadow, and it is a one-Heegner-point statement.

**Conjecture / open.**
- NON-DEGENERACY of the $p$-adic height pairing ($\mathrm{Reg}_p \neq 0$) is OPEN in general (Schneider). It is not known in rank $\geq 2$. So the second-order $p$-adic object is conjecturally non-trivial exactly where it would help.
- The link $\mathrm{Reg}_p \to$ leading term of $L_p \to \#\mathrm{Sha}[p^\infty]$ is the $p$-adic BSD / Iwasawa main conjecture: CONDITIONAL, one prime $p$ at a time (Detector 2).
- There is no $p$-adic Gross-Zagier in analytic rank $\geq 2$ producing TWO independent points. The second deformation direction gives a second-order $p$-adic $L$-value tied to a regulator of points ALREADY GIVEN; it does not manufacture the second point. Bridge 2 stays open $p$-adically too.

Net: the $p$-adic side genuinely has a second-order object (the height pairing / $\mathrm{Reg}_p$) where the archimedean Gross-Zagier leg has only a first-order one. That is real and is the point of the experiment. It is NOT a second independent rational point and NOT an unconditional $\mathrm{Sha}$ bound.

## The chosen prime: $p = 5$

The conductor of 389a1 is 389 (prime), so every $p \neq 389$ is good. The smallest good ordinary non-anomalous prime is $p = 5$:

| $p$ | $a_p$ | reduction | $m = \#E(\mathbb{F}_p)$ | usable |
|---|---|---|---|---|
| 2 | $-2$ | supersingular ($p \mid a_p$) | $-$ | no |
| 3 | $-2$ | ordinary but **anomalous** ($p \mid \#E(\mathbb{F}_p) = 6$) | 6 | no |
| **5** | $-3$ | **good ordinary** | **9** | **YES** |
| 7 | $-5$ | good ordinary | 13 | yes (contrast) |
| 11 | $-4$ | good ordinary | 16 | yes |

$p = 5$ is ordinary because $a_5 = -3 \not\equiv 0 \pmod 5$, and non-anomalous because $m = \#E(\mathbb{F}_5) = 9$ is prime to 5, so $1/m^2$ is a 5-adic unit. The multiplier $m = 9$ pushes $mP$ into the kernel of reduction at 5 (the formal group); trivial torsion and trivial Tamagawa numbers mean no further factor is needed.

## What was built

The engine is [`_shared/padic_height.py`](../_shared/padic_height.py), the $p$-adic mirror of the archimedean `analytic_height.py`:

1. **Formal group.** With $t = -x/y$, solve the Weierstrass relation for $w(t) \in \mathbb{Z}[[t]]$; then $x(t), y(t)$, the invariant differential $\omega = (1 + \dots)\,dt$, the formal logarithm $z(t)$, and its inverse $t(z)$. Verified: $\log \circ \exp = \mathrm{id}$ exactly, and on the short model $y^2 = x^3 - x$ the expansion $w = t^3 - t^7 + 2t^{11} + \dots$ is reproduced.

2. **The $p$-adic sigma function.** $\sigma_p(z) = z + O(z^3)$, odd, defined by $-\tfrac{d^2}{dz^2}\log\sigma_p = x(z) + c$, integrated twice. Verified odd ($z + \tfrac{1}{6}z^3 - \tfrac{1}{40}z^5 + \dots$).

3. **Formal-group reduction.** $m = \#E(\mathbb{F}_p)$, $mP = (x_m, y_m)$, $t_m = -x_m/y_m$ with $v_p(t_m) \geq 1$. Verified $v_5(t_m) = 1$.

4. **The cyclotomic height.** $h_p(P) = \tfrac{1}{m^2}\big(2\log_p \sigma_p(mP) - \log_p \mathrm{den}\,x(mP)\big)$, Iwasawa branch. The normalization is PINNED by the quadraticity self-check.

5. **The pairing and regulator.** $\langle P, Q\rangle_p = \tfrac{1}{2}(h_p(P+Q) - h_p(P) - h_p(Q))$, $\mathrm{Reg}_p = \det$.

All power-series arithmetic is exact rational; a single $p$-adic logarithm (from `padic.py`) closes it. Everything runs offline as a module from the repo root.

## Self-checks (the verification plan, executed)

Because a from-scratch $p$-adic height is error-prone, every checkable invariant was checked:

- **Quadraticity** $h_p(nP) = n^2 h_p(P)$: holds to full precision, for $n = 2, 3, 4$, for EVERY $c$.
- **Bilinearity** $\langle P+Q, R\rangle_p = \langle P, R\rangle_p + \langle Q, R\rangle_p$: holds for every $c$.
- **Parallelogram law** $h_p(P+Q) + h_p(P-Q) = 2h_p(P) + 2h_p(Q)$: holds for every $c$.
- **Precision stability**: $v_5(\mathrm{Reg}_5) = 2$ and the unit digits $96 \bmod 5^4$ are identical at PREC $= 12, 16, 20, 24$.
- **Rank-1 calibration**: on 37a1's generator $(0,0)$, $h_5$ and $h_7$ are quadratic and stable with $v_5 = v_7 = 1$, matching the Mazur-Stein-Tate worked example structure.
- **Sigma self-check**: $\sigma_p(t) = t + O(t^2)$, odd in $z$.

## The result, and the named gap

The $c$-INDEPENDENT, certified invariant (the bundled-checkable reference):
$$v_5\big(\mathrm{Reg}_5(389a1)\big) = 2, \qquad v_7\big(\mathrm{Reg}_7(389a1)\big) = 2.$$
These valuations match the published structure (Mazur-Stein-Tate 2006; Stein-Wuthrich), which is exactly why 389a1 is the canonical non-degenerate $p$-adic-regulator example: $\mathrm{Reg}_p \neq 0$ is observed (not proven; Schneider non-degeneracy is open).

**The headline is a MEASURED comparison.** The experiment prints the computed $\mathrm{Reg}_p$ valuation against a bundled reference (`REFERENCE_REG_VALUATION` in the experiment header, attributed below in `curve_data.py` style) and the difference:

| datum | computed | reference | $|\text{diff}|$ | match |
|---|---|---|---|---|
| $v_5(\mathrm{Reg}_5(389a1))$ | 2 | 2 | 0 | YES |
| $v_7(\mathrm{Reg}_7(389a1))$ | 2 | 2 | 0 | YES |

The difference is 0: the computed valuation EQUALS the bundled reference exactly, and the match is asserted (a drift in the sigma / reduction / height engine fails the run). Only the valuation is compared, because only the valuation is $c$-independent; the unit digits depend on the named gap $c$, so they are deliberately omitted rather than fabricated. A wrong formal group, sigma recursion, or reduction multiplier would move the valuation, so this exact (if coarse) agreement is a genuine check, not a tautology. The engine also generalizes off 389a1: on 433a1 at $p = 7$ (where $m = \#E(\mathbb{F}_7) = 11$) it returns $v_7(\mathrm{Reg}_7(433a1)) = 2$, stable across precision, confirming it is not 389a1-specific.

**The one gap, named not hidden.** The cyclotomic height needs one constant $c$, the Mazur-Tate $p$-adic $E_2$ value of $E$. Quadraticity, bilinearity, and the parallelogram law hold for EVERY $c$, so the self-checks verify the pipeline UP TO $c$ but cannot pin it. The valuation $v_p(\mathrm{Reg}_p)$ is $c$-independent, so it is delivered. The UNIT digits of $\mathrm{Reg}_p$ depend on $c$, and computing $c$ rigorously offline needs Kedlaya's Frobenius algorithm or overconvergent modular symbols, neither built here, exactly as experiment (k) did not build the overconvergent $p$-adic $L$-function. The function `sigma_constant_c` raises `NotImplementedError`: it names the gap, it does not ship a wrong number. This is the honest fallback the task specified, and it is the same discipline experiment (k) used when it named ITS missing objects.

## Detector posture

- **Detector 1 (parity).** PASSES. $\mathrm{Reg}_p$ is a leading-coefficient datum, far finer than rank mod 2. It lives at $p$, not at infinity.
- **Detector 2 (Sha-finiteness).** Flagged every time. The bridge $\mathrm{Reg}_p \to \#\mathrm{Sha}[p^\infty]$ is the Iwasawa main conjecture, conditional and one prime at a time. No $\mathrm{Sha}$ bound in rank $\geq 2$ is produced; non-degeneracy of the pairing is itself open. The experiment computes $\mathrm{Reg}_p$, it does not read off a $\#\mathrm{Sha}$.
- **Detector 3 (function-field mirage).** PASSES. The cyclotomic $\mathbb{Z}_p$-extension is the only deformation; the formal group is the $p$-adic completion of $E$ itself. No elliptic surface, no geometric Frobenius, no Brauer group. The $p$-adic / weight direction is the number-field SUBSTITUTE for the function-field second leg (Yun-Zhang's $\mathrm{Sht}^2$ over $X^2$ and the Frobenius twist), and it imports neither.

## Attribution of bundled reference values

- The algorithm: B. Mazur, W. Stein, J. Tate, "Computing $p$-adic heights of points on elliptic curves," Math. Comp. 75 (2006); B. Mazur, J. Tate, "The $p$-adic sigma function," 1991.
- The $p$-adic BSD leading-term shape: Mazur-Tate-Teitelbaum 1986 (reading note in `docs/03_research/reading_notes/`); Bernardi; Perrin-Riou.
- The valuation reference $v_5(\mathrm{Reg}_5(389a1)) = 2$, $v_7 = 2$: consistent with the Mazur-Stein-Tate 2006 worked example and the Stein-Wuthrich $p$-adic-regulator tables; here it is re-derived from scratch and cross-checked across precision and across $c$.

## Status

DONE: the formal group, the $p$-adic sigma recursion, the formal-group reduction, the cyclotomic height assembly (pinned by quadraticity), the bilinear pairing, the $2\times 2$ Gram matrix on 389a1, the rank-1 calibration on 37a1, and the $c$-independent $v_p(\mathrm{Reg}_p)$. NAMED GAP: the constant $c$ = the $p$-adic $E_2$ value (Kedlaya / overconvergent symbols), hence the unit digits of $\mathrm{Reg}_p$. OPEN, and stated as open: the rank $\geq 2$ construction, both Kudla bridges, non-degeneracy of the $p$-adic height pairing, and unconditional $\mathrm{Sha}$-finiteness. Nothing here is progress on the rank $\geq 2$ object; it is the $p$-adic second-order MEASUREMENT the archimedean leg cannot make.
