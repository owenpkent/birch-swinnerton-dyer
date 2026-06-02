# Direction 02: a rank >= 2 Euler system bounding Sha

> Open question. Kolyvagin's and Kato's Euler systems bound $\operatorname{Sha}$ and the Selmer group, but both are tied to rank $\leq 1$ or the analytic side. The missing object is an Euler system that bounds $\operatorname{Sha}$ unconditionally in the rank $\geq 2$ regime.

## The target

An Euler system is a norm-compatible family of Galois cohomology classes $\{c_F\}$ indexed by abelian extensions $F/\mathbb{Q}$, satisfying explicit norm relations, from which one derives an annihilator of $\operatorname{Sel}$ / $\operatorname{Sha}$. Kolyvagin's system is built from Heegner points (rank-1 input); Kato's from Beilinson elements / Siegel units (gives one divisibility in the main conjecture). Neither, as known, certifies $\operatorname{Sha}$ finite in rank $\geq 2$.

We want a system whose derived bound is sharp enough to force $\#\operatorname{Sha} < \infty$ on a curve of analytic rank $\geq 2$, without assuming finiteness as input.

## Detector checks

- **Detector 2 (Sha-finiteness).** The whole point: the system must PROVE finiteness, not assume it. Any step that uses $\operatorname{Sha}[p^\infty]$ cofinite or similar in the rank $\geq 2$ regime fails the detector.
- **Detector 3 (function-field mirage).** Over $\mathbb{F}_q(C)$, finiteness of the Brauer group gives the bound via etale cohomology of the surface. A number-field Euler system must not be a disguised version of that cohomological argument.

## Why it is hard

Euler systems give bounds proportional to the order of vanishing of an associated $L$-value, but the rank-1 systems "see" only the first derivative. A genuine rank $\geq 2$ system would need norm relations sensitive to a second-order phenomenon. No such system is known. Generalized Kato classes and the work around the elliptic Stark conjecture (Darmon-Lauder-Rotger) are the closest live inputs, and their behavior in rank 2 is partially conjectural.

## Falsifiability trigger

If the candidate system's bound is shown to degenerate to the rank-1 bound (i.e. it cannot exceed the proven regime), the direction is retired and the failure recorded.

## Deliverable

A reading-notes synthesis of the known systems and a precise statement of the norm relations a rank $\geq 2$ system would have to satisfy.
