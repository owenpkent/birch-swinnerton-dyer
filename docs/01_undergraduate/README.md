# Undergraduate: elliptic curves, the group law, and the L-series

> Prerequisites: calculus, modular arithmetic, basic group theory. Builds on [`docs/00_intuitive/`](../00_intuitive/); the next level is [`docs/02_graduate/`](../02_graduate/).

## Elliptic curves and the Weierstrass equation

An elliptic curve over $\mathbb{Q}$ is a smooth projective curve of genus 1 with a chosen rational base point. Concretely it is the set of solutions to a **Weierstrass equation**
$$E: y^2 + a_1 xy + a_3 y = x^3 + a_2 x^2 + a_4 x + a_6, \qquad a_i \in \mathbb{Q},$$
together with a point at infinity $O$. Smoothness is the condition that the discriminant $\Delta \neq 0$. Over a field of characteristic not 2 or 3 you can complete the square and cube to reach the short form $y^2 = x^3 + Ax + B$.

## The group law

The chord-and-tangent construction makes the rational points $E(\mathbb{Q})$ into an abelian group with identity $O$:

- to add $P$ and $Q$, draw the line through them, take the third intersection $R$, and reflect over the $x$-axis to get $P + Q$;
- the tangent line at $P$ gives $2P$ (doubling);
- $O$ is the identity; the reflection of $P$ is $-P$.

These operations are given by rational functions of the coordinates, so the sum of rational points is rational. Associativity is the nontrivial fact (it follows from the Riemann-Roch theorem, or by a direct but tedious computation).

## The Mordell-Weil theorem

**Theorem (Mordell 1922, Weil 1928).** $E(\mathbb{Q})$ is a finitely generated abelian group:
$$E(\mathbb{Q}) \cong \mathbb{Z}^r \oplus E(\mathbb{Q})_{\mathrm{tors}}.$$
The integer $r \geq 0$ is the **rank**. The torsion subgroup $E(\mathbb{Q})_{\mathrm{tors}}$ is finite, and by Mazur's theorem it is one of a short explicit list (cyclic of order 1 to 10 or 12, or $\mathbb{Z}/2 \times \mathbb{Z}/2m$ for $m \leq 4$).

The rank is the hard invariant. There is no known algorithm guaranteed to compute it for every curve. That gap is exactly what BSD addresses.

## Counting points mod p

For a prime $p$ of good reduction (one not dividing the conductor $N$), reduce the equation mod $p$ and count solutions over $\mathbb{F}_p$. Define
$$a_p = p + 1 - \#E(\mathbb{F}_p).$$
**Hasse's theorem** bounds it: $|a_p| \leq 2\sqrt{p}$. So $a_p$ measures how the actual count deviates from the "expected" $p + 1$. Heuristically, a curve with many rational points has more points mod $p$ on average, so $a_p$ trends positive, and the $L$-function below is larger.

This $a_p$ is exactly what `experiments/_shared/elliptic_curve.py` computes by honest enumeration.

## The Hasse-Weil L-function

Package the local data into an Euler product. At a good prime,
$$L_p(E, s) = \left(1 - a_p p^{-s} + p^{1 - 2s}\right)^{-1},$$
and at bad primes the local factor is $\left(1 - a_p p^{-s}\right)^{-1}$ with $a_p \in \{-1, 0, +1\}$ (split multiplicative, non-split multiplicative, additive). Then
$$L(E, s) = \prod_p L_p(E, s) = \sum_{n \geq 1} \frac{a_n}{n^s},$$
where the $a_n$ are built multiplicatively from the $a_p$ (the recurrence $a_{p^{k+1}} = a_p a_{p^k} - p\, a_{p^{k-1}}$ at good primes). The product and series converge only for $\operatorname{Re}(s) > 3/2$ by Hasse's bound.

## The central point and the conjecture

BSD lives at $s = 1$, the center of the critical strip. But the series above does not converge there, so you need to continue $L(E, s)$ analytically first. That continuation is not elementary: it comes from **modularity** (next level). Granting it,

> **Weak BSD:** $\operatorname{ord}_{s=1} L(E, s) = r$, the rank.

The order of vanishing is the **analytic rank**. The experiments compute it from derivatives of $L$ at $s = 1$.

## The root number and parity

Modularity gives a functional equation relating $L(E, s)$ to $L(E, 2 - s)$, with a sign $w = \pm 1$ called the **root number**. The sign forces
$$w = (-1)^{\text{analytic rank}}.$$
So $w$ tells you the analytic rank mod 2 for free: $w = +1$ means even, $w = -1$ means odd. This is powerful but partial: it cannot tell rank 0 from rank 2. Holding that thought is the entire point of the parity-only detector.

## Try it

```powershell
python -m experiments.l_function_rank.e_a_analytic_rank
```
computes the analytic rank from $L$-derivatives for curves of rank 0, 1, 2, 3 and checks it against the Mordell-Weil rank.
