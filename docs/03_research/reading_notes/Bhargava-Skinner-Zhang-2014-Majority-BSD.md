# Reading note: M. Bhargava, C. Skinner, W. Zhang, "A majority of elliptic curves over $\mathbb{Q}$ satisfy the Birch and Swinnerton-Dyer conjecture," arXiv:1407.1826v2 (July 2014)

> **Role in the BSD program.** This is the keystone *population-level* result for the proven regime. It proves that a positive, explicitly bounded proportion (more than $66.48\%$) of all $E/\mathbb{Q}$, ordered by naive height, satisfy the BSD *rank* conjecture ($\operatorname{rk}(E) = \operatorname{rk_{an}}(E)$) and have finite $\operatorname{Sha}$. The proof is a synthesis: it feeds the Bhargava-Shankar average $p$-Selmer sizes (for $p = 2, 3, 5$) into $p$-adic rank criteria that themselves rest on Gross-Zagier-Kolyvagin, Shouwu Zhang's Shimura-curve extension, the Skinner-Urban / Skinner cyclotomic main conjecture, the Skinner-Zhang and W. Zhang indivisibility-of-Heegner-points results, and the Skinner converse theorem. Crucially every certified curve is *individually* rank $0$ or rank $1$. The theorem certifies no rank $\geq 2$ curve, and by construction it cannot: each ingredient is a rank-$\leq 1$ criterion.
>
> **Reading depth.** Read from the downloaded arXiv PDF (17 pages, v2), full text: Section 1 (Introduction, Theorems 1-3, Corollary 4, pp. 1-3), Section 2 (Preliminaries, Theorems 5/9/13/15/16, pp. 3-6), Section 3 (Proofs, Lemmas 17-20, Theorems 21/23/25, Corollaries 22/24/26, pp. 7-14), Section 4 (Conclusion, conditional Theorem 27, pp. 14-15), References (pp. 15-17). Exact theorem numbers and page numbers below are taken from the PDF.
>
> **Cross-links.** Four-level framing: this sits at the *population* layer, orthogonal to the per-curve hard content in [`docs/02_graduate/`](../../02_graduate/); it does not touch the rank $\geq 2$ object at all. Three detectors: [`experiments/_shared/controls.py`](../../../experiments/_shared/controls.py). Research directions: [`01_rank_two_object.md`](../research_directions/01_rank_two_object.md) (the complementary $< 33.52\%$ is where the rank $\geq 2$ object must live), [`02_higher_rank_euler_system.md`](../research_directions/02_higher_rank_euler_system.md) (every $p$-adic criterion here degenerates at rank $\geq 2$), [`03_padic_archimedean.md`](../research_directions/03_padic_archimedean.md) (the proof is a $p$-adic-criterion + archimedean-input hybrid). Atlas: [`docs/research_atlas/README.md`](../../research_atlas/README.md), statistics/averages row.
>
> **Relation to sibling notes.** Companion to [`statistics_function_field.md`](statistics_function_field.md), which summarizes Bhargava-Shankar and this paper in one paragraph each; this note is the deep version of that paper's middle paragraph. It depends logically on [`gross_zagier_kolyvagin.md`](gross_zagier_kolyvagin.md) (the rank-$\leq 1$ wall it certifies *up to*) and on [`iwasawa_skinner_urban.md`](iwasawa_skinner_urban.md) (the main-conjecture machinery powering the rank-0 criterion). Topic folder: [`references/05_statistics_averages/`](../../../references/05_statistics_averages/).

## One-line takeaway

By averaging $5$-Selmer sizes over large congruence families and combining with $p$-adic sufficient conditions for rank exactly $0$ or exactly $1$ (each of which is downstream of Gross-Zagier-Kolyvagin and the main conjecture), the authors prove $> 66.48\%$ of $E/\mathbb{Q}$ have $\operatorname{rk} = \operatorname{rk_{an}} \in \{0, 1\}$ and finite $\operatorname{Sha}$, an honest *positive-density* theorem that nonetheless certifies zero curves in the open rank $\geq 2$ regime and whose proportion is, structurally, exactly the slice the rank-$\leq 1$ machine can reach.

## Technical content (section by section)

### Section 1: Introduction (pp. 1-3)

Curves are normalized as $E_{A,B} : y^2 = x^3 + Ax + B$ with $A, B \in \mathbb{Z}$ and the minimality condition $p^6 \nmid B$ whenever $p^4 \mid A$. The **naive height** is
$$H(E_{A,B}) := \max\{4|A|^3,\, 27 B^2\},$$
and "ordered by height" everywhere means this $H$.

- **Theorem 1 (p. 1).** A majority of $E/\mathbb{Q}$, ordered by height, satisfy the BSD *rank* conjecture (the rank equality $\operatorname{rk}(E) = \operatorname{rk_{an}}(E)$, where $\operatorname{rk_{an}}$ is the order of vanishing of $L(E, s)$ at $s = 1$; $L$ is entire by modularity, refs [28, 25, 7] = Wiles, Taylor-Wiles, Breuil-Conrad-Diamond-Taylor).
- **Theorem 2 (p. 2).** A majority of $E/\mathbb{Q}$, ordered by height, have *finite* Tate-Shafarevich group $\operatorname{Sha}(E)$.
- The quantitative form (display (1), p. 2):
$$\liminf_{X \to \infty} \frac{\#\{E/\mathbb{Q} : \operatorname{rk}(E) = \operatorname{rk_{an}}(E),\ \operatorname{Sha}(E)\text{ finite},\ H(E) < X\}}{\#\{E/\mathbb{Q} : H(E) < X\}} > 66.48\%.$$
  The authors note this percentage "can likely be improved."
- **Theorem 3 (p. 2).** At least $16.50\%$ of $E/\mathbb{Q}$ have both algebraic and analytic rank $0$; at least $20.68\%$ have both algebraic and analytic rank $1$.
- **Corollary 4 (p. 2).** The $\liminf$ of the average (algebraic or analytic) rank is $\geq 0.2068$. (Note: the two percentages in Theorem 3 sum to $37.18\%$, *less* than the $66.48\%$ of Theorem 1; the gap is because the rank "$0$ *or* $1$" count is proven with a better bound than the sum of the two separate counts.)

The introduction is explicit about the input chain (p. 2): refs [21] (Skinner, multiplicative reduction + cyclotomic main conjecture) and [22] (Skinner-Urban, Iwasawa main conjectures for $\mathrm{GL}_2$) give sufficient $p$-adic conditions for rank $0$ assuming $p \geq 3$; refs [24] (Skinner-Zhang) and [30] (W. Zhang), which themselves rely on Gross-Zagier [13], its Shimura-curve extension by Shouwu Zhang [29], Kolyvagin's Euler systems [14], and the Bertolini-Darmon variant [1], give sufficient $p$-adic conditions for rank $1$ assuming $p \geq 5$. The $p$-Selmer averages come from Bhargava-Shankar [2, 3, 4] for $p = 2, 3, 5$. **Finiteness of $\operatorname{Sha}$ (Theorem 2) is obtained only after** establishing analytic rank $\leq 1$, "through the work of Kolyvagin *et al.*" (p. 2). This is the load-bearing logical ordering: finiteness is *not* independent; it is downstream of the rank-$\leq 1$ certification.

### Section 2: Preliminaries (pp. 3-6)

**2.1, $p$-adic rank-$0$ criterion.**

- **Theorem 5 (p. 3).** Let $p$ be an odd prime and $E/\mathbb{Q}$ of conductor $N$ with: (a) good ordinary or multiplicative reduction at $p$; (b) $E[p]$ an irreducible $\operatorname{Gal}(\bar{\mathbb{Q}}/\mathbb{Q})$-module; (c) at least one prime $\ell \neq p$ with $\ell \,\|\, N$ and $E[p]$ ramified at $\ell$; (d) the $p$-Selmer group $S_p(E)$ trivial. Then $\operatorname{rk}(E) = \operatorname{rk_{an}}(E) = 0$.
  - Proof (p. 4) routes through Skinner-Urban [22, Thm. 2(b)] (good reduction) and Skinner [21, Thm. B] (multiplicative reduction) to get $L(E, 1) \neq 0$.
  - **Remark 8 (p. 4)** is the key structural disclosure: [22, Thm. 2(b)] and [21, Thm. B] identify the power of $p$ dividing $\#\operatorname{Sel}_{p^\infty}(E) \cdot \prod(\text{Tamagawa})$ with the power of $p$ in $L(E,1)/\Omega_E$, "a consequence of the Iwasawa-Greenberg main conjecture for $E$." So $\operatorname{Sel}_{p^\infty}(E)$ finite $\Rightarrow L(E,1) \neq 0$. To then conclude $\operatorname{Sha}(E)$ finite "requires an appeal to the work of Gross-Zagier [13] and Kolyvagin [14, Thm. A and Cor. B]." Detector 2 reading: finiteness is never assumed here, but it is *delivered* only by the rank-$\leq 1$ machine.

**2.2, $p$-adic rank-$1$ criterion.**

- **Theorem 9 (p. 4).** Let $p \geq 5$ and $E/\mathbb{Q}$ of conductor $N$ with: (a) good ordinary or multiplicative reduction at $p$; (b) $E[p]$ irreducible; (c) $E[p]$ ramified at every prime $\ell \,\|\, N$ with $\ell \equiv \pm 1 \pmod p$; (d) if $N$ is not squarefree, at least two prime factors $\ell \,\|\, N$, $\ell \neq p$, with $E[p]$ ramified; (e) a Mazur-Tate-Teitelbaum $\mathcal{L}$-invariant condition $\operatorname{ord}_p(\mathcal{L}(E)) = 1$ in the split-multiplicative case (and $E[p]$ not finite at $p$ in the multiplicative case); (f) the $p$-Selmer group $S_p(E)$ has order $p$. Then $\operatorname{rk}(E) = \operatorname{rk_{an}}(E) = 1$.
  - Proof (p. 5) uses Cassels' structure of $\operatorname{Sel}_{p^\infty}$ as $(\mathbb{Q}_p/\mathbb{Z}_p)^r \oplus F \oplus F$; $\#S_p(E) = p$ forces $F = 0$ and $r = 1$. Then [30, Thm. 1.3] (good reduction, W. Zhang) and [24, Thm. 1.1] (multiplicative reduction, Skinner-Zhang) give $\operatorname{ord}_{s=1} L(E, s) = 1$ and $\operatorname{rk} E(\mathbb{Q}) = 1$.
  - **Remark 12 (p. 5)** discloses the mechanism: [30] and [24] show certain Heegner-point indices are not divisible by $p$ (so the Heegner points are *non-torsion*), proved by comparing [22, Thm. 2(b)] and [21, Thm. B] with the Gross special value formula [26, (7-8)], owing much to Bertolini-Darmon [1]. These Heegner points "possibly only" come from Shimura-curve uniformizations (Shouwu Zhang [29]), not necessarily classical modular curves. Finite $\operatorname{Sha}$ follows from [29].

**2.3, Selmer averages.**

- **Theorem 13 ([2, 3, 4], stated p. 5).** Let $p \leq 5$ be prime. When $E/\mathbb{Q}$ in any *large family* are ordered by height, the *average* size of the $p$-Selmer group is $p + 1$.
  - **"Large family"** (p. 5-6): a family $F_\Sigma$ defined by congruence conditions $(\Sigma_\ell)_\ell$, $\Sigma_\ell \subset \mathbb{Z}_\ell^2$ closed with boundary measure $0$; *large* means for all large $\ell$, $\Sigma_\ell \supseteq \{(A,B) : \ell^2 \nmid \Delta(A,B)\}$. Any large family is a positive proportion of all curves [2, Thm. 3.17]. The family of all curves and the family of all semistable curves are large.
  - **Remark 14 (p. 6)** notes the count is by integral models of $p$-Selmer elements (binary quartic forms, ternary cubic forms, quintuples of quinary alternating $2$-forms for $p = 2, 3, 5$), via geometry-of-numbers; ref [5] refines this to equidistribution of local images.

**2.4, root numbers and Selmer parity (this is where parity enters, and where Detector 1 must be watched).**

- **Theorem 15 (Dokchitser-Dokchitser [10], p. 6).** For $E/\mathbb{Q}$ and any prime $p$, with $s_p(E) = \operatorname{rk}_{\mathbb{F}_p} S_p(E)$ and $t_p(E) = \operatorname{rk}_{\mathbb{F}_p} E(\mathbb{Q})[p]$, the quantity $r_p(E) := s_p(E) - t_p(E)$ is *even iff the root number of $E$ is $+1$*. (This is the $p$-parity theorem: it relates the *parity* of Selmer rank to the root number. It is parity-only; it does *not* compute the rank.)
- **Theorem 16 (from [4, §5], p. 6).** Any large family $F$ defined by congruence conditions mod powers of primes $p \equiv 1 \pmod 4$ contains a finite union $F'$ of large subfamilies, of density $> 55.01\%$ of $F$, on which root numbers are *equidistributed* ($+1$ and $-1$ each half), with $E$ and its $-1$-twist $E_{-1}$ both in $F'$ and of opposite root sign.
  - Consequence: for any $p$, $> 55.01\%$ of all $E/\mathbb{Q}$ have *equidistributed parity of $p$-Selmer rank*.

### Section 3: Proofs (pp. 7-14)

**3.1-3.2, densities of three families at $p = 5$ (pp. 7-10).** Define $S_0(p) \supset S_1'(p) \supset S_1(p)$ by reduction-type and ramification congruences matching Theorems 5 and 9. The constant $\kappa \geq 0.5501$ is the equidistribution fraction from Theorem 16. Computed densities:
- **Lemma 17 (p. 7).** $\mu(S_0(5)) = \dfrac{4 \cdot 5^{10}}{5(5^{10} - 1)} > 0.8$.
- **Lemma 18 (p. 8).** $\mu(S_1'(5)) = \left(\dfrac{99}{125} - \dfrac{19}{125}\cdot\dfrac{4}{5^5 - 1}\right)\left(1 - \dfrac{1}{5^{10}}\right)^{-1} = 0.7918054\ldots$
- **Lemma 19 (p. 9-10).** $\mu(S_1(5)) > 0.7917957\ldots$, the density of $S_1(5)$ (the additional ramification congruence at primes $\ell \equiv \pm 1 \pmod 5$ shaves at most $0.00001$ off $\mu(S_1'(5))$; this is the bound (2) on p. 10).
- **Lemma 20 (p. 10-11).** For any prime $p$, $100\%$ of $E/\mathbb{Q}$ (by height) satisfy two properties: $E[p]$ is an irreducible $\operatorname{Gal}(\bar{\mathbb{Q}}/\mathbb{Q})$-module (via Hilbert irreducibility; see also Duke [11]), and there exist at least two primes $\ell \,\|\, N(E)$, $\ell \neq p$, at which $E[p]$ is ramified. This is why only conditions (a)/(c)/(e) (not (b)/(d)) had to be built into the families $S_0, S_1$: the rest hold for $100\%$ of curves.

**3.3, rank-0 lower bound (pp. 11-12).**

- **Theorem 21 (p. 11).** If $F$ is a finite union of large families with exactly $50\%$ root number $+1$, then at least $3/8$ of $F$ has $5$-Selmer rank $0$. (Proof: average $5$-Selmer size $= 6$ by Thm 13; half have even parity by Thm 15; an Markov-type bound on the average forces a $(p-2)/(p-1) = 3/4$ fraction of the even half to be trivial, i.e. $3/8$ overall.)
- **Corollary 22 (p. 11-12).** At least $16.50\%$ of all $E/\mathbb{Q}$ have both algebraic and analytic rank $0$. Arithmetic: $\frac{3}{8} \times 0.5501 \times 0.8 = 0.16503$.

**3.4, rank-1 lower bound (p. 12).**

- **Theorem 23 (p. 12).** Same hypotheses; at least $19/40$ of $F$ has $5$-Selmer rank $1$.
- **Corollary 24 (p. 12).** At least $20.68\%$ of all $E/\mathbb{Q}$ have both algebraic and analytic rank $1$. Arithmetic: $\frac{19}{40} \times 0.5501 \times 0.7918054 - 0.00001 > 0.20688$.

**3.5, rank "$0$ or $1$" lower bound (pp. 13-14).**

- **Theorem 25 (p. 13).** For finite unions $F \subset S_0(5) \cap S_1(5)$ of large families: at least $19/24$ of $F$ has algebraic and analytic rank $0$ or $1$; and *if* root numbers are equidistributed in $F$, at least $7/8$ do. (The improvement over summing Corollaries 22 and 24 comes from not separating the two ranks: a single linear-programming constraint $x_0 + p^2(1/2 - x_0) + p(x_1 + p^2(1/2 - x_1)) \leq p + 1$ on the densities yields a sharper $(2p-3)/(2p-2)$ bound.)
- **Corollary 26 (p. 13-14).** At least $66.48\%$ of all $E/\mathbb{Q}$ have algebraic and analytic rank $0$ or $1$. Final arithmetic (p. 14):
$$\left(\tfrac{7}{8} \times 0.5501 + \tfrac{19}{24} \times 0.4499\right) \times 0.7918054 - \left(\tfrac{7}{8} + \tfrac{19}{24}\right) \times 0.00001 + 0.00169 = 0.664816\ldots$$
  This proves Theorem 1; Theorem 2 (finite $\operatorname{Sha}$) follows because each certified curve has analytic rank $\leq 1$ and so Gross-Zagier-Kolyvagin gives finiteness.

### Section 4: Conclusion and future work (pp. 14-15)

- The percentages improve if the input theorems improve. If Theorem 5 is strengthened (Remark 6: supersingular reduction, dropping irreducibility), rank-0 density rises to $19.8\%$ and the "0 or 1" bound to $69.6\%$. If Theorem 9 is strengthened (Remark 10), rank-1 density rises to $24.8\%$ and the BSD-rank bound to $79.7\%$ ("working also with the prime $3$ would push this lower bound over $80\%$").
- **Theorem 27 (conditional, p. 15).** *If* for all primes $p$ the average $p$-Selmer size is $p + 1$ (the conjectured Selmer average, consistent with Delaunay [9] and Poonen-Rains [16] heuristics), then the BSD *rank* conjecture holds for $100\%$ of $E/\mathbb{Q}$. The product of the density bounds (3) and (4) tends to $1$ as $p \to \infty$. **This is a conjecture, not a theorem**: it is conditional on the unproven extension of the Selmer-average result to all (infinitely many) primes, and it is still only about $100\%$ *density*, never about a *specific* curve and never about rank $\geq 2$.

## Project mapping

1. **What is PROVEN vs the GAP.** PROVEN: $> 66.48\%$ of $E/\mathbb{Q}$ (by height) satisfy the BSD rank equality and have finite $\operatorname{Sha}$ (Theorems 1, 2). GAP: the complementary $< 33.52\%$ is uncertified, and *all* rank $\geq 2$ curves live inside that complement. The theorem says nothing about any individual curve and nothing about the rank $\geq 2$ structure. Theorem 27's $100\%$ is conditional and density-only, so even its strongest form would not close BSD: $100\%$ density tolerates an infinite uncertified set, exactly where rank $\geq 2$ sits.

2. **EXACT regime.** Every certified curve is *individually* analytic rank $0$ (Theorem 5 route, $\#S_p = 1$) or *individually* analytic rank $1$ (Theorem 9 route, $\#S_p = p$). The proof is a **hybrid of $p$-adic and archimedean**: the rank criteria are $p$-adic (main-conjecture / $p$-Selmer / Heegner-index-mod-$p$ statements at $p = 3, 5$), but their validity rests on the archimedean Gross-Zagier height formula and Kolyvagin's Euler system. So this note feeds research direction [`03_padic_archimedean.md`](../research_directions/03_padic_archimedean.md): it is a worked example of stitching $p$-adic Selmer control to archimedean nonvanishing, and it shows that stitch degenerating exactly at rank $\geq 2$.

3. **Detector 1 (parity-only): PASSES, but only by adding non-parity input.** Root numbers (Theorem 16) and the Dokchitser-Dokchitser $p$-parity theorem (Theorem 15) supply *only parity*. The paper is explicit (p. 6) that "Theorem 13 alone is not sufficient." Parity is upgraded to an actual rank value solely by the Selmer-*size* average (Theorem 13, average $= p+1$, not just parity) combined with the rank-$\leq 1$ $p$-adic criteria. Reading: this is a clean illustration that parity is necessary but never sufficient. The detector is satisfied because the rank is genuinely computed, but *only* in the range where $\#S_p \in \{1, p\}$ pins it down. Remove the rank-$\leq 1$ criteria and you are back to parity-only.

4. **Detector 2 (Sha-finiteness assumed): PASSES.** Finiteness of $\operatorname{Sha}$ is never an input. It is an *output*, delivered by Gross-Zagier-Kolyvagin after analytic rank $\leq 1$ is established (Theorem 2 derivation, p. 2; Remark 8, p. 4; Remark 12, p. 5). The note records the precise dependency: no finiteness is assumed, but finiteness is obtained *only* on the rank-$\leq 1$ slice, so this paper provides *zero* new finiteness in the open regime.

5. **Detector 3 (function-field mirage): PASSES, not applicable.** The argument is over $\mathbb{Q}$ throughout and uses no elliptic surface or geometric Frobenius. The Selmer counts are geometry-of-numbers over $\mathbb{Z}$ (binary quartics, ternary cubics, quinary $2$-forms), not etale cohomology of a surface. There is no function-field shortcut imported.

6. **Control pair (rank $\leq 1$ proven vs rank $\geq 2$ open).** This paper is the *cleanest possible statement of the control wall at the population level*. The proven $> 66.48\%$ is, ingredient by ingredient, exactly the Gross-Zagier-Kolyvagin-reachable part (rank $0$ via $\#S_p = 1$, rank $1$ via $\#S_p = p$). The open complement is exactly where a curve has $5$-Selmer rank $\geq 2$, the population shadow of the rank $\geq 2$ object. Every $p$-adic criterion here (Theorems 5, 9) is hard-coded to $\#S_p \in \{1, p\}$ and has no analog for $\#S_p \geq p^2$; this is the population-level fingerprint of the one-Heegner-point ceiling documented in [`gross_zagier_kolyvagin.md`](gross_zagier_kolyvagin.md).

7. **Which research direction / experiment it feeds.** Primarily [`01_rank_two_object.md`](../research_directions/01_rank_two_object.md): the complementary density is the *target population* for a rank $\geq 2$ construction, and the smallest rank-2 curve 389a1 lives there. Secondarily [`02_higher_rank_euler_system.md`](../research_directions/02_higher_rank_euler_system.md): the Heegner-index-mod-$p$ nonvanishing (Remark 12) is exactly the rank-1 Euler-system input that a rank $\geq 2$ system would have to replace, and this paper shows the input is sharp at rank $1$. Experimentally it motivates a population-level check: among bundled curves, partition by $2$-Selmer rank and confirm that the rank-$\geq 2$ curves (389a1, 5077a1) are precisely the ones no criterion here certifies (the [`experiments/weak_bsd_table`](../../../experiments/weak_bsd_table) thread is the natural home).

## Status

Read in full from the downloaded arXiv PDF ([`references/05_statistics_averages/Bhargava-Skinner-Zhang-2014-Majority-Satisfy-BSD.pdf`](../../../references/05_statistics_averages/Bhargava-Skinner-Zhang-2014-Majority-Satisfy-BSD.pdf), 17 pages, v2 dated 18 July 2014, 225 KB). Theorem numbers (1-27), corollary numbers (4, 22, 24, 26), lemma numbers (17-20), the height normalization, the $\mu(S_0(5))$ and $\mu(S_1'(5))$ formulas, the final $0.664816$ arithmetic, and all cited page numbers were transcribed directly from the PDF, not from memory. NOT independently verified: the internal correctness of the cited inputs (Bhargava-Shankar Selmer averages [2, 3, 4], Skinner-Urban [22], Skinner [21], Skinner-Zhang [24], W. Zhang [30], Skinner converse [20], Dokchitser-Dokchitser $p$-parity [10]); these are read as black boxes at the strength their authors state. The conditional Theorem 27 is flagged as conjectural and was not promoted. No numerical experiment was run as part of this note.
