# Reading note: B. Mazur, P. Swinnerton-Dyer, "Arithmetic of Weil curves," Inventiones Mathematicae 25 (1974), 1-61.

> **Role in the BSD program.** This is the paper that builds the analytic engine the Iwasawa-theoretic attack runs on: it introduces the modular symbol as a computational and theoretic tool, packages a weight-2 newform's periods into a $p$-adic measure on $\mathbb{Z}_p^\ast$ via the Iwasawa algebra, and out of that measure constructs the $p$-adic $L$-series $L_p(E, \chi, s)$ of an elliptic curve with good ordinary reduction. It is the origin of the object whose interpolation the $p$-adic BSD detector watches, and the source of the four "motivating" $p$-adic BSD conjectures ($\S 9.5$) later organized by Mazur-Tate-Teitelbaum and attacked by Kato and Skinner-Urban. Part I also proves an unconditional, archimedean half-result on fundamental critical points: the analytic rank is bounded above by (and has the same parity as) the count of odd-order $\varphi$-ramification points.
>
> **Reading depth.** Read from the GDZ-hosted PDF (Göttingen digitization, PPN356556735_0025, LOG_0007). Read pages 1-10 (Table of Contents, $\S 1$ Introduction, $\S 2$ Weil curves, including Conjectures A and B and the fundamental-critical-point Theorem), pages 33-36 ($\S 6$ The modular symbol, the functional equation Formula (11), and the opening of $\S 7$), pages 39-43 ($\S 7.3$-$\S 7.4$ Iwasawa algebra and analytic functions on the character group), and pages 49-57 ($\S 8.2$-$\S 8.3$ volumes and finite-character values, $\S 9$ the $p$-adic $L$-series and its functional equation, motivating conjectures, constant term, and finite-character values, $\S 10$ irregular-prime tables). Sections $\S 3$-$\S 5$ (involutory curves, conductor-37 worked example) and the bulk of the $\S 10$ numerical tables were skimmed, not read line by line.
>
> **Cross-links.** Four-level framing: [`docs/02_graduate/`](../../02_graduate/). Three detectors: [`experiments/_shared/controls.py`](../../../experiments/_shared/controls.py). Research directions: [`01_rank_two_object.md`](../research_directions/01_rank_two_object.md), [`02_higher_rank_euler_system.md`](../research_directions/02_higher_rank_euler_system.md), [`03_padic_archimedean.md`](../research_directions/03_padic_archimedean.md). Atlas: [`docs/research_atlas/README.md`](../../research_atlas/README.md), Architecture row 3 (Iwasawa theory).
>
> **How it differs from the related notes.** [`iwasawa_skinner_urban.md`](iwasawa_skinner_urban.md) records the *theorems* (Kato's divisibility, Skinner-Urban's reverse divisibility, the Mazur-Tate-Teitelbaum exceptional zero) that constrain this object decades later. This note records the *construction* of the object itself and the original *conjectures* attached to it. It is upstream of all of them. It is also distinct from [`gross_zagier_kolyvagin.md`](gross_zagier_kolyvagin.md): that note covers the proven archimedean rank-$\leq 1$ regime; this paper is foundational and almost entirely $p$-adic, and proves no rank equality.
>
> **Topic folder.** `references/04_iwasawa_main_conjecture/`. PDF: `Mazur-Swinnerton-Dyer-1974-Arithmetic-of-Weil-Curves.pdf`.

## One-line takeaway

For a Weil curve $E/\mathbb{Q}$ (then conjecturally, now provably by modularity, every $E/\mathbb{Q}$) with good ordinary reduction at $p$, the modular symbol of the associated weight-2 newform defines a $\mathbb{Z}_p$-valued measure $\mu_E$ on $\mathbb{Z}_p^\ast$ whose Iwasawa-algebra element $\alpha_E$ is the $p$-adic $L$-series $L_p(E, \chi, s)$; this $p$-adic analytic function interpolates the critical values $L_\infty(E, \chi, 1)$ of the complex $L$-series, satisfies a functional equation, and vanishes at $s=1$ iff $L_\infty(E, 1)$ does, but the paper proves no rank equality (its BSD content is a set of conjectures, plus one unconditional parity-flavored upper bound on the archimedean analytic rank).

## Technical content (section by section)

### Part I, $\S 2$: Weil curves, winding number, and the BSD conjectures (pp. 4-10)

**Weil parametrization (2.1).** A non-constant morphism $\varphi: X_0(N) \to E$ over $\mathbb{Q}$ sending $i\infty \mapsto 0$. Pulling back the Néron differential, $\varphi^\ast \omega = c \cdot f \cdot dq/q$ with $c \in \mathbb{Q}^\ast$ and $f$ a newform whose $q$-expansion has coefficients $\lambda(n)$, $\lambda(1)=1$, $\lambda(p)=\lambda_p$ at good primes, where $N_p = 1 + p - \lambda_p$ counts $E(\mathbb{F}_p)$ (p. 5). The constant $c = c(\varphi)$ (the "mysterious constant") lies in $\mathbb{Z}' = \mathbb{Z}[1/n]$ and is a unit iff $\varphi$ is étale along the cusp $i\infty$ (Lemma 1, Lemma 2, p. 6). **Weil's conjecture** (p. 6): every elliptic curve over $\mathbb{Q}$ is a weak Weil curve. (This is the modularity conjecture; it is now a theorem of Wiles, Taylor-Wiles, Breuil-Conrad-Diamond-Taylor. The 1974 paper states it as a conjecture and works only with curves known to be modular.)

**Winding number (2.2).** $M \in \mathbb{Q}$ defined by $\int_I \varphi^\ast\omega = M \int_{E(\mathbb{R})} \omega$, with $I = [i\infty, 0]$ the fundamental arc (Formula (1), p. 8). Geometrically $M$ measures the degree of the map $I/(0 \sim i\infty) \to E(\mathbb{R})^{\mathrm{conn}}$.

**Complex $L$-series (2.3).** $L_\infty(E, s) = \sum \lambda(n) n^{-s}$ is the Mellin transform of the newform (p. 8). The central value satisfies
$$L(E, 1) = c(\varphi)^{-1} \int_I \varphi^\ast\omega = M c(\varphi)^{-1} \int_{E(\mathbb{R})} \omega \tag{2}$$
(p. 9), with the **Corollary**: $M = 0$ iff $L(E, 1) = 0$.

**The BSD conjectures, as stated here (p. 9).**
- **Conjecture A.** $\operatorname{rank} E(\mathbb{Q}) = \operatorname{ord}_{s=1} L(E, s)$.
- **Conjecture B.** (1) $M = 0$ iff $E(\mathbb{Q})$ is infinite. (2) If $M \neq 0$,
$$M = c(\varphi) \cdot [\mathrm{III}] / [E(\mathbb{Q})]^2 \prod_p n_p,$$
with $[\,\cdot\,]$ the order of a group and $n_p$ the number of rational components of the Néron fiber at $p$. The paper explicitly flags that Conjecture B "presupposes the conjecture that $\mathrm{III}$ is finite, a fact which remains unproven for any elliptic curve" (p. 9), and cites Cassels for the perfect-square / isogeny-invariance facts. These are conjectures here, not theorems.

**The one unconditional Part-I result (2.4, p. 10).** Define *fundamental critical points* of $E$ as the turning (ramification) points of $\varphi$ on the fundamental arc $I$.

> **Theorem.** *Let $E$ be a Weil curve. The analytic rank of $E$ is less than or equal to the number of fundamental critical points of $E$ of odd order, and these two numbers have the same parity.*

The proof differentiates the Mellin-transform integral $L(E, s) = \frac{1}{c\,\Gamma(s)}\int_0^{i\infty}(-2\pi i \tau)^{s-1}\varphi^\ast\omega$ under the integral sign. Write $m = \operatorname{ord}_{s=1} L(E,s)$ for the analytic rank and $k$ for the number of odd-order fundamental critical points. An $m$-fold zero at $s=1$ forces $J_t = \int_0^{i\infty}(\log(-2\pi i \tau))^t \varphi^\ast\omega = 0$ for $t = 0, \dots, m-1$. The product over the odd-order turning points $\tau_j$ keeps $(\varphi^\ast\omega)\prod_j\{\log(-2\pi i\tau) - \log(-2\pi i\tau_j)\}$ of constant sign, so the associated degree-$k$ integral cannot vanish. Hence there can be at most $k$ vanishing log-moments, i.e. $m \leq k$ (p. 10). This is an **archimedean** statement, and it is an upper bound on the analytic rank plus a parity match, not an equality. It does not prove BSD in any rank.

### Part I, $\S 6$: The modular symbol (pp. 33-35)

For $r \in \overline{U}$ (the extended upper half plane), $\{r\} = \int_{\langle r\rangle} : H^0(Y, \Omega^1_{Y/\mathbb{C}}) \to \mathbb{C}$ is the linear functional given by integrating a holomorphic differential along a path from $0$ to $r$; under $H_1(Y, \mathbb{R}) \cong \operatorname{Hom}_\mathbb{C}(H^0, \mathbb{C})$ it is an element of $H_1(Y, \mathbb{R})$ depending only on $r$ (p. 33). Basic relations: $\{0\}=0$; $\{r_2\} - \{r_1\} = \{\gamma(r_2)\} - \{\gamma(r_1)\}$ for $\gamma \in \Gamma_0(N)$; $\{\gamma(r)\} = \{r\}$ when $\gamma$ has a fixed point; $\{r+1\}=\{r\}$ (Formulas (1)-(5)). By Manin's theorem, for a cusp $r$, $\varphi(r) \in H_1(E, \mathbb{Q})$ (p. 34). Composing with $\varphi$ and using $H^\pm \cong \mathbb{Z}$ gives the integer-valued plus/minus modular symbols
$$\varphi^\pm(r) = \varphi(r) \pm \varphi(-r) \in H^\pm, \qquad r \in (\mathbb{Q}/\mathbb{Z})'$$
(here $(\mathbb{Q}/\mathbb{Z})'$ means rationals mod 1 with denominator prime to $N$), the objects an experiment actually computes by machine. Hecke operators act by
$$T_p\{r\} = \{pr\} + \sum_{k=0}^{p-1}\Big\{\tfrac{r+k}{p}\Big\} - \sum_{k=0}^{p-1}\Big\{\tfrac{k}{p}\Big\} \tag{6}$$
so that $-N_p \varphi(I) = \sum_{k=0}^{p-1}\varphi(k/p)$ in $H_1(E,\mathbb{Z})^+$, equivalently $-2 N_p M = \sum \varphi^+(k/p)$ (Formulas (9)-(10), p. 35). The Atkin-Lehner involution $w: z \mapsto -1/Nz$ acts with eigenvalue $\varepsilon = \pm 1$ (the **sign of the Weil curve**, the root number), and the modular symbol satisfies the **functional equation**
$$\varphi w = -\varepsilon\,\varphi. \tag{11}$$
This Formula (11) is the seed of the $p$-adic functional equation in $\S 9.4$.

### Part II, $\S 7$: $p$-adic Fourier analysis and the Iwasawa algebra (pp. 36-46)

Distributions $\operatorname{Dist}(T, W) = \operatorname{Hom}(\operatorname{Step}(T), W)$; a distribution is a **measure** when bounded (so its integrals against continuous functions converge). For a compact group $G = \varprojlim G/G_n$ with coefficient ring $D$ (a complete DVR finite over $\mathbb{Z}_p$), the **Iwasawa algebra** is
$$\Lambda = D[[G]] = \varprojlim_n D[G/G_n],$$
and $\operatorname{Dist}(G, D) \xrightarrow{\sim} \Lambda$ (Corollary, p. 39): measures are exactly Iwasawa-algebra elements. A character $\chi: G \to D^\ast$ extends to $\rho: \Lambda \to D$, $\rho(\alpha) = \int_G \chi \cdot \mu_\alpha$ (p. 40). For a group with a **linear $p$-adic structure** $G = C \times H$, $C$ finite of order prime to $p$ and $\gamma: \mathbb{Z}_p^d \xrightarrow{\sim} H$, one gets $\Lambda_G \cong D[C] \otimes_D D[[T_1, \dots, T_d]]$ (Lemma, p. 41), and in the "sufficiently large $D$" special case $\Lambda_G \cong \prod_\chi D[[T]]$ over tame characters $\chi$ (Corollary, p. 42). Each tame character $\chi$ thus yields a power series $L(\alpha, \chi, T)_{(\gamma)} \in D[[T]]$ (Formula (3), p. 42). The Iwasawa algebra is identified with an algebra $F(X, D)$ of $D$-valued analytic functions on the character group $X = \operatorname{Hom}(G, D^\ast)$ ($\S 7.4$, p. 43): $\alpha \mapsto \alpha(x) = \int_G x \cdot \mu_\alpha$ is an isomorphism onto a subalgebra of analytic functions. This is the conceptual core: a measure becomes an analytic function on character space.

### Part II, $\S 8$: Hecke operators, volumes, finite-character values (pp. 47-50)

For an eigenfunction $f$ of $T_p$ with unit eigenvalue $\lambda_p$ (the **good ordinary** hypothesis), set $S_m = \sum_a f(a/\Delta_m)$ over $(\mathbb{Z}/\Delta_m)^\ast$, $S = S_1$. The **volume** of the measure $\mu = \mu^{\Delta, f}$ is $I = \int_{\mathbb{Z}_\Delta} \mu = \lim_m \pi^{-m} S_m$, and

> **Proposition (8.2, p. 49).** $\displaystyle I = \frac{-N_p \cdot S}{(\pi^2 - p)(1 - \bar\pi)^2}$,

where $\pi$ is the $p$-adic unit root of $X^2 - \lambda_p X + p = 0$, $\bar\pi = p/\pi$, and $N_p = (1-\pi)(1-\bar\pi) = 1 + p - \lambda_p$. (The unit root exists exactly because reduction is ordinary; this is where ordinariness is consumed.) On a finite character $\chi$ of conductor $\Delta_r$, with $G(\chi) = \sum_a \chi^{-1}(a) f(a/\Delta_m)$,

> **Proposition (8.3, p. 50).** $\displaystyle L(\chi) = \int \chi \cdot \mu^{\Delta, f} = \frac{\pi^{1-r}}{\pi - \bar\pi} G(\chi)$.

These two formulas are the interpolation property in raw form: the measure's integral against a character recovers a (twisted, $\pi$-scaled) Gauss-sum / $L$-value $G(\chi)$.

### Part II, $\S 9$: The $p$-adic $L$-series of a Weil curve (pp. 50-55)

**Definition (9.1, p. 50).** Let $E$ be a Weil curve of conductor $N$ prime to $p$ with **good ordinary reduction at $p$**. From the modular symbol $\varphi: (\mathbb{Q}/\mathbb{Z})' \to H = H_1(E,\mathbb{Z})$, split into even/odd parts $\varphi^\pm$, build the $H \otimes \mathbb{Z}_p$-valued eigen-measure $\mu = \mu^{\Delta, \varphi}$ on $X = \operatorname{Hom}(\mathbb{Z}_\Delta^\ast, D^\ast)$; project via the sign-decomposition to a $\mathbb{Z}_p$-valued measure $\mu^{\mathrm{sign}}$. The **$\mathbb{Z}_p$-valued measure associated to $E$** is
$$\mu_E = c \cdot \mu^{\mathrm{sign}},$$
$c$ the constant of $(2.1)$, and the **$p$-adic $L$-series of $E$** is the Iwasawa element $\alpha_E$ read against characters:
$$L(E, \chi) = c \int_{\mathbb{Z}_\Delta^\ast} \chi \cdot \mu^{\mathrm{sign}}.$$

**The $s$-plane form (9.2, p. 51-52).** With the product decomposition $\mathbb{Z}_\Delta^\ast = (\mathbb{Z}/\Delta_1)^\ast \times U$ and Teichmüller character $\omega$, a topological generator $\gamma \in U$ gives a power series $L(E, \chi, T)_{(\gamma)} \in D[[T]]$ whose polynomial part $G(E, \chi, T)_{(\gamma)} \in D[T]$ is the **analytically-defined characteristic polynomial of $E$** (at $\chi$, structure $\gamma$). Shifting $T \to U$ defines the **$p$-adic $L$-series in the $s$-plane**:
$$L_p(E, \chi, s) = L(\alpha_E, \chi, s-1) \in D[[s]],$$
the shift by 1 only to match the classical normalization. Over a finite abelian field $K/\mathbb{Q}$, $L_p(E/K, s) = \prod_\chi L_p(E, \chi, s)$ over characters belonging to $K$.

**Functional equation (9.4, p. 52-53).** From Formula (11), $\mu_E(g) = -\varepsilon \cdot \mu_E(-1/Ng)$, hence
$$L(E, \chi^{-1}) = -\varepsilon \cdot \chi(-N) \cdot L(E, \chi),$$
and in the $s$-plane
$$L_p(E, \chi^{-1}, s) = -\varepsilon\,\chi(-N)\langle -N\rangle^{1-s} L_p(E, \chi, 2-s).$$

**The four motivating conjectures (9.5, p. 53-54).** For $E$ a Weil curve, $p \nmid N$ ordinary, $A/\mathbb{Q}$ finite abelian:
- **Conjecture 1.** $L_p(E/A, s)$ does not vanish identically in $s$.
- **Conjecture 2.** $\operatorname{ord}_{s=1} L_p(E/A, s) = \operatorname{rank} E(A)$. (This is the $p$-adic analog of weak BSD. It is a conjecture, in every rank.)
- **Conjecture 3.** If $p \neq 2$, the analytically-defined characteristic polynomial equals the **algebraically-defined** characteristic polynomial $G^{\mathrm{alg}}(E/A, T)_{(\gamma)}$ of the $\Gamma$-extension (this is the seed of the **Iwasawa Main Conjecture** for $E$, identifying a $p$-adic $L$-function with a Selmer/Iwasawa-module characteristic ideal; for $p=2$ only a constant-factor ambiguity is conjectured).
- **Conjecture 4.** A relative $p$-adic BSD: for $n \geq 3$ with $E(A_{n-1}) = E(A_n)$, a ratio of $\#\mathrm{III}(E/A_n)$ over a cyclotomic step equals $e \cdot \lim_{s\to 1} L_p(E/A_n, s)/L_p(E/A_{n-1}, s)$ with an explicit period/Frobenius factor $e$.

The authors explicitly name **two gaps** they cannot fill (p. 54): a "fine" $p$-adic BSD giving $\lim_{s\to 1}(s-1)^{-\rho}L_p(E/A, s)$ in terms of $\mathrm{III}$ and a $p$-adic regulator of heights; and a relation between $p$-adic $L$-values at integers and classical $L$-values. These two gaps are essentially Direction 03's open comparison.

**Constant term and central value (9.6, p. 54-55).** Over $\mathbb{Q}$ with $\Delta_0=1$, the volume $I$ is the value $L_p(E/\mathbb{Q}, 1)$, and
$$L_p(E/\mathbb{Q}, 1) = I = \frac{c \cdot \lambda \cdot N_p^2 \cdot M}{(\pi^2 - p)(1 - \bar\pi)^2}.$$
**Corollary 1:** $L_p(E/\mathbb{Q}, s)$ vanishes at $s=1$ iff the complex $L$-series vanishes at $s=1$ (because $L_p(E/\mathbb{Q},1)=0 \iff M=0 \iff L_\infty(E,1)=0$). This is the central interpolation/comparison statement: **at $s=1$, $p$-adic and complex vanishing coincide**, but it is a statement about the *value at one point*, not the *order of vanishing*. **Corollary 2** lists equivalent unit conditions ($I$, $N_p$ $p$-adic units; $\lambda_p \not\equiv 1 \bmod p$; $L_p$ trivial on wild characters; $G_p = 1$).

### Part II, $\S 10$: Irregular primes and zero tables (pp. 56-57)

The polynomial part $G_i = G_i(T)_{(\gamma)}$ of $L(E, \omega^i, T)$ factors as $G_i = G_i^{\mathrm{III}} \cdot G_i^{\mathrm{M\text{-}W}}$, the second being the "cyclotomic" Weierstrass-prepared part (roots $T = \zeta - 1$, $\zeta$ a $p^\nu$-th root of unity), the first carrying the conjectural $\mathrm{III}$-contribution. The functional equation gives $\deg G_i = \deg G_{p-1-i}$, and at $i = (p-1)/2$ predicts $(-1)^r = \varepsilon \cdot \left(\tfrac{-N}{p}\right)$ for $r = \operatorname{ord}_{T=0} G_{(p-1)/2}$. A pair $(p, i)$ is **irregular for $E$** when $G_i^{\mathrm{III}}$ is not a unit, the $p$-adic analog of irregular primes. Computed (Stephens-Davenport program) for $E = X_0(11)$, $p \leq 347$ and $E = X_0(17)$, $p \leq 179$: e.g. for $X_0(11)$ the only non-monic $G_i$ occurs at $p=5$.

## Project mapping

1. **What is PROVEN here vs the GAP.** Proven: the *construction* of $\mu_E$, $L(E,\chi)$, and $L_p(E,\chi,s)$ (a genuine $p$-adic analytic object), its functional equation ($\S 9.4$), the interpolation/value formulas ($\S 8.2$-$\S 8.3$, $\S 9.6$), and one unconditional archimedean inequality on the analytic rank ($\S 2.4$ Theorem). GAP: every BSD-flavored statement linking this object to ranks or $\mathrm{III}$ is a **Conjecture** (A, B in Part I; 1-4 in $\S 9.5$). The paper proves no rank equality and no finiteness of $\mathrm{III}$, and says so in print ("a fact which remains unproven for any elliptic curve," p. 9).

2. **Exact regime.** Foundational and almost entirely **$p$-adic** (Part II). The one archimedean result ($\S 2.4$) is an upper bound on the analytic rank with matching parity, valid for all ranks but delivering an *inequality plus parity*, not equality. The $p$-adic construction requires **good ordinary reduction at $p$** and $p \nmid N$ (the unit root $\pi$ of $X^2 - \lambda_p X + p$ must exist; $\S 8.2$, $\S 9.1$). No rank restriction is imposed on the *conjectures*, but no rank is *proven*: Conjecture 2 ($p$-adic rank equality) is open in rank $0$, $1$, and $\geq 2$ alike as of this paper.

3. **Detectors.**
   - **Detector 1 (parity-only): TRIGGERED, in Part I.** The $\S 2.4$ Theorem pins the analytic rank only to an upper bound (the count of odd-order critical points) together with a *parity* match against that count; the root number $\varepsilon$ ($\S 6$, Formula (11)) is exactly a parity datum. By itself this is parity-level information, not rank-closing: it cannot certify the exact analytic rank, let alone the Mordell-Weil rank. The note flags it.
   - **Detector 2 (Sha-finiteness): PASSES (honestly), but the object it builds is where the assumption later hides.** The paper does not assume $\mathrm{III}$ finite to prove anything; it states finiteness as an open hypothesis (p. 9) and isolates the $\mathrm{III}$-contribution into a separate conjectural factor $G_i^{\mathrm{III}}$ ($\S 10$). The downstream theorems (Skinner-Urban) control $\mathrm{III}[p^\infty]$ for individual $p$; assembling all $p$ in rank $\geq 2$ stays open. This paper is the clean origin: it never overclaims.
   - **Detector 3 (function-field mirage): PASSES.** Pure number-field $\mathbb{Q}$ / cyclotomic $\mathbb{Z}_p$-tower construction. The $p$-adic interpolation replaces, rather than imports, a geometric Frobenius; there is no function-field shortcut.

4. **Control pair (rank $\leq 1$ proven vs rank $\geq 2$ open).** This paper sits *before* the control pair: it predates Gross-Zagier-Kolyvagin and proves rank equality in neither regime. Its lasting value is that it pins the $p$-adic side of strong BSD as a *factored* target (Conjectures 3 and 4, the $G^{\mathrm{III}}$ / $G^{\mathrm{M\text{-}W}}$ split) so that later work can attack one factor at a time. The rank-$\geq 2$ object the program needs is invisible to the modular symbol the same way it is invisible to a single Heegner point: $L_p$ records order-of-vanishing only conjecturally (Conjecture 2), and the $\S 2.4$ archimedean result is only an upper bound on the analytic rank.

5. **What it feeds.** Primarily **Research Direction 03** ([`03_padic_archimedean.md`](../research_directions/03_padic_archimedean.md)): this is the source of $L_p(E, \chi, s)$, the order-of-vanishing of which Direction 03 wants to bridge to the archimedean leading term; the paper's own "two gaps" ($\S 9.5$, a fine $p$-adic BSD and a $p$-adic-to-classical value comparison) are literally Direction 03's open comparison, stated in 1974. Secondary feed to **Direction 02** ([`02_higher_rank_euler_system.md`](../research_directions/02_higher_rank_euler_system.md)): Conjecture 3 is the Main-Conjecture seed an Euler system would prove. Experiments: the modular-symbol formulas ($\S 6$, Formulas (6)-(11)) and the $L_p(E/\mathbb{Q},1)$ formula ($\S 9.6$) are directly machine-computable and feed the $p$-adic-$L$ interpolation checks in the experimental thread.

## Status

Read from the GDZ PDF (`references/04_iwasawa_main_conjecture/Mazur-Swinnerton-Dyer-1974-Arithmetic-of-Weil-Curves.pdf`, Göttingen PPN356556735_0025 / LOG_0007, 4.6 MB, verified PDF v1.3). Pages actually read: 1-10 (TOC, $\S 1$, $\S 2$ with Conjectures A/B and the $\S 2.4$ Theorem), 33-36 ($\S 6$ modular symbol and Formula (11), opening of $\S 7$), 39-43 ($\S 7.3$-$\S 7.4$), 49-57 ($\S 8.2$-$\S 8.3$, all of $\S 9$, $\S 10$). Page and formula numbers above are taken directly from the PDF; theorem and conjecture statements are quoted or closely paraphrased from those pages. **Not read line by line:** $\S 3$ (involutory curves), $\S 4$ (tables of critical points), $\S 5$ (the conductor-37 worked example with the $E, F, G$ isogeny analysis), $\S 7.1$-$\S 7.2$ and $\S 7.5$-$\S 7.6$ (the elementary distribution/measure preliminaries and the multiplicative-group/finite-character determination, skimmed), and the bulk of the $\S 10$ numerical tables (read the framing and the $X_0(11)$ synopsis, not every entry). No claim above rests on an unread page.
