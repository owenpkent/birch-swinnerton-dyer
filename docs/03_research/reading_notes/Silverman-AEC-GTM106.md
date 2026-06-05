# Reading note: J. H. Silverman, "The Arithmetic of Elliptic Curves," 2nd ed., Graduate Texts in Mathematics 106, Springer (2009)

> **Role in the BSD program.** This is the substrate. It is the textbook that *defines* the objects BSD is a statement about: the Mordell-Weil group $E(\mathbb{Q})$ and its rank, the descent that proves $E(\mathbb{Q})$ finitely generated (Chapter VIII), the canonical height and the regulator $\operatorname{Reg}(E/\mathbb{Q})$ (Chapter VIII §9), and the Selmer and Tate-Shafarevich groups together with the fundamental descent exact sequence $0 \to E(K)/mE(K) \to \operatorname{Sel}^{(m)}(E/K) \to \operatorname{Sha}(E/K)[m] \to 0$ (Chapter X §4). It is the honest baseline: finiteness of $\operatorname{Sha}$ is stated here as a CONJECTURE (Chapter X §4, remark on the Shafarevich-Tate conjecture), not a theorem, in exactly the regime-blind way that the rest of the program then has to repair rank by rank. Every later note (Gross-Zagier, Kolyvagin, Kato, Skinner-Urban) manipulates the groups defined here; this note pins down their definitions so the others can be precise.
>
> **Reading depth.** Written from authoritative knowledge of Chapters VIII (Mordell-Weil) and X (computing the Mordell-Weil group: descent, the Selmer and Shafarevich-Tate groups), with supporting definitions from Chapter III (Weierstrass equations, isogenies, the Weil and Tate pairings) and Chapter VIII §6 (the descent via two-isogeny / the Kummer sequence). NO open PDF was obtained: the book is copyrighted by Springer and the only located copies were paywalled or pirate mirrors (scribd, dokumen.pub, ad-hoc institutional repositories), none of which qualifies as a legal open source, and the author's homepage (math.brown.edu/johsilve/AECHome.html) hosts only errata, not the text. Consequently NO page numbers are cited; results are keyed to Silverman's chapter, section, and named-theorem/proposition structure only. Where a theorem is referenced by its standard label in this book (e.g. "Theorem VIII.6.7, the Weak Mordell-Weil theorem") the label follows Silverman's own numbering convention; it is cited at section/named-result granularity, never as a verified page.
>
> **Topic folder.** `references/07_foundations_textbooks/`.
>
> **Cross-links.** Four-level framing: `docs/02_graduate/` (this note sits BELOW all four levels; it is the definition layer that the height-formula level, the Selmer-bounding level, and the parity level all presuppose). Three detectors: `experiments/_shared/controls.py` (this note is where the Sha-finiteness detector's *premise* is established: the text itself leaves $\operatorname{Sha}$ finiteness open, so any downstream method that assumes it must flag the assumption against THIS baseline). Research directions: `docs/03_research/research_directions/01_rank_two_object.md` (the regulator and the descent sequence defined here are the exact quantities a rank-$\geq 2$ construction must control), `docs/03_research/research_directions/02_higher_rank_euler_system.md` (the Selmer group $\operatorname{Sel}^{(m)}$ defined in Chapter X is the object an Euler system bounds), `docs/03_research/research_directions/03_padic_archimedean.md` (the archimedean canonical height of Chapter VIII §9 is the archimedean side that the $p$-adic height / $p$-adic regulator must mirror). Atlas: `docs/research_atlas/README.md`, foundational row.
>
> **Difference from related notes.** Every other note in this folder proves or surveys a THEOREM or CONJECTURE *about* $\operatorname{rank}$, $\operatorname{Sel}$, $\operatorname{Sha}$, or $\operatorname{Reg}$. This note is the only one that defines those symbols. `Kolyvagin-1990-Euler-Systems.md` bounds the $\operatorname{Sel}_p$ defined here; `Gross-Zagier-1986-Heegner-Points-Derivatives.md` computes a height in the pairing defined here; `Mazur-Tate-Teitelbaum-1986-p-adic-BSD.md` builds the $p$-adic analog of the regulator defined here. Read this note first; it fixes the vocabulary.

## One-line takeaway

Silverman's Chapters VIII and X construct, with full proofs, the finite-generation of $E(K)$ (Mordell-Weil), the canonical height pairing and regulator, and the descent exact sequence $0 \to E(K)/mE(K) \to \operatorname{Sel}^{(m)}(E/K) \to \operatorname{Sha}(E/K)[m] \to 0$ that splits the computation of the rank into an effectively computable piece ($\operatorname{Sel}^{(m)}$, finite and computable) and an obstruction piece ($\operatorname{Sha}[m]$, whose finiteness is left OPEN as a conjecture in the text). These are the definitions BSD is stated in. The book proves finite generation of $E(K)$ unconditionally (a theorem for every number field, every rank), but it does NOT prove finiteness of $\operatorname{Sha}$, does not compute the rank, and says nothing about $L$-functions; it is regime-neutral substrate, and the honest place to anchor the Sha-finiteness detector.

## Technical content (section by section)

Notation: $K$ a number field, $E/K$ an elliptic curve, $M_K$ the set of places, $E(K)$ the group of $K$-rational points, $E[m]$ the $m$-torsion, $G_{\bar K/K} = \operatorname{Gal}(\bar K/K)$.

**Chapter VIII, the Mordell-Weil theorem.** The chapter's goal (Theorem VIII.6.7 for the weak form, then the full theorem) is:

> **Mordell-Weil theorem.** For an elliptic curve $E$ over a number field $K$, the group $E(K)$ is finitely generated.

The proof has two ingredients, presented in this order.

**VIII §1 (heights on projective space) and §5-6 (heights on $E$).** A *height* on $\mathbb{P}^N(K)$ measures arithmetic complexity. The chapter develops the *Weil height machine*: to each divisor (line bundle) on a variety it attaches a height function, well-defined up to bounded functions, additive in the divisor up to $O(1)$. On $E$, applied to a suitable even divisor (e.g. $2(O)$ or the divisor of the $x$-coordinate), this gives a height $h_x$ satisfying:
- **(Quasi-parallelogram law / quadraticity up to $O(1)$):** $h_x(P+Q) + h_x(P-Q) = 2h_x(P) + 2h_x(Q) + O(1)$.
- **(Finiteness):** for any bound $C$, the set $\{P \in E(K) : h_x(P) \le C\}$ is finite.

**VIII §9 (the canonical / Neron-Tate height).** Averaging out the $O(1)$ gives the *canonical height*

$$\hat h(P) = \lim_{n \to \infty} \frac{h_x(2^n P)}{4^n},$$

which is an honest quadratic form: $\hat h(mP) = m^2 \hat h(P)$, $\hat h \ge 0$, and $\hat h(P) = 0 \iff P$ is torsion. The associated *Neron-Tate height pairing*

$$\langle P, Q \rangle = \tfrac12\big(\hat h(P+Q) - \hat h(P) - \hat h(Q)\big)$$

is bilinear, symmetric, and positive-definite on $E(K) \otimes \mathbb{R}$ modulo torsion. Its Gram determinant on a basis of $E(K)/E(K)_{\mathrm{tors}}$ is the **regulator** $\operatorname{Reg}(E/K)$, one of the explicit factors in the strong (full) BSD formula. (Silverman decomposes $\hat h$ into local heights / a sum of contributions from each place; the archimedean local height is the analytically delicate one.)

**VIII §1-3 and §6 (the weak Mordell-Weil theorem).** The arithmetic core is:

> **Weak Mordell-Weil theorem (VIII.1.1 / VIII.6.7).** For every $m \ge 2$, the quotient $E(K)/mE(K)$ is finite.

The proof goes through Galois cohomology. From the multiplication-by-$m$ isogeny and the short exact sequence of $G_{\bar K/K}$-modules
$$0 \to E[m] \to E(\bar K) \xrightarrow{\;\times m\;} E(\bar K) \to 0,$$
taking Galois cohomology yields the **Kummer sequence** (the descent connecting map $\delta$):

$$0 \to E(K)/mE(K) \xrightarrow{\;\delta\;} H^1(G_{\bar K/K}, E[m]) \to H^1(G_{\bar K/K}, E)[m] \to 0.$$

One shows $\delta(E(K)/mE(K))$ lands in a subgroup of $H^1$ that is **unramified outside a finite set $S$** (the places of bad reduction, those above $m$, and the archimedean places), and that for the field $K(E[m])$ (which is a finite extension by the Weil pairing forcing $\mu_m \subset K(E[m])$, Chapter III) this $S$-ramified, $m$-torsion cohomology is finite. Finiteness of $E(K)/mE(K)$ follows. The descent from "weak" to "full" Mordell-Weil is the **descent lemma**: a group $A$ with a height function satisfying quadraticity-up-to-$O(1)$, finiteness of bounded sets, and $A/mA$ finite is itself finitely generated. That packaging of the height machinery (§9) with weak Mordell-Weil (§6) is the proof.

**Chapter X, computing the Mordell-Weil group: Selmer and Tate-Shafarevich.** Chapter VIII proves $E(K)/mE(K)$ finite but the cohomological argument is not effective: it bounds the rank in principle but the bound is not computable because one cannot in general decide which cohomology classes come from actual rational points. Chapter X repairs effectivity, place by place, and in doing so defines the two groups BSD's strong form is about.

**X §3-4 (the Selmer and Shafarevich-Tate groups).** Fix $m$ (or more generally an isogeny $\phi: E \to E'$). For each place $v \in M_K$ there is a localization $H^1(G_{\bar K/K}, E[m]) \to H^1(G_{\bar K_v / K_v}, E[m])$, and a *local Kummer map* $E(K_v)/mE(K_v) \hookrightarrow H^1(G_{\bar K_v/K_v}, E[m])$. The **$m$-Selmer group** is the subgroup of global classes that are everywhere locally in the image of a local point:

$$\operatorname{Sel}^{(m)}(E/K) = \ker\!\Big( H^1(G_{\bar K/K}, E[m]) \longrightarrow \prod_{v \in M_K} H^1(G_{\bar K_v/K_v}, E) \Big),$$

equivalently the classes whose restriction at every $v$ lies in $\operatorname{im}\big(E(K_v)/mE(K_v)\big)$. The **Tate-Shafarevich group** is the obstruction to a global point existing despite everywhere-local points:

$$\operatorname{Sha}(E/K) = \ker\!\Big( H^1(G_{\bar K/K}, E) \longrightarrow \prod_{v \in M_K} H^1(G_{\bar K_v/K_v}, E) \Big).$$

These fit into the **fundamental descent exact sequence** (Chapter X §4):

$$0 \longrightarrow E(K)/mE(K) \xrightarrow{\;\delta\;} \operatorname{Sel}^{(m)}(E/K) \longrightarrow \operatorname{Sha}(E/K)[m] \longrightarrow 0.$$

> **Theorem (X.4.2, finiteness of the Selmer group).** $\operatorname{Sel}^{(m)}(E/K)$ is finite, and it is effectively computable.

That is the entire point of the construction: the local conditions cut $H^1$ down to a finite, in-principle-computable group, so $\operatorname{Sel}^{(m)}$ gives a computable *upper bound* on $\operatorname{rank} E(K)$. The descent sequence then reads:

$$\operatorname{rank} E(K) + \dim_{\mathbb{F}_p}\operatorname{Sha}(E/K)[p] = \dim_{\mathbb{F}_p}\operatorname{Sel}^{(p)}(E/K) - \dim_{\mathbb{F}_p} E(K)[p] \quad (\text{for prime } m=p),$$

so the gap between the computable Selmer bound and the true rank is EXACTLY $\operatorname{Sha}[p]$.

**X §4 (the Shafarevich-Tate conjecture, stated as OPEN).** Silverman states, as a conjecture and not a theorem:

> **Conjecture (Shafarevich-Tate).** $\operatorname{Sha}(E/K)$ is finite.

The text emphasizes that the descent procedure terminates and computes $\operatorname{rank} E(K)$ *if* $\operatorname{Sha}$ (or at least its $p$-primary part for some $p$) is finite, and that without this one cannot in general certify that the Selmer bound is sharp. This is the precise origin of the project's Sha-finiteness detector: the foundational text itself flags finiteness as unproven. (Silverman notes the Cassels-Tate pairing makes $\operatorname{Sha}$, if finite, carry a non-degenerate alternating pairing, forcing $\#\operatorname{Sha}$ to be a perfect square; this is structure, not a finiteness proof.)

**X §1-2 and §6 (explicit descent, complete $2$-descent, examples).** The chapter makes descent concrete for small $m$: complete $2$-descent via the $x$-coordinates and the connecting map to $K^*/(K^*)^2$-valued invariants, descent via a $2$-isogeny when $E$ has rational $2$-torsion, and worked computations of $\operatorname{Sel}^{(2)}$ and $E(\mathbb{Q})$ for explicit curves. This is the computational substrate behind the repo's descent / weak-BSD experiments.

**Where BSD itself appears.** AEC states the Mordell-Weil group, the regulator, $\operatorname{Sha}$, and the local conditions, i.e. all the arithmetic side of the strong BSD formula

$$\lim_{s\to 1}\frac{L(E,s)}{(s-1)^r} \;\stackrel{?}{=}\; \frac{\#\operatorname{Sha}(E/\mathbb{Q}) \cdot \operatorname{Reg}(E/\mathbb{Q}) \cdot \prod_v c_v \cdot \Omega_E}{(\#E(\mathbb{Q})_{\mathrm{tors}})^2}.$$

The $L$-function side, the analytic continuation, the functional equation, and the conjecture itself are treated in Silverman's *companion* volume (Advanced Topics in the Arithmetic of Elliptic Curves, GTM 151), NOT in GTM 106. GTM 106 supplies $E(\mathbb{Q})$, $r = \operatorname{rank}$, $\operatorname{Reg}$, $E(\mathbb{Q})_{\mathrm{tors}}$, the Tamagawa-type local factors via Neron models (Chapter VII), and $\operatorname{Sha}$. It does not assert BSD.

## Project mapping

1. **What is PROVEN vs the GAP.** PROVEN here, unconditionally and in every rank over every number field: $E(K)$ finitely generated (Mordell-Weil, VIII), $E(K)/mE(K)$ finite (weak Mordell-Weil, VIII.6.7), $\hat h$ a positive-definite quadratic form giving a well-defined $\operatorname{Reg}$ (VIII.9), $\operatorname{Sel}^{(m)}$ finite and computable (X.4.2), and the descent exact sequence (X.4). The GAP, stated AS a gap in the text: finiteness of $\operatorname{Sha}(E/K)$ is a CONJECTURE; the rank is not computed by the book (only bounded above by $\operatorname{Sel}^{(m)}$); and nothing connects any of this to $L(E,s)$. The structural fact the book makes precise: $\operatorname{rank} E(K)$ is determined by $\operatorname{Sel}^{(p)}$ MINUS the unknown $\operatorname{Sha}[p]$, so the whole rank question is "how big is $\operatorname{Sha}$," which is exactly where rank $\geq 2$ becomes hard.

2. **EXACT regime.** Regime-NEUTRAL and foundational. The Mordell-Weil theorem, the regulator, and the descent sequence hold for ALL ranks and ALL number fields; the book draws no line at rank $1$. The canonical height of VIII.9 is the ARCHIMEDEAN object (the regulator is a real determinant); the $p$-adic regulator that appears in $p$-adic BSD (Mazur-Tate-Teitelbaum) is a separate construction not in this book. So this note feeds both the archimedean and (by contrast) the $p$-adic sides, but its own content is archimedean and algebraic, not $p$-adic-analytic.

3. **Three detectors.**
   - *Parity-only:* **N/A, but it is the DEFINITION layer the detector measures against.** The book never computes a rank from parity; it computes (a bound on) the rank from descent. The root number, the functional equation, and the parity conjecture are not in GTM 106 at all. So it cannot trigger parity-only; rather, it supplies the true rank invariant against which a parity-only method is exposed as giving only $r \bmod 2$.
   - *Sha-finiteness-assumed:* **This note is the SOURCE / baseline of the detector.** Silverman states finiteness of $\operatorname{Sha}$ as an OPEN conjecture (X §4). Every downstream method that "reads $\#\operatorname{Sha}$ off the BSD formula" or "completes a descent" is implicitly using a finiteness that THIS book declines to prove. The detector exists precisely to flag that borrowing against this baseline. The book PASSES honestly: it does not assume finiteness; it isolates it as the obstruction.
   - *Function-field-mirage:* **PASSES (number-field-native, and explicitly so).** The descent here is built from $H^1(G_{\bar K/K}, -)$ for $K$ a number field, local conditions at places of $K$, and the Weil-height finiteness (Northcott property) which is a NUMBER-FIELD phenomenon. There is no geometric Frobenius, no $\ell$-adic cohomology of a surface, no Artin-Tate Brauer-group machinery. The function-field proof of finite Sha (Tate; Artin-Tate; Milne) lives in a different formalism; this book is the honest number-field version where finiteness stays open.

4. **Control pair (rank $\leq 1$ proven vs rank $\geq 2$ open).** This note defines BOTH ends of the control pair without privileging either: $37a1$ (rank $1$) and $389a1$ (rank $2$) are both just curves whose $E(\mathbb{Q})$, $\operatorname{Reg}$, $\operatorname{Sel}^{(p)}$, and $\operatorname{Sha}$ are the objects of Chapters VIII and X. The book is where you SEE that the rank-$1$ vs rank-$\geq 2$ distinction is invisible at the level of definitions: the descent sequence is identical for both. The distinction only appears once a *bound* on $\operatorname{Sel}$ (Kolyvagin, from one Heegner point) or a *value* of $L$ (Gross-Zagier) is imported, neither of which is in this book. That is the cleanest possible statement of why the wall is not a definitional wall but a *construction* wall.

5. **Feeds.** Research Direction 01 (`01_rank_two_object.md`): the regulator (VIII.9) and the descent sequence (X.4) are the exact invariants a rank-$2$ object must pin down; a successful construction has to produce TWO independent classes in $\operatorname{Sel}^{(p)}$ whose images in $E(K)/pE(K)$ are independent, in the language defined here. Research Direction 02 (`02_higher_rank_euler_system.md`): an Euler system's output is a bound on $\operatorname{Sel}^{(p)}(E/K)$, the group X §3 defines; this note is the definition document those bounds are quoted against. Research Direction 03 (`03_padic_archimedean.md`): VIII.9's archimedean canonical height is the object whose $p$-adic shadow (the $p$-adic regulator) the $p$-adic BSD program must build. Experiments: this note underwrites `experiments/weak_bsd_table/` (descent / $E(\mathbb{Q})$ computations) and `experiments/strong_bsd_quantities/` (the regulator and $\operatorname{Sha}$ factor), and it is the definition source for the Sha-finiteness flag in `experiments/_shared/controls.py`. Atlas: foundational row, all detectors PASS or N/A, the honest baseline.

## Status

Written from authoritative knowledge of Silverman, AEC (GTM 106, 2nd ed.), Chapters VIII (heights VIII.1, VIII.5-6, VIII.9; weak Mordell-Weil VIII.6.7; the Mordell-Weil theorem and descent lemma) and X (the Selmer group and Shafarevich-Tate group X.3-4; finiteness of the Selmer group X.4.2; the descent exact sequence; the Shafarevich-Tate conjecture stated as open; complete $2$-descent and $2$-isogeny descent X.1-2, X.6), with supporting definitions from Chapter III (Weierstrass forms, isogenies, the Weil and Tate pairings) and Chapter VII (Neron models, the local Tamagawa factors $c_v$) drawn on only to place the strong-BSD quantities. Theorem and section labels follow Silverman's own numbering convention and are cited at section/named-result granularity.

NOT read: no PDF was obtained. The book is copyrighted by Springer; the only located copies were paywalled or pirate/uncertified mirrors (scribd, dokumen.pub, ad-hoc institutional repositories) and the author homepage hosts only errata, so per the open/legal-only rule NO PDF was downloaded and NO page numbers are cited. The numbering above (e.g. VIII.6.7, X.4.2) reflects this book's standard internal scheme and is given as section-level reference, not as verified page reference; nothing was fabricated. Not covered here because it is outside GTM 106: the $L$-function, its analytic continuation and functional equation, the root number / parity, and the statement of BSD itself, all of which live in Silverman's companion volume GTM 151 and in the modularity / Gross-Zagier notes. The single load-bearing logical claim, stated exactly: this book proves finite generation of $E(K)$ in every rank but leaves finiteness of $\operatorname{Sha}$ OPEN, so it is the honest baseline against which the Sha-finiteness detector is calibrated.
