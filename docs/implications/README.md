# Implications: why BSD matters

> What a proof (or the existing partial results) buys us, across number theory, computation, and cryptography.

## A computable handle on rank

There is no algorithm known to compute $\operatorname{rank} E(\mathbb{Q})$ for every curve with a guaranteed answer. Descent gives an upper bound via the Selmer group; the gap is $\operatorname{Sha}$. BSD, granting finite $\operatorname{Sha}$, turns the rank into something you can read off an analytic computation: compute $L(E, s)$ near $s = 1$, count the order of vanishing, done. The experiments here do exactly this on a bundled table. Without BSD, a low point-count is ambiguous (low rank, or huge generators?); with it, the analytic rank settles the matter.

## Diophantine equations and the congruent number problem

Whether $n$ is a **congruent number** (the area of a right triangle with rational sides) is equivalent to the curve $y^2 = x^3 - n^2 x$ having positive rank. Tunnell's theorem (1983), conditional on BSD, gives a simple finite criterion in terms of counting representations by ternary quadratic forms. So BSD converts an ancient Diophantine question into a finite computation. Many such problems (rational points on specific cubics, ranks in families) inherit decidability from BSD.

## The strong form: an exact arithmetic identity

The strong form is not just "rank = analytic rank." It pins a transcendental quantity (the leading Taylor coefficient of $L$) to a product of arithmetic invariants: period, regulator, Tamagawa numbers, $\#\operatorname{Sha}$, torsion. This makes $\#\operatorname{Sha}$ (otherwise hard to compute) readable from analytic data, and conversely lets analytic computations predict and verify Sha. Experiment (c) exploits exactly this: it solves the formula for $\#\operatorname{Sha}$ and checks the answer is a perfect square.

## Cryptography (indirect)

Elliptic-curve cryptography rests on the hardness of the discrete log problem on $E(\mathbb{F}_p)$, not directly on BSD. But the broader theory BSD sits in (point counting, $L$-functions, the arithmetic of $E$ over number fields) is the same machinery that underpins curve selection, pairing-based cryptography, and the security analysis of curves. BSD's experimental thread (point counting, Sato-Tate) exercises the same $a_p$ pipeline that cryptographic point-counting (Schoof-Elkies-Atkin) optimizes.

## A Rosetta stone between analysis and arithmetic

The deepest implication is conceptual. BSD is one of the central instances of the philosophy that $L$-functions encode arithmetic: special values of analytic objects determine the structure of solution sets. It is a concrete, testable case of the Langlands program's promise and of the Beilinson-Bloch-Kato conjectures on special values. A proof would be a landmark confirmation that the analytic and arithmetic worlds are genuinely one.

## The honest scope

The proven results (ranks 0 and 1) already deliver real consequences: Tunnell's criterion, positive-proportion BSD (Bhargava-Skinner-Zhang), and decidability in many families. The open rank $\geq 2$ case is where a general "compute the rank from the $L$-function" guarantee still awaits the missing construction.
