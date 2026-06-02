# Direction 01: specify the rank-2 object

> The most-leveraged move in the program. Write down precisely what a rank-2 generalization of the Heegner-point construction must produce, then run the specification through Detector 1 (parity-only) and Detector 3 (function-field mirage). Cheap, high-information.

## Why this first

The Heegner construction produces one point and so is capped at rank 1. The entire open part of BSD is the rank $\geq 2$ regime. Before attempting any construction, we should pin down exactly what success would look like, so that any candidate can be tested against a fixed target rather than a vague aspiration.

## The specification (what the object must produce)

A construction $\mathcal{C}$ taking a curve $E/\mathbb{Q}$ of analytic rank $\geq 2$ to data on $E$, such that:

1. **Two independent points.** $\mathcal{C}$ outputs points $P_1, P_2 \in E(\mathbb{Q})$ (or in $E(K)$ for a controlled $K$, with a descent back to $\mathbb{Q}$) that are provably independent in $E(\mathbb{Q}) \otimes \mathbb{Q}$. Independence must be certified, e.g. by a $2 \times 2$ height-pairing matrix with nonzero determinant.
2. **Tied to the analytic side.** The independence must be forced by $L$-function data of order $\geq 2$ (a second-order Gross-Zagier-type formula), not assumed.
3. **A Sha bound.** Either $\mathcal{C}$ also produces an Euler system bounding $\operatorname{Sha}$, or it is paired with Direction 02.

## Detector checks the spec must pass

- **Detector 1 (parity-only).** The output must be the exact rank-2 certificate (two independent points), not a parity statement. A construction that, after analysis, only reproduces $w = +1$ has failed: $w = +1$ is consistent with rank 0, 2, 4, ...
- **Detector 3 (function-field mirage).** The construction must use an input that exists over $\mathbb{Q}$. If the only way to produce $P_1, P_2$ is via a geometric Frobenius or a base curve $C$, it is a function-field object and has not crossed the gap. Over $\mathbb{F}_q(C)$ such higher-rank constructions exist (the surface has enough cohomology); the test is whether the $\mathbb{Q}$-version survives without that geometry.

## Known obstructions to anticipate

- A naive "two Heegner points from two imaginary quadratic fields" is not independent in general; the heights relate to $L'$ over each field, and both can be forced by the same rank-1 phenomenon. The spec must rule this out via the determinant condition.
- Generalized Heegner cycles (Bertolini-Darmon-Prasanna) and Darmon's Stark-Heegner points are candidate inputs, but their rationality and independence in the relevant regime are themselves open. Cite them as inputs, not as solved.

## Falsifiability trigger

If every candidate input to $\mathcal{C}$ is shown to be either parity-only (Detector 1) or function-field-only (Detector 3), Direction 01 is retired in favor of a pure Sha-bounding route (Direction 02), and PHASE_STATE.md records the failure mode (which input class is missing).

## Deliverable

A short formal spec document plus a Lean statement of the rank-2 certificate (two points with nonzero height-pairing determinant) in [`lean/BSD/RankEquality.lean`](../../../lean/BSD/RankEquality.lean), stated as a `sorry` target.
