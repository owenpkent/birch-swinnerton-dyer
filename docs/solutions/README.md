# Solutions: known approaches to BSD and their obstructions

> The per-approach catalog. For each candidate proof architecture: what it is, what it proves, where it stops, and which detector catches the gap. The strategic overview is in [`docs/research_atlas/README.md`](../research_atlas/README.md).

## 1. Modularity (Wiles; Taylor-Wiles; BCDT 2001)

**What it is.** Every $E/\mathbb{Q}$ is modular: $L(E, s) = L(f, s)$ for a weight-2 newform $f$. **Proves.** Analytic continuation of $L(E, s)$ to $\mathbb{C}$, the functional equation $\Lambda(E, s) = w\,\Lambda(E, 2 - s)$, and the root number $w = (-1)^{\text{analytic rank}}$. **Stops at.** The rank mod 2. It cannot separate rank 0 from 2. **Detector.** Detector 1 (parity-only). Modularity is the prerequisite that makes $s = 1$ a meaningful point at all; it is not itself a route to the rank.

## 2. Heegner points + Gross-Zagier + Kolyvagin

**What it is.** A Heegner point $y_K \in E(K)$ with $\hat{h}(y_K) \doteq L'(E/K, 1)$, plus Kolyvagin's Euler system. **Proves.** Full BSD (rank equality + finite Sha) for analytic rank 0 and 1. The only fully proven regime over $\mathbb{Q}$. **Stops at.** Rank 1: one Heegner point is a rank-1 object and cannot exhibit two independent generators. **Obstruction.** The rank-boundary wall itself. See [`docs/03_research/reading_notes/gross_zagier_kolyvagin.md`](../03_research/reading_notes/gross_zagier_kolyvagin.md).

## 3. Iwasawa theory / main conjectures (Mazur; Kato; Skinner-Urban 2014)

**What it is.** $p$-adic $L$-functions and the main conjecture relating $\operatorname{Sel}$ to $L_p$. **Proves.** The $p$-part of strong BSD in many rank $\leq 1$ cases; the $p$-adic BSD order of vanishing (Mazur-Tate-Teitelbaum, Greenberg-Stevens). **Stops at.** The archimedean leading term and unconditional Sha-finiteness in rank $\geq 2$. **Detector.** Detector 2 (Sha-finiteness). See [`docs/03_research/reading_notes/iwasawa_skinner_urban.md`](../03_research/reading_notes/iwasawa_skinner_urban.md).

## 4. Euler systems (Kolyvagin, Kato)

**What it is.** Norm-compatible cohomology classes annihilating $\operatorname{Sel}$ / $\operatorname{Sha}$. **Proves.** Sharp bounds in rank $\leq 1$ (Heegner) and one divisibility of the main conjecture (Kato). **Stops at.** Rank 1: the known systems see only first-order analytic behavior. **Obstruction.** A rank $\geq 2$ Euler system is the missing object. See Research Direction 02.

## 5. Statistics / averages (Bhargava-Shankar; Bhargava-Skinner-Zhang)

**What it is.** Bounded average Selmer size, hence bounded average rank; positive proportion satisfying BSD. **Proves.** BSD for a positive proportion of curves; average rank bounded. **Stops at.** It is a statement about the family, not about a given $E$. **Note.** Not a single-detector failure; it is a different kind of claim (population, not pointwise).

## 6. Function-field analog (Tate; Artin-Tate; Milne 1975)

**What it is.** BSD over $\mathbb{F}_q(C)$ from etale cohomology of the elliptic surface, under finite Brauer/Tate-Shafarevich group. **Proves.** Full BSD in the geometric case. **Stops at.** It is a template, not a proof over $\mathbb{Q}$: no base curve, no geometric Frobenius. **Detector.** Detector 3 (function-field mirage). See [`docs/03_research/reading_notes/statistics_function_field.md`](../03_research/reading_notes/statistics_function_field.md).

## The synthesis

Each approach is a coordinate. Modularity gives parity (L0). Heegner gives rank $\leq 1$ (L1). Statistics gives a positive proportion of the family. The function-field analog gives the template. None reaches an arbitrary rank $\geq 2$ curve (L2), which is exactly where a proof must build the missing object: two independent points or an unconditional Sha bound in the open regime.
