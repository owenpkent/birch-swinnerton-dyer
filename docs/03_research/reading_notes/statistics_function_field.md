# Reading note: statistics and the function-field template

**Type:** THEOREM (population-level; and the function-field analog). **Regime:** the family of all $E/\mathbb{Q}$; and $\mathbb{F}_q(C)$. **Detector relevance:** Detector 3 (the function-field analog is the template, not a proof over $\mathbb{Q}$).

## Bhargava-Shankar (average rank)

Ordering elliptic curves over $\mathbb{Q}$ by height, the average size of the $n$-Selmer group is bounded for $n = 2, 3, 4, 5$, which bounds the average rank. The average rank is less than $1$ (in fact $\leq 7/6$ from 2-Selmer, improved with higher $n$). A positive proportion have rank 0 (with $\operatorname{Sha}$ trivial) and a positive proportion have rank 1.

## Bhargava-Skinner-Zhang (positive proportion satisfy BSD)

Combining the Selmer averages with Gross-Zagier-Kolyvagin and Skinner-Urban, a positive proportion (over $66\%$) of elliptic curves over $\mathbb{Q}$ satisfy BSD (rank equality and the relevant finiteness). Crucially this is a statement about the FAMILY, not about a given curve: it does not tell you whether your specific $E$ satisfies BSD.

## Goldfeld's minimalist conjecture

Conjecturally (not proven), density $1/2$ each for rank 0 and rank 1, so rank $\geq 2$ is a density-zero phenomenon. This is consistent with the rank-boundary thesis: the hard regime is rare but is exactly where the open problem lives.

## The function-field template (Tate; Artin-Tate; Milne 1975)

For $E$ over $K = \mathbb{F}_q(C)$, $L(E, s)$ is a rational function of $q^{-s}$ (Grothendieck's cohomological formula), so continuation and the functional equation are free. BSD (rank equality and the leading-coefficient formula) is a THEOREM provided the Tate-Shafarevich (equivalently Brauer) group of the associated elliptic surface $\mathcal{E} \to C$ is finite, and $\#\operatorname{Sha}$ is the order of a finite group read off from etale cohomology of the surface.

## The gap (the reading)

Over $\mathbb{Q}$ there is no base curve $C$, no elliptic surface, and no geometric Frobenius. The function-field proof is cohomology of a surface; the number-field case lacks the surface. This is why Detector 3 matters: any number-field argument that runs verbatim over $\mathbb{F}_q(C)$ has silently used the geometry the rationals do not have. The template tells us what a complete proof looks like; it does not hand us one.
