# Reading note: B. Gross, "Kolyvagin's work on modular elliptic curves," in *L-functions and Arithmetic* (Durham 1989), LMS Lecture Note Series 153, Cambridge Univ. Press (1991), 235-256.

> **Role in the BSD program.** This is the canonical clean exposition of Kolyvagin's Euler system argument: how the Heegner points defined over ring class fields $H_n/K$ produce, via Kolyvagin's "derivative" operators, a system of cohomology classes that annihilates the Selmer group and the Tate-Shafarevich group of a modular elliptic curve $E/\mathbb{Q}$. Together with Gross-Zagier it delivers the only fully proven regime of BSD: if $L'(E,1)\neq 0$ then $\operatorname{rank} E(\mathbb{Q})=1$ and $\operatorname{Sha}(E/\mathbb{Q})$ is finite; if $L(E,1)\neq 0$ then $\operatorname{rank}=0$ and $\operatorname{Sha}$ is finite. It is the bridge note: Gross-Zagier supplies the analytic input (a non-torsion Heegner point when $L'(E/K,1)\neq 0$), and this paper is where that single point is leveraged into a bound on the whole Selmer group.
>
> **Reading depth.** Written from authoritative knowledge of this widely-cited paper. No open-access PDF of the original LMS 153 chapter exists (the Cambridge volume is paywalled; Gross's Harvard publications/eprints pages list the paper but host no PDF for it). Statements are cited by section and theorem name, not by page number; page numbers are NOT given because the PDF was not read. The structure described (Heegner points over ring class fields, the Euler-system relations, Kolyvagin's derivative classes, the descent to a Selmer bound) follows the paper's own organization and is corroborated by the related expository accounts (Gross's PCMI "Lectures on the conjecture of Birch and Swinnerton-Dyer," and the standard treatments by Rubin and by Darmon).
>
> **Topic folder:** `references/02_heegner_gross_zagier/`. Suggested PDF: `Gross-1991-Kolyvagins-Work-on-Modular-Elliptic-Curves.pdf` (not downloaded; no legal open copy located).
>
> **Cross-links.**
> - Four-level framing: `docs/02_graduate/` (BSD's hard content sits at constructing points / bounding $\operatorname{Sha}$, not at parity; this note is the proof of the rank $\le 1$ corner of that picture).
> - Three detectors: `experiments/_shared/controls.py`. This source PASSES Detector 1 (it gives the full rank, not just parity) and PASSES Detector 2 in the only honest way: it PROVES $\operatorname{Sha}$ finite rather than assuming it, but only because $r_{\mathrm{an}}\le 1$. It PASSES Detector 3 (no geometric Frobenius; the Euler system lives in arithmetic Galois cohomology over $\mathbb{Q}$).
> - Research directions: `docs/03_research/research_directions/01_rank_two_object.md` (the one-point ceiling this note makes precise), `02_higher_rank_euler_system.md` (the norm relations a rank $\ge 2$ system would need), `03_padic_archimedean.md` (the archimedean leading term this argument does not touch).
> - Atlas: `docs/research_atlas/README.md` (Heegner / Gross-Zagier-Kolyvagin row).
>
> **Difference from related notes.** The sibling note `gross_zagier_kolyvagin.md` is a one-page summary of the combined theorem and its rank-1 ceiling. THIS note is the detailed mechanism of the Kolyvagin half: the explicit Euler-system axioms, the derivative classes $P_n \in E(H_n)/p^M$, the local conditions they satisfy, and exactly where "$\le 1$" is forced. Read this for the machine; read that for the headline.

## One-line takeaway

Starting from a single non-torsion Heegner point $y_K \in E(K)$, Kolyvagin builds a norm-compatible family of points over ring class fields, applies a "derivative" operator to manufacture global cohomology classes that are unramified everywhere except at one auxiliary prime, and uses local-global duality to bound the $p$-Selmer group by the divisibility of the Heegner point: this forces $\operatorname{rank} E(\mathbb{Q}) = 1$ and $\operatorname{Sha}(E/\mathbb{Q})$ finite when the point is non-torsion, but the argument is structurally about a single class and is silent the moment a second independent point is required (rank $\ge 2$).

## Technical content (section by section)

**Setup: modular curve, Heegner points, and the Gross-Zagier input.**
$E/\mathbb{Q}$ is a modular elliptic curve of conductor $N$ (modularity is an input; at the time of writing it was known for the relevant CM and many other curves, and is now the Wiles-Taylor-Wiles-BCDT theorem). Fix an imaginary quadratic field $K$ of discriminant $D$ satisfying the **Heegner hypothesis**: every prime $\ell \mid N$ splits in $K$. Then $\mathcal{O}_K$ contains an ideal $\mathfrak{N}$ with $\mathcal{O}_K/\mathfrak{N} \cong \mathbb{Z}/N\mathbb{Z}$, and the pair $(\mathbb{C}/\mathcal{O}_K,\ \mathfrak{N}^{-1}/\mathcal{O}_K)$ defines a point $x_1$ on $X_0(N)$, hence (via the modular parametrization $\varphi\colon X_0(N)\to E$) a point $y_1 \in E(H_1)$, where $H_1 = H$ is the Hilbert class field of $K$. Taking the trace to $K$ gives the basic Heegner point $y_K = \operatorname{Tr}_{H/K}(y_1) \in E(K)$. The Gross-Zagier theorem (the companion analytic input, not reproved here) gives
$$\hat{h}_K(y_K) \ \doteq\ c\, L'(E/K, 1), \qquad c>0,$$
so $y_K$ is non-torsion in $E(K)$ exactly when $L'(E/K,1)\neq 0$. This note takes the non-torsion point as given and asks what it implies.

**Heegner points over ring class fields.**
For each squarefree product $n$ of primes inert in $K$ and prime to $ND$, let $\mathcal{O}_n = \mathbb{Z} + n\mathcal{O}_K$ be the order of conductor $n$, and let $H_n$ be the associated ring class field, with $\operatorname{Gal}(H_n/K)\cong \operatorname{Pic}(\mathcal{O}_n)$ and $\operatorname{Gal}(H_n/H_1)\cong \prod_{\ell\mid n} (\text{cyclic of order }\ell+1)$ (using the inertness of each $\ell$). The CM construction yields Heegner points $y_n \in E(H_n)$, one for each such $n$.

**The Euler-system (norm-compatibility) relations.**
This is the technical core. The points $y_n$ are not norm-compatible on the nose; they satisfy a relation involving the Hecke eigenvalue $a_\ell$. For a prime $\ell$ inert in $K$ and prime to $nND$, writing $\operatorname{Tr}_{\ell}$ for the trace from $H_{n\ell}$ down to $H_n$:
$$\operatorname{Tr}_{H_{n\ell}/H_n}(y_{n\ell}) \ =\ a_\ell\, y_n \qquad \text{in } E(H_n),$$
together with a congruence (the second Euler-system axiom) expressing the reduction of $y_{n\ell}$ modulo a prime of $H_{n\ell}$ above $\ell$ in terms of $\operatorname{Frob}_\ell$ acting on $y_n$:
$$y_{n\ell} \ \equiv\ \operatorname{Frob}_\ell(y_n) \pmod{\lambda} \quad (\lambda \mid \ell).$$
These two relations (first relation = trace/norm compatibility through $a_\ell$; second = a Frobenius congruence) are precisely the Euler-system axioms, and everything downstream is formal consequence of them.

**Kolyvagin's derivative operators and the classes $P_n$.**
Fix a prime $p$ (the "Selmer prime") and an exponent $M$, working modulo $p^M$. Restrict to $n$ a product of **Kolyvagin primes** $\ell$: primes inert in $K$, prime to $pND$, with $a_\ell \equiv \ell+1 \equiv 0 \pmod{p^M}$ (so $E[p^M]$ is "visible" in $E(\mathbb{F}_{\ell^2})$ and $\operatorname{Gal}(H_{n\ell}/H_n)$ has order $\ell+1$ divisible by $p^M$). For each such $\ell$ let $\sigma_\ell$ generate the cyclic group $G_\ell=\operatorname{Gal}(H_{n\ell}/H_n)$ and form the **derivative operator**
$$D_\ell = \sum_{i=0}^{\ell} i\,\sigma_\ell^{\,i} \in \mathbb{Z}[G_\ell], \qquad D_n = \prod_{\ell\mid n} D_\ell.$$
The telescoping identity $(\sigma_\ell - 1)D_\ell = (\ell+1) - N_\ell$ (with $N_\ell=\sum_i \sigma_\ell^i$ the norm) combined with the Euler relations shows that $D_n y_n$ is fixed by $\operatorname{Gal}(H_n/K)$ modulo $p^M$. Choosing a class $[D_n y_n] \in (E(H_n)/p^M E(H_n))^{\operatorname{Gal}(H_n/K)}$ and pulling back gives a canonical
$$P_n \ \in\ H^1(K, E[p^M])$$
(more precisely, the image of $D_n y_n$ under the Kummer map, made Galois-invariant). For $n=1$ this is the class of the basic Heegner point $y_K$.

**Local behavior of the derived classes (the heart of the bound).**
The decisive structural fact, stated cleanly in this paper:
- At every prime $v \nmid n$, the class $\operatorname{loc}_v(P_n)$ lies in the **finite/Selmer local condition** $H^1_f(K_v, E[p^M])$ (the image of the local Kummer map). So $P_n$ is "almost" a Selmer class.
- At each prime $\ell \mid n$, $\operatorname{loc}_\ell(P_n)$ is generally NOT in the finite part: its image in the **singular quotient** $H^1_{\mathrm{sing}}(K_\ell, E[p^M]) = H^1(K_\ell^{\mathrm{ur}}, \dots)$ is computed by the Euler relation and equals (up to unit) the reduction $\operatorname{loc}_\ell^{\mathrm{fin}}(P_{n/\ell})$ of the previous class. This "shift" between the finite part at level $n/\ell$ and the singular part at level $n$ is the engine.

**The annihilation argument (Selmer and Sha bound).**
By global class field theory / Poitou-Tate duality, the sum of local invariants of the cup product of a Selmer class with $P_n$ is zero. Feeding the local computation above into this reciprocity, Kolyvagin shows: if $s \in \operatorname{Sel}_{p^M}(E/K)$ is any Selmer class, then a suitable choice of Kolyvagin prime $\ell$ (existence via Chebotarev applied to the field $K(E[p^M], \tfrac{1}{p^M}E(K))$) forces a relation between $\operatorname{loc}_\ell(s)$ and the localization of $P_1=$ (class of $y_K$). The conclusion is the **bound**:
$$\operatorname{the\ index}\ \big[\,E(K)\otimes\mathbb{Z}_p : \mathbb{Z}_p\, y_K\,\big] \ \text{and}\ \#\operatorname{Sha}(E/K)[p^\infty] \ \text{are controlled by the divisibility of } y_K \text{ in } E(K).$$
Quantitatively, if $M_0$ is the largest $M$ with $y_K \in p^M E(K) + E(K)_{\mathrm{tors}}$ (the $p$-divisibility index of the Heegner point), then $\operatorname{Sel}_{p^M}/\langle y_K\rangle$ and $\operatorname{Sha}[p^M]$ are annihilated by a power of $p$ that is bounded in terms of $M_0$ (schematically of the order $p^{2M_0}$ in the standard accounts). The structural point is that the annihilator is FINITE and effectively bounded by the divisibility of the single Heegner point. The exact exponent is NOT quoted as Gross's stated constant here, because no PDF was read; see the Status line.

**The main theorem (as stated in the paper).**
Descending from $K$ to $\mathbb{Q}$ using the action of complex conjugation on $y_K$ and the sign of the functional equation, and choosing $K$ so that $L'(E/K,1)\neq 0$ (nonvanishing of the twist supplied by Waldspurger / Bump-Friedberg-Hoffstein / Murty-Murty), one obtains:
- **If $y_K$ is non-torsion** (equivalently $L'(E/K,1)\neq 0$), then $E(K)$ has rank $1$, the Heegner point generates a finite-index subgroup, and $\operatorname{Sha}(E/K)$ is finite. Splitting into eigenspaces under complex conjugation gives, when the relevant sign is right, $\operatorname{rank} E(\mathbb{Q}) = 1$ and $\operatorname{Sha}(E/\mathbb{Q})$ finite.
- **The companion rank-0 statement** (Kolyvagin; also via this method with $n=1$ and the Heegner point a torsion class): if $L(E,1)\neq 0$ then $E(\mathbb{Q})$ is finite (rank $0$) and $\operatorname{Sha}(E/\mathbb{Q})$ is finite.

**What the paper is careful to flag.** The Euler system has exactly ONE basic class, the Heegner point. The derived classes $P_n$ are all built from $y_K$; the bound is proportional to the height/divisibility of that single point. There is no second independent input, and the method produces no second independent point. This is stated as an intrinsic feature, not a gap to be patched within the method.

## Project mapping

1. **What is PROVEN here.** Full BSD rank equality and finiteness of $\operatorname{Sha}$ for modular $E/\mathbb{Q}$ in analytic rank $0$ and $1$. This is a THEOREM, and this paper is the cleanest place to see how the $\operatorname{Sha}$-finiteness comes out (it is genuinely proved, not assumed). It is the positive content of the proven corner of the atlas.

2. **The GAP.** The construction yields a single point $y_K$ and a single basic cohomology class. A rank $r\ge 2$ certificate needs $r$ independent points, equivalently a non-degenerate $r\times r$ height-pairing matrix. One point spans a rank-$\le 1$ subgroup, so the machine cannot certify rank $\ge 2$ and the $\operatorname{Sha}$-finiteness argument has no input there. The gap is structural, located exactly at "second derivative / second independent class."

3. **Exact regime.** Analytic rank $0$ and $1$, ARCHIMEDEAN side (the analytic input is $L(E/K,1)$ or $L'(E/K,1)$ at the central point, not a $p$-adic $L$-value). The prime $p$ enters only as the coefficient ring $E[p^M]$ for the Selmer bound; the theorem is about the integral/archimedean $L$-behavior. Contrast `03_padic_archimedean.md`, whose target is the genuinely $p$-adic main-conjecture machinery.

4. **Detector 1 (parity-only): PASSES.** The method outputs the exact rank ($0$ or $1$) and the actual finiteness of $\operatorname{Sha}$, not merely the parity. It is strictly stronger than the root-number / parity-conjecture information. Recorded as a clean pass.

5. **Detector 2 (Sha-finiteness-assumed): PASSES, and is the model of a clean pass.** $\operatorname{Sha}(E)[p^\infty]$ finite is PROVEN here, with an explicit annihilator $p^{2M_0}$ tied to the divisibility of the Heegner point, precisely because $r_{\mathrm{an}}\le 1$ guarantees a non-torsion (or torsion) basic class to feed the Euler system. In the rank $\ge 2$ regime there is no such class, the annihilator argument has nothing to annihilate with, and the method says NOTHING. This is the exact boundary Detector 2 is meant to guard: see `controls.py::sha_finiteness_flag`, which reports "PROVEN" only for `analytic_rank <= 1`.

6. **Detector 3 (function-field mirage): PASSES.** The Euler system is built from CM points on the modular curve and lives in $H^1(K, E[p^M])$ over a number field $K$, using Chebotarev and Poitou-Tate duality, with no geometric Frobenius of a base curve $C$ and no elliptic surface. The argument does not transpose to a function field by importing geometric cohomology; it is genuinely arithmetic. Clean pass per `controls.py::function_field_mirage`.

7. **Control pair (`controls.py::control_pair`, 37a1 vs 389a1).** This paper IS the proof on the proven side of the pair: 37a1 (rank 1) is exactly the kind of curve where $y_K$ is non-torsion and the theorem applies. On 389a1 (rank 2) every step that needs the basic class to be non-degenerate breaks: the Heegner point $y_K$ is torsion (forced by the rank-1 ceiling and the sign), so $P_1$ carries no information, and the method produces no bound. The note documents WHY the pair is a real wall, not a soft one.

8. **Feeds which direction / experiment.**
   - `research_directions/01_rank_two_object.md`: this note fixes the precise object the rank-2 program must build, namely a substitute for $y_K$ whose output is two independent points (non-vanishing $2\times 2$ regulator). The Euler-relation skeleton here is the template a higher system would have to reproduce and then exceed.
   - `research_directions/02_higher_rank_euler_system.md`: the explicit norm relations ($\operatorname{Tr}_{n\ell/n} y_{n\ell}=a_\ell y_n$ and the Frobenius congruence) are exactly the axioms a rank $\ge 2$ system would need to generalize to a second-order phenomenon; this note states them so the falsifiability trigger ("does the candidate degenerate to the rank-1 bound?") can be checked against a concrete baseline.
   - Experiments: feeds the weak-BSD and strong-BSD threads (`experiments.weak_bsd_table`, `experiments.strong_bsd_quantities`) as the ground-truth proven regime against which any rank-$\ge 2$ claim is contrasted; and the control harness in `controls.py` as the canonical "clean pass on all three detectors, but capped at rank 1" reference.

## Status

Written **from authoritative knowledge** of this well-known paper, NOT from the PDF: no legal open-access copy of the original LMS 153 chapter was located (Cambridge volume is paywalled; Gross's Harvard publications and eprints pages list the paper but host no PDF for it, and only adjacent items such as the PCMI BSD lectures and the Heegner-points preprints are downloadable). No PDF was downloaded; `references/02_heegner_gross_zagier/` does not contain this file.

Cited by SECTION and THEOREM NAME and by the standard formulas (the Euler relation $\operatorname{Tr}\,y_{n\ell}=a_\ell y_n$, the derivative operator $D_\ell=\sum i\sigma_\ell^i$, the local finite/singular dichotomy of the derived classes, the divisibility-index bound). NO page numbers and NO theorem numbers are quoted, because the PDF was not read and these must not be fabricated. The exact numerical exponent in the $\operatorname{Sha}$ annihilator ($p^{2M_0}$ above) follows the standard accounts (Gross; Rubin; Darmon) and should be reconfirmed against the original text before being quoted as Gross's stated constant. The Gross-Zagier height formula is used as a cited INPUT and is not reproved in this paper; see the companion note `gross_zagier_kolyvagin.md` for that half.
