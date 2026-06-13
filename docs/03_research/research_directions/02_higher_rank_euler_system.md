# Direction 02: a rank >= 2 Euler system bounding Sha

> Open question. Kolyvagin's and Kato's Euler systems bound $\operatorname{Sha}$ and the Selmer group, but both are tied to rank $\leq 1$ or the analytic side. The missing object is an Euler system that bounds $\operatorname{Sha}$ unconditionally in the rank $\geq 2$ regime.

## The target

An Euler system is a norm-compatible family of Galois cohomology classes $\{c_F\}$ indexed by abelian extensions $F/\mathbb{Q}$, satisfying explicit norm relations, from which one derives an annihilator of $\operatorname{Sel}$ / $\operatorname{Sha}$. Kolyvagin's system is built from Heegner points (rank-1 input); Kato's from Beilinson elements / Siegel units (gives one divisibility in the main conjecture). Neither, as known, certifies $\operatorname{Sha}$ finite in rank $\geq 2$.

We want a system whose derived bound is sharp enough to force $\#\operatorname{Sha} < \infty$ on a curve of analytic rank $\geq 2$, without assuming finiteness as input.

## Architecture-4 detector scorecard (Euler systems)

Scored against the three detectors and the rank control pair. Reading notes behind the rows: [Kolyvagin 1990](../reading_notes/Kolyvagin-1990-Euler-Systems.md) (the Heegner-point system), [Coates-Wiles 1977](../reading_notes/Coates-Wiles-1977-BSD.md) (elliptic units, rank 0), and Kato's Beilinson-element system (via the [Skinner-Urban note](../reading_notes/Skinner-Urban-2014-Iwasawa-Main-GL2.md), which uses Kato's divisibility).

| Detector | Verdict | Where exactly |
|---|---|---|
| **1 (parity-only)** | PASSES | Each known system produces an exact rank value and exact triviality of $\operatorname{Sha}_p$ (Kolyvagin: $\operatorname{Sel}_p$ cyclic, rank $1$), not rank mod 2. Strictly finer than the root number. |
| **2 (Sha-finiteness)** | THE WALL, and the point of the direction | Kolyvagin's system PROVES $\#\operatorname{Sha}<\infty$ but only because it has a single non-torsion seed (the Heegner point), so it certifies rank $\leq 1$; the Selmer bound $\dim\operatorname{Sel}_p \leq 1 + 2\operatorname{ord}_p[\cdots]$ is finite precisely because there is one degree of freedom. Kato's system gives one divisibility (analytic side bounds algebraic), tied to the order of vanishing it sees, which is $\leq 1$. A genuine rank-$\geq 2$ system must prove finiteness with $\geq 2$ seeds; none is known. |
| **3 (function-field mirage)** | PASSES, with the contrast named | Over $\mathbb{F}_q(C)$ finiteness of $\operatorname{Br}(X)$ (Tate/Milne) gives the bound via etale cohomology of the surface, rank-uniformly; the number-field Euler system is genuinely number-field-native (Chebotarev over $K(E_p)$, Tate local duality) and must not be a disguised surface argument. The contrast localizes what $\mathbf{Q}$ lacks: a second cohomological degree of freedom the geometric Frobenius supplies for free. |
| **Control pair** | proven side; structural ceiling is one seed | The axioms (norm relation $\operatorname{Tr}_\ell y_n = a_\ell y_m$, Frobenius congruence, sign $\epsilon_n$) specify exactly what a rank-$\geq 2$ system must reproduce; the known systems satisfy them with a single class and so cap at rank $1$. |

## What a rank $\geq 2$ system must satisfy

A norm-compatible family $\{c_F\}$ whose derived classes span a $\geq 2$-dimensional subspace of $\operatorname{Sel}_p(E/\mathbb{Q})$, with norm relations sensitive to the *second-order* vanishing of the associated $L$-value (the rank-1 systems "see" only the first derivative). The closest live inputs are generalized Kato classes and the elliptic Stark conjecture (Darmon-Lauder-Rotger), whose rank-2 behavior is partially conjectural. Computationally, experiment (j) ([`two_descent/`](../../../experiments/two_descent/)) exhibits the one-seed ceiling from the descent side: where a rational $2$-isogeny exists the Selmer bound is two-sided and pins the rank ($\operatorname{rank} E_{34} = 2$), but the rank-$\geq 2$ bundled curves carry no such isogeny, so the elementary system does not even start.

## Why it is hard

Euler systems give bounds proportional to the order of vanishing of an associated $L$-value, but the rank-1 systems "see" only the first derivative. A genuine rank $\geq 2$ system would need norm relations sensitive to a second-order phenomenon. No such system is known. Generalized Kato classes and the work around the elliptic Stark conjecture (Darmon-Lauder-Rotger) are the closest live inputs, and their behavior in rank 2 is partially conjectural.

## Falsifiability trigger

If the candidate system's bound is shown to degenerate to the rank-1 bound (i.e. it cannot exceed the proven regime), the direction is retired and the failure recorded.

## Deliverable

A reading-notes synthesis of the known systems and a precise statement of the norm relations a rank $\geq 2$ system would have to satisfy.
