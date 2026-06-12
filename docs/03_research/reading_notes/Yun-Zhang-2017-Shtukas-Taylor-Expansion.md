# Reading note: Yun-Zhang 2017, "Shtukas and the Taylor expansion of L-functions"

**Type:** THEOREM (function field). **Regime:** $F = \mathbb{F}_q(X)$, ALL central Taylor coefficients $L^{(r)}$, every $r \geq 0$; everywhere-unramified $PGL_2$ in part I, Iwahori level in part II (2019). **Detector relevance:** the canonical Detector 3 positive control for HIGHER DERIVATIVES: the rank-$\geq 2$ analytic tie exists and is a theorem, but its auxiliary object is built from two imports (extra legs, Frobenius twist) with no known number-field counterparts. This note names them.

Source: Z. Yun and W. Zhang, Annals of Mathematics 186 (2017); part II, Annals of Mathematics 189 (2019). Note written from the papers and surrounding literature; no PDF in the local library yet (note-only source).

## The theorem in one paragraph

Let $X$ be a smooth projective curve over $\mathbb{F}_q$ ($q$ odd), $F = \mathbb{F}_q(X)$, and $X' \to X$ an etale double cover with function field $F'$. For an everywhere-unramified cuspidal automorphic representation $\pi$ of $PGL_2(\mathbb{A}_F)$ and EVERY integer $r \geq 0$, the $r$-th central derivative of the base-change $L$-function $L(\pi_{F'}, s)$ is, up to an explicit positive factor, the self-intersection number of the $\pi$-isotypic part of the HEEGNER-DRINFELD CYCLE:

$$L^{(r)}(\pi_{F'}, 1/2) \sim \left\langle [\mathrm{Sht}^r_T]_\pi,\ [\mathrm{Sht}^r_T]_\pi \right\rangle_{\mathrm{Sht}^r_G}.$$

Here $\mathrm{Sht}^r_G$ is the moduli stack of $G$-shtukas with $r$ modification points ("legs") moving along $X^r$, and $\mathrm{Sht}^r_T$ is the finite cover coming from the torus $T = (\mathrm{Res}_{X'/X}\mathbb{G}_m)/\mathbb{G}_m$, mapped in as a middle-dimensional cycle. For $r = 0$ this is a Waldspurger-type value formula; for $r = 1$ it is the function-field Gross-Zagier; for $r \geq 2$ it is something that DOES NOT EXIST over number fields: an exact geometric identity for the second and higher Taylor coefficients.

## Why this matters to the program (read this twice)

This is the only proven statement in any setting with the SHAPE of Direction 01's Clause 2 at order $r = 2$: an arithmetic-geometric invariant equal to the second central derivative. The one-derivative bottleneck that experiments (e) and (h) measured over $\mathbb{Q}$ (the Heegner machine's entire output is $L'$) is NOT a law of nature: over function fields the tower $r = 0, 1, 2, 3, \ldots$ is uniform, one definition for all $r$. The wall is therefore localized in the two inputs below, not in the idea of higher-derivative formulas.

## The two imports, named (the Detector 3 audit)

1. **The legs.** $\mathrm{Sht}^r_G$ fibers over $X^r$: the $r$ modification points move along $r$ independent copies of the curve. The number-field analog of even $X \times X$ (something like $\mathrm{Spec}\,\mathbb{Z} \times_{\mathbb{F}_1} \mathrm{Spec}\,\mathbb{Z}$) does not exist in current mathematics. One leg degenerates to the classical setting (CM points on modular curves have a number-field life); the SECOND leg is precisely what has no $\mathbb{Q}$-shadow.
2. **The Frobenius twist.** A shtuka is a vector bundle with an isomorphism to its Frobenius pullback away from the legs; the geometric Frobenius $\mathrm{Frob}_q$ enters the definition itself. This is the same import Detector 3 flags in Tate/Milne/Ulmer, now load-bearing inside the higher-derivative mechanism rather than in the Brauer-group bookkeeping.

A candidate construction over $\mathbb{Q}$ claiming Clause 2 must answer, explicitly: what plays the second leg, and what replaces Frobenius twisting? If it cannot, Detector 3 fires.

## What the theorem does NOT give (honesty box)

- It does not produce rational points, even over function fields: the output is an intersection number of a cycle class, and deducing Mordell-Weil rank from $L$-behavior over $\mathbb{F}_q(X)$ still routes through Tate-conjecture / Brauer-finiteness input (Tate, Milne; see [`Milne-1975-Artin-Tate.md`](Milne-1975-Artin-Tate.md)). So even in the best world, a number-field transfer of Yun-Zhang would supply the Clause 2 ANALYTIC TIE, while Clause 1 (two actual points) and Clause 3 (Sha) would still need their own mechanisms.
- The base-change structure means the identity is over $F'$ (the double cover), the function-field analog of the Heegner field $K$; the descent bookkeeping mirrors the $E/K$ vs $E/\mathbb{Q}$ split in Gross-Zagier.
- Part I is everywhere-unramified ($X'$ etale, $\pi$ unramified everywhere); ramification is partially handled in part II (Iwahori level). Nothing here covers the full generality an elliptic-curve application over $\mathbb{F}_q(t)$ with bad reduction would want.

## Detector verdicts

- **Detector 1 (parity-only): PASSES (over-delivers).** Every Taylor coefficient, not parity; the $r$-uniformity is the exact opposite of a parity collapse.
- **Detector 2 (Sha-finiteness): PASSES (n/a).** No Sha input or output; the theorem is on the cycle/L-function side.
- **Detector 3 (function-field mirage): TRIGGERS BY DESIGN.** This note exists to make the trigger PRECISE: two imports, named above. Alongside Ulmer (unbounded rank) and Milne (Artin-Tate), this is the third and sharpest member of the function-field control suite, because it mirrors the exact object Direction 01 wants.

## Rank control pair

Rank-uniform by construction: $r = 1$ and $r = 2$ are the same theorem. The number-field side has $r \leq 1$ (Gross-Zagier) and nothing at $r = 2$; the pair therefore isolates the wall to the two named imports. This is the most informative single comparison the program has.

## What this feeds

- Direction 01, Clause 2: the spec's demand "output whose size is a second Taylor coefficient" is realized here, so the spec is not vacuous; the transfer question is now concrete ("number-field shadow of the 2-legged Heegner-Drinfeld cycle").
- The atlas's function-field section: upgrade from "BSD is a theorem under finite Sha (Tate/Milne)" to "AND the all-orders derivative formula is a theorem (Yun-Zhang)"; the mirage detector gains a second, sharper template.
- Surveyor follow-ups: the relative-trace-formula skeleton of the proof (which parts are Frobenius-free?), and W. Zhang's surveys on arithmetic GGP for the number-field end of the same dictionary.

## Caveats recorded

- No local PDF; theorem statements paraphrased structurally, no numbering cited (per PROCESSING_PDFS.md).
- The positive factor in the identity involves normalizations (Petersson-type norms, $\log q$ powers) suppressed here; any quantitative use must restate them from the paper.
