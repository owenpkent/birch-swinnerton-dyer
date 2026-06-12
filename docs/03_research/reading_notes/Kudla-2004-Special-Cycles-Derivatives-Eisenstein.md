# Reading note: Kudla 2004, "Special cycles and derivatives of Eisenstein series" (the Kudla program)

**Type:** PROGRAM SURVEY (theorems inside it are real but partial). **Regime:** number-field arithmetic geometry; the proven layer parallels analytic rank $\leq 1$ (first central derivatives); the higher-derivative layer is conjectural. **Detector relevance:** the candidate home for Direction 01's Clause 2 (a second-order analytic tie); passes Detectors 1 and 3 structurally; its codimension-1 shadow (Gross-Kohnen-Zagier) is the theorem that retired multi-field Heegner inputs.

Source: S. Kudla, in *Heegner Points and Rankin L-Series*, MSRI Publications 49, Cambridge University Press (2004). Note written from the survey and the surrounding literature; no PDF in the local library yet (note-only source).

## The program in one paragraph

For a quadratic space $V$ of signature $(n, 2)$ (and unitary analogs), the associated Shimura variety $M$ carries SPECIAL CYCLES $Z(T, \varphi)$ of codimension $r$, indexed by positive semidefinite $r \times r$ matrices $T$. Kudla's vision: (1) the generating series $\sum_T Z(T, \varphi) q^T$ is a Siegel modular form of genus $r$ valued in the Chow group $CH^r(M)$; (2) on integral models, the ARITHMETIC versions $\widehat{Z}(T, v)$ (cycles plus Green currents, in Gillet-Soule arithmetic Chow groups) assemble into an arithmetic theta series whose arithmetic degrees match the central DERIVATIVE of a Siegel-Eisenstein series at its center, where the value vanishes for sign reasons (the incoherent case). Slogan: Siegel-Weil computes VALUES of Eisenstein series as degrees of cycles; arithmetic Siegel-Weil computes central DERIVATIVES as heights.

## What is proven (kept strictly separate from the vision)

- **Codimension 1, geometric modularity.** Gross-Kohnen-Zagier (1987) for Heegner divisors on modular curves; Borcherds (1999) for divisor generating series on $O(n,2)$ Shimura varieties; Bruinier and Westerholt-Raum (2015) proved Kudla's modularity conjecture for the full generating series in $CH^r$ over $\mathbb{C}$ in the orthogonal case.
- **Arithmetic Siegel-Weil, low dimension.** Kudla (1997) matched nonsingular coefficients of the genus-2 central derivative with arithmetic intersections on Shimura curves; Kudla-Rapoport-Yang (2006 book) built the modular arithmetic theta series on Shimura curves and proved an arithmetic inner-product formula whose output is a FIRST central derivative.
- **The local engine, unitary case.** The Kudla-Rapoport conjecture (intersection numbers of special cycles on unitary Rapoport-Zink spaces equal derivatives of local representation densities) was proven by Li and W. Zhang (2021), giving arithmetic Siegel-Weil for nonsingular coefficients on unitary Shimura varieties. The arithmetic fundamental lemma (W. Zhang, 2021) powers the arithmetic Gan-Gross-Prasad relative-trace approach in the same spirit.
- **The pattern across all proven cases:** the analytic object is a FIRST central derivative (of an Eisenstein series, or of a Rankin-Selberg / doubling $L$-function via the Rallis inner product). Nothing proven over a number field outputs a second Taylor coefficient of anything, let alone of $L(E, s)$.

## Why this is the live Clause 2 candidate anyway

The program is the only systematic formalism in number-field arithmetic geometry in which HIGHER-codimension cycles are paired with HIGHER-genus Eisenstein series, so it is the natural home for a second-order Gross-Zagier identity: genus-2 data seeing codimension-2 cycles is structurally the shape that $\det R = \kappa \cdot L^{(2)}$ requires. The codimension-1 case already delivered for this program twice: it is Gross-Zagier itself, and it is GKZ, whose one-line proportionality of all Heegner points is what Direction 01 used to retire the multi-field input class (and which experiment (h) exhibited numerically on 37a1).

## The two missing bridges (the honest gaps)

1. **From Eisenstein/doubling $L$-functions to $L(E, s)$.** The arithmetic Siegel-Weil identities concern Eisenstein series and theta lifts; transferring a higher-genus central-derivative statement into Taylor coefficients of the Hasse-Weil $L$-function of a single $E/\mathbb{Q}$ is not part of the proven layer.
2. **From cycle classes to points.** Even granted an arithmetic identity for codimension-2 cycles, the output is an arithmetic intersection number / height of a CYCLE CLASS, not two independent elements of $E(\mathbb{Q})$. The descent from "nonvanishing cycle invariant" to "rank-2 Mordell-Weil certificate" is exactly the part of the spec (Clauses 1 and 2 jointly) that no formalism currently supplies. Compare the function-field side, where Yun-Zhang have the all-orders cycle identity ([`Yun-Zhang-2017-Shtukas-Taylor-Expansion.md`](Yun-Zhang-2017-Shtukas-Taylor-Expansion.md)) and even there points are not produced.

## Detector verdicts

- **Detector 1 (parity-only): PASSES.** The proven outputs are exact height identities and intersection numbers, strictly finer than parity; the conjectural layer aims at full Taylor coefficients.
- **Detector 2 (Sha-finiteness): PASSES (n/a).** No statement in the program assumes or delivers finiteness of $\operatorname{Sha}$; it lives on the points/heights side, which is why it pairs with Direction 02 rather than replacing it.
- **Detector 3 (function-field mirage): PASSES, with a flagged caution.** The arithmetic cycles live on integral models over $\mathbb{Z}$ with genuine Arakelov theory; no geometric Frobenius is imported. The caution: the program's higher-derivative layer is exactly the part that IS a theorem over function fields (Yun-Zhang) and only a vision over $\mathbb{Q}$; any claimed transfer must be audited against the two named imports in the Yun-Zhang note (the extra legs and the Frobenius twist).

## Rank control pair

Nothing here yet runs on 389a1: the program does not currently output points, so T1 of the Direction 01 test battery is not even formulable for it. What it would contribute is the Clause 2 ANALYTIC side (a second-derivative identity); the spec's verdict stands that this is the only input class whose structural shape matches Clause 2 over $\mathbb{Q}$.

## What this feeds

Direction 01's scorecard (the live row). Surveyor follow-ups, in order of leverage: (1) the precise statement of the genus-2 arithmetic Siegel-Weil conjecture for a Shimura curve attached to a rank-2 $E$-relevant quaternion algebra, to see what $\mathrm{Aux}(E)$ literally is; (2) the Rallis inner-product mechanism, to see where a SECOND derivative could enter without vanishing for sign reasons; (3) Bruinier-Yang and Andreatta-Goren-Howard-Madapusi-Pera height formulas as the proven height-side technology.

## Caveats recorded

- This is a survey of a program; the program's headline (arithmetic theta series in all codimensions, matching all higher central derivatives) is CONJECTURAL. Nothing in this note upgrades it.
- The proven unitary-case results (Li-Zhang) concern nonsingular Fourier coefficients; singular coefficients and the full global identity carry additional hypotheses.
- No local PDF; precise theorem numbering deferred until the source is in the library (per PROCESSING_PDFS.md, no page or theorem numbers are cited from memory).
