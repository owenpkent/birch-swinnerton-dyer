# Direction 01: the rank-2 object, specified precisely

> The most-leveraged move in the program: pin down exactly what a rank-2 generalization of the Heegner construction must produce, so every candidate is tested against a fixed target. Upgraded 2026-06-11: the spec's bars are no longer aspirational, they are quantities measured by experiments (e), (f), (g), (h), and one of the anticipated obstructions is now cited as a theorem (Gross-Kohnen-Zagier) and exhibited numerically on our own substrate.

## Why this first

The Heegner construction produces one point, and experiment (h) measured what that means quantitatively: the height of the machine's entire output is one first derivative of one $L$-function, $L'(E,1)\,L(E_D,1) = \mathrm{Vol}(\Lambda)\,\hat{h}(P)/\sqrt{|D|}$, verified to $10^{-20}$ on four $(E, K)$ pairs. On every curve of analytic rank $\geq 2$ that number is $0$ and the machine outputs torsion (experiment (e), measured on 389a1 and 5077a1). The open part of BSD is exactly the regime where this equation reads $0 = 0$. Before attempting any construction, the target must be fixed.

## The object's type

A construction $\mathcal{C}$ with:

- **Input.** $E/\mathbb{Q}$ of analytic rank $2$ (operationally: $w = +1$, $L(E,1) = 0$, $L''(E,1) \neq 0$, certified as in experiments (b) and (g)), together with auxiliary data $\mathrm{Aux}(E)$ that provably exists for every such $E$ over $\mathbb{Q}$ (a field, a family of cycles, an automorphic object). The existence requirement is Detector 3's hook: over $\mathbb{F}_q(C)$ the auxiliary object is $H^2$ of the elliptic surface; the spec demands a substitute that lives over $\mathbb{Q}$.
- **Output.** Points $P_1, P_2 \in E(\mathbb{Q})$ (or $E(K)$ with a controlled descent to $\mathbb{Q}$) plus a certificate, subject to the three clauses below.

### Clause 1: nondegeneracy (the 389a1 bar, from experiment e)

The Neron-Tate Gram matrix $R = (\langle P_i, P_j \rangle)$ has $\det R > 0$. Operationally: $\mathcal{C}$ must output non-torsion, independent points on 389a1, where the Heegner machine provably and measurably returns the zero point ($|z| < 10^{-10}$ mod $\Lambda$). This clause alone separates $\mathcal{C}$ from every proven technique.

### Clause 2: second-order analytic tie (the bar from experiment h)

There is an explicit constant $\kappa(E, \mathrm{Aux}) > 0$ with

$$\det R \;=\; \kappa \cdot \frac{L^{(2)}(E/K, 1)}{2!} \quad \text{(or the corresponding leading coefficient over } \mathbb{Q}\text{)}.$$

This is the rank-2 analog of the measured Gross-Zagier identity, with the $2 \times 2$ regulator replacing the square of one height and the second Taylor coefficient replacing the first. The clause excludes, by construction, any $\mathcal{C}$ whose output size factors through $L'(E/K, 1)$: on rank $\geq 2$ input that number is exactly $0$, so such a $\mathcal{C}$ is the old machine in disguise and outputs torsion. "Tied to the analytic side" means precisely this clause; nothing weaker forces independence.

### Clause 3: Sha control

Either $\mathcal{C}$ also produces an Euler-system-type bound on $\operatorname{Sha}$, or it is explicitly paired with Direction 02. Without this clause the construction proves rank $\geq 2$ but not the rank equality, and strong BSD stays out of reach (Detector 2 territory).

## What the spec excludes, now as theorems and measurements

- **Parity readers (Detector 1).** Experiment (g) found 11 twists of 11a1/37a1 with $w = +1$ and $L(E_d, 1) = 0$: analytic rank 2, invisible to the root number. Any $\mathcal{C}$ that only reads $w$ cannot distinguish 11a1 $\times$ (-47) (rank 2) from the rank-0 twists in the same family. Concrete failure instance, ready to run.
- **Multi-field Heegner points: retired by theorem.** Gross-Kohnen-Zagier (1987): the Heegner points $y_D$ for varying discriminant all lie on a single line in $E(\mathbb{Q}) \otimes \mathbb{Q}$ (their heights are the coefficients of a weight-3/2 modular form). Two fields do not give two independent points, ever. Exhibited on our substrate by experiment (h): on 37a1 the traces over $\mathbb{Q}(\sqrt{-67})$ and $\mathbb{Q}(\sqrt{-11})$ are $\pm 12 G$ and $\pm 2 G$ for the same generator $G = (0,0)$, so the $2 \times 2$ Gram determinant of the pair is exactly $0$. The old draft listed this as an obstruction to anticipate; it is a measured fact.
- **Function-field imports (Detector 3).** Over $\mathbb{F}_q(C)$, rank $\geq 2$ is reachable because the Neron-Severi group of the elliptic surface supplies independent classes and Tate's theorem converts cohomology to points. The spec's existence requirement on $\mathrm{Aux}(E)$ is the guard: a candidate whose auxiliary object is "the second cohomology of the arithmetic surface" in any disguise has not crossed the gap (experiment (f) names this as the exact missing upper-bound input too).

## The executable test battery

Any candidate construction, before any theory is evaluated, runs on the substrate (period lattice for both signs of $\Delta$, $\sigma$-function heights to $\sim$20 digits, closed-form and AFE $L$-values):

| Test | Input | Required output | Substrate reference |
|---|---|---|---|
| T1 nondegeneracy | 389a1, 433a1, 571a1, 643a1 | exact rational points, $\det R > 0$, matching (f)'s certified regulators at finite index | experiment (f) generators |
| T2 second-order tie | same curves | $\det R = \kappa \cdot$ leading coefficient to $\geq 10$ digits, $\kappa$ explicit | experiment (c) leading coefficients |
| T3 parity-blind family | the 11 blind twists of (g) + rank-0 twists in the same family | rank-2 certificates on the blind rows, no points on the rank-0 rows | experiment (g) table |
| T4 rank-1 degeneration | 37a1, 43a1, 53a1 | if $\mathcal{C}$ degenerates to one point, it must reproduce the measured GZ identity; it must NOT emit a fake second independent point (GKZ guard) | experiment (h) |

A candidate that passes T1 through T4 numerically is worth a theory investment; anything that fails T1 is the rank-1 machine again.

## Candidate input classes, scored

| Input class | Status | Risk profile |
|---|---|---|
| Heegner points over several fields | RETIRED: GKZ proportionality theorem, measured $\det = 0$ in (h) | was Detector 1-adjacent |
| Stark-Heegner / Darmon points (real quadratic) | conjectural rationality; still one point per field, and a GKZ-type proportionality for pairs is plausible and unexamined | repeats the one-derivative bottleneck |
| Generalized Heegner cycles (Bertolini-Darmon-Prasanna) | proven $p$-adic formulas, rank $\leq 1$ regime | input material, not a rank-2 output |
| Diagonal cycles (Gross-Kudla-Schoen, Darmon-Rotger) | one cycle controlled by a first central derivative of a triple-product $L$-function | a different bottleneck, same order |
| Kudla program / arithmetic theta series | the only systematic source of SECOND derivatives in arithmetic geometry today (codimension-2 special cycles vs second derivatives of Siegel-Eisenstein series) | the gap: from Eisenstein/orthogonal $L$ to $L(E,s)$, and from cycle classes to points; Detector 3 audit required |
| Higher-rank Euler systems (Beilinson-Flach etc.) | bound Selmer groups; no point construction | Direction 02's lane |

The Kudla row is the live one for Clause 2, and the surveyor pass on it is done (2026-06-11): see [`Kudla-2004-Special-Cycles-Derivatives-Eisenstein.md`](../reading_notes/Kudla-2004-Special-Cycles-Derivatives-Eisenstein.md). Verdict: structurally the right shape (codimension-$r$ cycles vs genus-$r$ Eisenstein series), Detector 1 and 3 clean, but everything PROVEN over number fields outputs first central derivatives; the two missing bridges are named in the note (Eisenstein-to-$L(E,s)$, and cycle-classes-to-points). The decisive context is the function-field side: Yun-Zhang prove the ALL-ORDERS formula $L^{(r)} \sim \langle[\mathrm{Sht}^r_T], [\mathrm{Sht}^r_T]\rangle$ for every $r$, so Clause 2's shape is realizable in principle, and the number-field wall is localized to exactly two imports (the $r$ moving legs over $X^r$, and the Frobenius twist in the shtuka definition): see [`Yun-Zhang-2017-Shtukas-Taylor-Expansion.md`](../reading_notes/Yun-Zhang-2017-Shtukas-Taylor-Expansion.md). Any Clause 2 candidate over $\mathbb{Q}$ must say what replaces those two imports; that question is the current sharpest form of Direction 01.

## Falsifiability trigger

If every input class above is shown to be parity-only (Detector 1), first-derivative-bottlenecked (Clause 2 failure, the GKZ pattern), or function-field-only (Detector 3), Direction 01 is retired in favor of the pure Sha-bounding route (Direction 02), and PHASE_STATE.md records which input class died last and why. The GKZ retirement of multi-field Heegner points is the template for what a clean kill looks like.

## Deliverable status

- This document is the formal spec (the missing Phase 1 deliverable; PHASE_STATE item 1).
- The Lean certificate exists as a `sorry` target: `rankTwoCertificate` in [`lean/BSD/RankEquality.lean`](../../../lean/BSD/RankEquality.lean) (two points, nonzero height-pairing determinant).
- The test battery T1 to T4 is runnable today against any candidate; no new substrate is required.
