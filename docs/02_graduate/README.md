# Graduate: modularity, Heegner points, Selmer and Sha, the four-level framing

> Prerequisites: algebraic number theory, some algebraic geometry, Galois cohomology. Builds on [`docs/01_undergraduate/`](../01_undergraduate/); the frontier is [`docs/03_research/`](../03_research/).

## Modularity: where the L-function comes from

**Modularity theorem (Wiles; Taylor-Wiles; Breuil-Conrad-Diamond-Taylor 2001).** Every elliptic curve $E/\mathbb{Q}$ of conductor $N$ is modular: there is a weight-2 newform $f \in S_2(\Gamma_0(N))$ with $a_p(f) = a_p(E)$ for all $p$. Equivalently there is a non-constant morphism $X_0(N) \to E$ defined over $\mathbb{Q}$.

Consequence: $L(E, s) = L(f, s)$, and the latter has analytic continuation to all of $\mathbb{C}$ and a functional equation. Writing $\Lambda(E, s) = N^{s/2}(2\pi)^{-s}\Gamma(s) L(E, s)$,
$$\Lambda(E, s) = w \, \Lambda(E, 2 - s), \qquad w = \pm 1.$$
The center is $s = 1$, and $w = (-1)^{\operatorname{ord}_{s=1} L(E,s)}$. This is the analytic input BSD presupposes. The smoothed approximate functional equation in `experiments/_shared/elliptic_curve.py` evaluates $L(E, s)$ at the center using exactly this $\Lambda$.

## Selmer groups and the Tate-Shafarevich group

To bound the rank you study Galois cohomology. For an integer $m$, the short exact sequence $0 \to E[m] \to E \to E \to 0$ gives the Kummer sequence and a descent map. The **$m$-Selmer group** $\operatorname{Sel}_m(E)$ sits in
$$0 \to E(\mathbb{Q})/m E(\mathbb{Q}) \to \operatorname{Sel}_m(E) \to \operatorname{Sha}(E)[m] \to 0,$$
where the **Tate-Shafarevich group**
$$\operatorname{Sha}(E) = \ker\Big( H^1(\mathbb{Q}, E) \to \prod_v H^1(\mathbb{Q}_v, E) \Big)$$
measures the failure of the local-to-global (Hasse) principle: it classifies torsors over $E$ with points everywhere locally but no global point. $\operatorname{Sel}_m$ is computable; it bounds the rank from above. The gap between that bound and the true rank is exactly $\operatorname{Sha}(E)[m]$.

**Finiteness of Sha is the crux.** If $\operatorname{Sha}(E)$ is finite, descent computes the rank and the strong BSD formula is well-posed (the $\#\operatorname{Sha}$ factor is a finite integer, conjecturally a perfect square via the Cassels-Tate pairing). Finiteness is a THEOREM only for analytic rank $\leq 1$. In rank $\geq 2$ it is open. This is Detector 2 in the experimental thread.

## Heegner points and Gross-Zagier + Kolyvagin

For a curve of analytic rank 1, the proof of BSD is constructive:

1. **Heegner points.** Using complex multiplication on $X_0(N)$ and an imaginary quadratic field $K$ satisfying a Heegner hypothesis, one constructs a point $y_K \in E(K)$ as the image of a CM point under the modular parametrization.
2. **Gross-Zagier (1986).** The Neron-Tate height of $y_K$ is a nonzero multiple of $L'(E/K, 1)$:
$$\hat{h}(y_K) \doteq L'(E/K, 1).$$
So $y_K$ has infinite order exactly when $L'(E/K, 1) \neq 0$, i.e. when the analytic rank is 1.
3. **Kolyvagin (1990).** The Heegner point generates an **Euler system** of cohomology classes whose norm-compatibility bounds $\operatorname{Sha}$ and forces $\operatorname{rank} E(\mathbb{Q}) = 1$ with $\operatorname{Sha}$ finite.

**The structural ceiling.** The construction produces **one** point $y_K$. One point spans a rank-1 subgroup. It can certify rank exactly 1 (the point has infinite order) or rank 0 (the point is torsion), but it can never exhibit two independent generators. So the Heegner machine is intrinsically capped at rank 1. This is the rank-boundary wall.

## Iwasawa theory and the p-adic picture

For a prime $p$, $p$-adic $L$-functions $L_p(E, s)$ interpolate the special values, and the **Iwasawa Main Conjecture** relates $L_p$ to the characteristic ideal of a Selmer module. Kato's Euler system (one divisibility) plus Skinner-Urban 2014 (the reverse divisibility, under hypotheses) prove the main conjecture in many cases, yielding the $p$-part of strong BSD for analytic rank $\leq 1$. The **$p$-adic BSD** of Mazur-Tate-Teitelbaum handles the order of vanishing of $L_p$. What this does not give: the archimedean leading term, or unconditional Sha-finiteness in rank $\geq 2$.

## The four-level framing

It clarifies where BSD's difficulty actually sits to separate four levels of claim:

| Level | Claim | Status |
|---|---|---|
| L0 Parity | analytic rank $\equiv$ Mordell-Weil rank $\pmod 2$ | THEOREM (parity conjecture: Nekovar; Dokchitser-Dokchitser) |
| L1 Rank $\leq 1$ | full rank equality + finite Sha when analytic rank $\leq 1$ | THEOREM (Gross-Zagier + Kolyvagin) |
| L2 Rank $\geq 2$ | full rank equality + finite Sha when analytic rank $\geq 2$ | OPEN |
| L3 Strong form | exact leading-coefficient formula in all ranks | OPEN beyond rank $\leq 1$ ($p$-parts known) |

The content of BSD is the jump from L1 to L2. Parity (L0) is free from modularity. The hard object lives at L2: a construction of $\geq 2$ independent points, or a Sha bound, in the open regime.

## Statistical results

**Bhargava-Shankar:** the average rank of elliptic curves over $\mathbb{Q}$ (ordered by height) is bounded above (in fact below $1$); a positive proportion have rank 0 and a positive proportion have rank 1. **Bhargava-Skinner-Zhang:** a positive proportion of elliptic curves satisfy BSD. **Goldfeld's minimalist conjecture:** density $1/2$ each for rank 0 and rank 1. These are statements about the family, not about any single given $E$.

## The function-field template

Over a global function field $K = \mathbb{F}_q(C)$, $L(E, s)$ is a rational function of $q^{-s}$ (Grothendieck), so continuation and the functional equation are automatic, and BSD is a theorem assuming the Tate-Shafarevich (equivalently Brauer) group of the associated elliptic surface is finite (Tate; Artin-Tate; Milne 1975). This is the cleanest picture of "what a complete proof looks like," computed from etale cohomology of a surface. It is a template, not a proof over $\mathbb{Q}$: there is no base curve $C$ and no geometric Frobenius over $\mathbb{Q}$. Detector 3 guards against importing it silently.
