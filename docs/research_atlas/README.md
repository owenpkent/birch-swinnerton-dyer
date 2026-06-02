# Research Atlas: the master map of BSD approaches

> The strategic reference for the whole repo. Every known approach to BSD, what it proves, where it stops, and which wrong-approach detector catches its failure mode. Start here for the landscape; go to [`docs/solutions/`](../solutions/) for per-approach detail and [`docs/03_research/`](../03_research/) for the proof program.

## The statement, pinned

**Weak BSD.** For an elliptic curve $E/\mathbb{Q}$,
$$\operatorname{ord}_{s=1} L(E, s) = \operatorname{rank} E(\mathbb{Q}).$$
The left side is the analytic rank (order of vanishing of the Hasse-Weil $L$-function at the central point $s = 1$). The right side is the Mordell-Weil rank.

**Strong BSD.** With $r = \operatorname{rank} E(\mathbb{Q})$,
$$\lim_{s \to 1} \frac{L(E, s)}{(s-1)^r} = \frac{\Omega_E \cdot \operatorname{Reg}_E \cdot \prod_p c_p \cdot \#\operatorname{Sha}(E)}{(\#E(\mathbb{Q})_{\mathrm{tors}})^2},$$
where $\Omega_E$ is the real period, $\operatorname{Reg}_E$ the regulator of the Neron-Tate height pairing, $c_p$ the Tamagawa numbers, $\#E(\mathbb{Q})_{\mathrm{tors}}$ the order of the torsion subgroup, and $\operatorname{Sha}(E)$ the Tate-Shafarevich group. The formula presupposes $\operatorname{Sha}(E)$ is finite.

## What is proven, exactly

| Regime | Status | By whom |
|---|---|---|
| Analytic rank 0 | Rank equality + finite Sha + strong-form $p$-part (many $p$) PROVEN | Coates-Wiles (rank 0 part, CM), Kolyvagin, Rubin, Kato, Skinner-Urban |
| Analytic rank 1 | Rank equality + finite Sha PROVEN | Gross-Zagier 1986 + Kolyvagin 1990 |
| Analytic rank $\geq 2$ | OPEN. Neither rank equality nor finite Sha is known | -- |
| Modularity of $E/\mathbb{Q}$ | THEOREM (gives continuation + functional equation + root number) | Wiles; Taylor-Wiles; Breuil-Conrad-Diamond-Taylor 2001 |
| Parity conjecture | THEOREM (rank mod 2 matches analytic rank mod 2) | Nekovar; T. and V. Dokchitser |
| BSD over $\mathbb{F}_q(C)$ | THEOREM under finite Sha (template, not a proof over $\mathbb{Q}$) | Tate; Artin-Tate; Milne 1975 |
| Population statements | Positive proportion of $E/\mathbb{Q}$ satisfy BSD; average rank bounded | Bhargava-Shankar; Bhargava-Skinner-Zhang |

## The architectures and their walls

| # | Architecture | Reaches | The wall | Detector that catches it |
|---|---|---|---|---|
| 1 | **Modularity** (Wiles; BCDT) | analytic continuation, functional equation, root number $w$ | gives rank mod 2 only, not the rank | Detector 1 (parity-only) |
| 2 | **Heegner / Gross-Zagier + Kolyvagin** | rank 0 and 1, fully (rank equality + finite Sha) | a single Heegner point is a rank-1 object; cannot exhibit two independent generators | the rank-boundary wall itself |
| 3 | **Iwasawa theory / main conjectures** (Mazur; Kato; Skinner-Urban) | $p$-part of strong BSD in many rank $\leq 1$ cases; $p$-adic BSD | archimedean leading term and unconditional Sha-finiteness in rank $\geq 2$ | Detector 2 (Sha) |
| 4 | **Euler systems** (Kolyvagin, Kato) | bounds on Selmer / Sha | known systems are tied to rank $\leq 1$ or the analytic side; a higher-rank system is missing | the rank-boundary wall |
| 5 | **Statistics / averages** (Bhargava et al.) | positive proportion satisfy BSD; bounded average rank | a statement about the family, not about a given $E$ | (no single detector; it is a different kind of claim) |
| 6 | **Function-field analog** (Tate; Artin-Tate) | full BSD over $\mathbb{F}_q(C)$ under finite Sha | imports a geometric Frobenius the number-field case lacks | Detector 3 (function-field mirage) |

## The cross-cutting thesis

**The rank-boundary thesis.** Every proven technique bottoms out at analytic rank 1 because its engine is a rank-1 object (one Heegner point, one Euler system class tied to it). A general proof must construct something new in the rank $\geq 2$ regime: either a construction producing $\geq 2$ independent rational points (a higher-rank analog of the Heegner point), or an Euler system bounding Sha unconditionally in rank $\geq 2$.

## The one missing object

A construction that, on a rank $\geq 2$ curve, produces two provably independent rational points OR bounds $\operatorname{Sha}$ unconditionally. Untouched at the construction level. Multi-year, multi-person.

## How to read the rest of the repo

- Per-approach detail and obstructions: [`docs/solutions/`](../solutions/).
- The proof program and research-grade specs: [`docs/03_research/`](../03_research/).
- Why it matters: [`docs/implications/`](../implications/).
- The computational thread that validates the substrate: [`experiments/PLAN.md`](../../experiments/PLAN.md).
- Operating philosophy: [`docs/researcher_mindset.md`](../researcher_mindset.md).
