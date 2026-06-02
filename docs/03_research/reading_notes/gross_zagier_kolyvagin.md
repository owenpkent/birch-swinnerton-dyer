# Reading note: Gross-Zagier + Kolyvagin (the proven rank <= 1 regime)

**Type:** THEOREM. **Regime:** analytic rank 0 and 1, archimedean. **Detector relevance:** defines the rank-boundary wall; clean against all three detectors but structurally capped at rank 1.

## Gross-Zagier (1986)

For $E/\mathbb{Q}$ modular of conductor $N$ and an imaginary quadratic field $K$ with a Heegner hypothesis (primes dividing $N$ split in $K$), the Heegner point $y_K \in E(K)$ has Neron-Tate height proportional to the first derivative of the $L$-function over $K$:
$$\hat{h}(y_K) = c \cdot L'(E/K, 1), \qquad c > 0.$$
So $y_K$ is non-torsion iff $L'(E/K, 1) \neq 0$. Combined with a suitable $K$, this handles analytic rank 1 over $\mathbb{Q}$.

## Kolyvagin (1990)

The Heegner point generates an Euler system of cohomology classes (derived classes from $y_K$ over ring class fields). Their norm-compatibility yields an annihilator of $\operatorname{Sel}$ and $\operatorname{Sha}$, proving: if $L'(E,1) \neq 0$ then $\operatorname{rank} E(\mathbb{Q}) = 1$ and $\operatorname{Sha}(E)$ is finite; if $L(E,1) \neq 0$ then rank 0 and finite Sha.

## The structural ceiling (the key reading)

The construction outputs ONE point $y_K$. A single point spans at most a rank-1 subgroup of $E(K)$. So the machine can certify rank exactly 1 ($y_K$ non-torsion) or rank 0 ($y_K$ torsion), but it can never produce two independent generators. This is not a soft limitation; it is intrinsic to the object. The Euler system inherits the same ceiling: it is built from $y_K$ and sees only the first-order analytic behavior.

## What this feeds

Research Direction 01 (specify the rank-2 object) is precisely the attempt to replace $y_K$ with something whose output is two independent points. The reading here fixes what the replacement must beat: the determinant of a $2 \times 2$ height-pairing matrix must be nonzero, which one point can never achieve.

## Caveats recorded

- Gross-Zagier is over $K$; descent to $\mathbb{Q}$ uses the sign of the functional equation and a choice of $K$ (Bump-Friedberg-Hoffstein, Murty-Murty, Waldspurger for the nonvanishing of the twisted $L$-value). All proven, all rank $\leq 1$.
- Finiteness of $\operatorname{Sha}$ from Kolyvagin is exactly the analytic rank $\leq 1$ statement. It says nothing in rank $\geq 2$.
