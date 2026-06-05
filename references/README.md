# References library (reading list)

> Curated reference library for the BSD study program. The PDFs themselves are
> copyrighted and **gitignored** (`*.pdf`); this index is tracked. Organized into eight
> role folders mapped to the proof architectures in
> [`docs/solutions/README.md`](../docs/solutions/README.md). One deep reading note per
> source lives in [`docs/03_research/reading_notes/`](../docs/03_research/reading_notes/).
> **How to add a paper / process a PDF (file -> extract -> note -> index):**
> [`docs/03_research/reading_notes/PROCESSING_PDFS.md`](../docs/03_research/reading_notes/PROCESSING_PDFS.md).
>
> **Local PDF column.** "yes" = an open/legal copy was gathered into the folder (gitignored,
> local only); "note only" = no open PDF was found (paywalled book or restricted journal), so
> the reading note was written from authoritative knowledge and cites by section/theorem.
> Converted text of any primary source we hold lives in [`../sources/`](../sources/).
>
> **Reading order for the live front.** The proven regime is folders 02 + 03 (Heegner +
> Euler systems, analytic rank $\leq 1$); the parity wall is 01 (modularity); the open
> structure lives past them. 06 (function field) is the mirage control; 05 (statistics) sets
> the population picture; 04 (Iwasawa) is the $p$-adic route; 07/08 are substrate and framing.

## 01 Modularity (the parity wall: analytic continuation + functional equation + root number)

| File | Reference | Local PDF | Role |
|---|---|---|---|
| `Wiles-1995-Modular-Elliptic-Curves-and-FLT.pdf` | A. Wiles, "Modular elliptic curves and Fermat's Last Theorem," Ann. of Math. 141 (1995), 443-551 | yes | Modularity for semistable $E/\mathbb{Q}$ via $R = T$; gives $L(E,s)$, the functional equation, and the root number $w$, hence only the PARITY of the analytic rank (Detector 1 source). |
| `Taylor-Wiles-1995-Ring-Theoretic-Hecke-Algebras.pdf` | R. Taylor, A. Wiles, "Ring-theoretic properties of certain Hecke algebras," Ann. of Math. 141 (1995), 553-572 | yes | The patching argument (complete intersection, $R = T$) completing Wiles; makes $L(E,s)$ exist, so its BSD payoff is parity only. Methodological ancestor of Skinner-Urban. |
| `Breuil-Conrad-Diamond-Taylor-2001-Modularity-of-Elliptic-Curves.pdf` | C. Breuil, B. Conrad, F. Diamond, R. Taylor, "On the modularity of elliptic curves over Q: wild 3-adic exercises," J. Amer. Math. Soc. 14 (2001), 843-939 | yes | Full modularity for EVERY $E/\mathbb{Q}$; analytic continuation, functional equation and parity universally, never the rank equality. |

## 02 Heegner points + Gross-Zagier (the proven analytic-rank-1 engine)

| File | Reference | Local PDF | Role |
|---|---|---|---|
| `Gross-Zagier-1986-Heegner-Points-and-Derivatives-of-L-series.pdf` | B. Gross, D. Zagier, "Heegner points and derivatives of L-series," Invent. Math. 84 (1986), 225-320 | yes | The proven archimedean rank-1 height-derivative formula $L'(E/K,1) = c\,\hat h(P_K)$: ONE non-torsion point, structurally capped at rank 1, clean on all three detectors. |
| `Gross-1991-Kolyvagins-Work-on-Modular-Elliptic-Curves.pdf` | B. Gross, "Kolyvagin's work on modular elliptic curves," in L-functions and Arithmetic (Durham 1989), LMS LNS 153 (1991), 235-256 | note only | The cleanest exposition of Kolyvagin's Euler system: Heegner points over ring class fields bound $\mathrm{Sel}$/$\mathrm{Sha}$, giving rank 1 + finite $\mathrm{Sha}$ when $L'(E,1) \neq 0$. |
| `Darmon-2004-Rational-Points-on-Modular-Elliptic-Curves-CBMS.pdf` | H. Darmon, "Rational Points on Modular Elliptic Curves," CBMS 101, AMS (2004) | yes | The Heegner / Stark-Heegner toolkit: rank 1 proven, the $p$-adic real-quadratic extensions conjectural; the one-point ceiling made explicit. |
| `Zhang-2001-Heights-of-Heegner-Points-on-Shimura-Curves.pdf` | S. Zhang, "Heights of Heegner points on Shimura curves," Ann. of Math. 153 (2001), 27-147 | yes | Gross-Zagier generalized to Shimura curves (Heegner hypotheses relaxed); still a one-point (rank-1) formula however general. |

## 03 Euler systems (bounding Selmer and Sha)

| File | Reference | Local PDF | Role |
|---|---|---|---|
| `Kolyvagin-1990-Euler-Systems-Grothendieck-Festschrift.pdf` | V. Kolyvagin, "Euler systems," in The Grothendieck Festschrift II, Progr. Math. 87 (1990), 435-483 | note only (expository copy gathered) | The Euler system of Heegner points bounding $\mathrm{Sel}_p$ and proving $\mathrm{Sha}$ finite, but only at rank $\leq 1$; the single-seed ceiling is intrinsic. Number-field-clean. |
| `Kato-2004-p-adic-Hodge-Theory-and-Values-of-Zeta-Functions.pdf` | K. Kato, "p-adic Hodge theory and values of zeta functions of modular forms," Asterisque 295 (2004), 117-290 | note only | Kato's Euler system (Beilinson elements in $K_2$ of modular curves); one divisibility of the GL2 main conjecture; rank-0 / $p$-part-of-$\mathrm{Sha}$ bounds without CM. |
| `Rubin-2000-Euler-Systems-Annals-Studies-147.pdf` | K. Rubin, "Euler Systems," Annals of Math. Studies 147, Princeton (2000) | note only | The axiomatic Euler-system machine + the CM application (elliptic units prove finite $\mathrm{Sha}$ for CM curves, rank 0); needs a starting class absent at rank $\geq 2$. |
| `Coates-Wiles-1977-On-the-Conjecture-of-BSD.pdf` | J. Coates, A. Wiles, "On the conjecture of Birch and Swinnerton-Dyer," Invent. Math. 39 (1977), 223-251 | yes | The FIRST theorem toward BSD: for CM curves, $L(E,1) \neq 0 \Rightarrow E(\mathbb{Q})$ finite (rank 0). The root of the Euler-system / Iwasawa line. |

## 04 Iwasawa theory / main conjectures / p-adic BSD

| File | Reference | Local PDF | Role |
|---|---|---|---|
| `Mazur-Swinnerton-Dyer-1974-Arithmetic-of-Weil-Curves.pdf` | B. Mazur, P. Swinnerton-Dyer, "Arithmetic of Weil curves," Invent. Math. 25 (1974), 1-61 | yes | Modular symbols and the construction of the $p$-adic $L$-function of an elliptic curve; the analytic engine of the Iwasawa attack and the BSD data. |
| `Mazur-Tate-Teitelbaum-1986-p-adic-Analogues-of-BSD.pdf` | B. Mazur, J. Tate, J. Teitelbaum, "On p-adic analogues of the conjectures of Birch and Swinnerton-Dyer," Invent. Math. 84 (1986), 1-48 | note only | $p$-adic BSD: order of vanishing + leading term of $L_p$, the exceptional (split-multiplicative) zero and the $\mathcal{L}$-invariant; a different object than the complex $L$. |
| `Skinner-Urban-2014-Iwasawa-Main-Conjectures-for-GL2.pdf` | C. Skinner, E. Urban, "The Iwasawa main conjectures for GL2," Invent. Math. 195 (2014), 1-277 | yes | The reverse divisibility (Eisenstein congruences on U(2,2)) completing the main conjecture with Kato; gives the $p$-part of BSD in many rank $\leq 1$ cases. $p$-adic, not archimedean. |

## 05 Statistics / averages (the population picture)

| File | Reference | Local PDF | Role |
|---|---|---|---|
| `Bhargava-Shankar-2015-Binary-Quartic-Forms-Average-Rank.pdf` | M. Bhargava, A. Shankar, "Binary quartic forms having bounded invariants, and the boundedness of the average rank of elliptic curves," Ann. of Math. 181 (2015), 191-242. arXiv:1006.1002 | yes | Average size of 2-Selmer is 3, hence average rank bounded (below 1); a statement about the average, silent on any individual rank-$\geq 2$ curve. |
| `Bhargava-Skinner-Zhang-2014-Majority-Satisfy-BSD.pdf` | M. Bhargava, C. Skinner, W. Zhang, "A majority of elliptic curves over Q satisfy the Birch and Swinnerton-Dyer conjecture," arXiv:1407.1826 (2014) | yes | A positive proportion (> 66%) of $E/\mathbb{Q}$ have analytic rank $\leq 1$ and satisfy BSD; every certified curve is rank 0 or 1, the open regime is the complement. |
| `Goldfeld-1979-Conjectures-on-Elliptic-Curves-Quadratic-Fields.pdf` | D. Goldfeld, "Conjectures on elliptic curves over quadratic fields," in Number Theory Carbondale 1979, LNM 751 (1979), 108-118 | note only | The minimalist conjecture: density 1/2 each for rank 0 and 1, average analytic rank 1/2, rank $\geq 2$ density 0. Density 0 does not mean empty. |
| `Bhargava-Kane-Lenstra-Poonen-Rains-2015-Modeling-Sha-Selmer.pdf` | M. Bhargava, D. Kane, H. Lenstra, B. Poonen, E. Rains, "Modeling the distribution of ranks, Selmer groups, and Shafarevich-Tate groups of elliptic curves," Camb. J. Math. 3 (2015), 275-321. arXiv:1304.3971 | yes | A random-maximal-isotropic / random-matrix model predicting Selmer and $\mathrm{Sha}$ distributions; $\mathrm{Sha}$-finiteness is MODELED, not proven (Detector 2). |

## 06 Function-field template (the mirage control)

| File | Reference | Local PDF | Role |
|---|---|---|---|
| `Tate-1966-BSD-and-a-Geometric-Analog-Bourbaki.pdf` | J. Tate, "On the conjectures of Birch and Swinnerton-Dyer and a geometric analog," Seminaire Bourbaki, Exp. 306 (1966), 415-440 | note only (numdam open; sandbox-blocked) | States strong BSD invariantly and builds the geometric analog: over $\mathbb{F}_q(C)$, BSD $\iff$ finite Brauer group $\iff$ Tate conjecture. The SOURCE of Detector 3. |
| `Milne-1975-On-a-Conjecture-of-Artin-and-Tate.pdf` | J. S. Milne, "On a conjecture of Artin and Tate," Ann. of Math. 102 (1975), 517-533 | yes | Proves Artin-Tate (hence function-field BSD) under finite Brauer group, via geometric Frobenius and Poincare duality on the surface; the sharpest mirage. |
| `Ulmer-2002-Elliptic-Curves-Large-Rank-Function-Fields.pdf` | D. Ulmer, "Elliptic curves with large rank over function fields," Ann. of Math. 155 (2002), 295-315 | yes | Elliptic curves over $\mathbb{F}_q(t)$ of arbitrarily large rank with BSD fully PROVEN; the starkest mirage, full rank-to-infinity BSD via geometry the number field lacks. |

## 07 Foundations / textbooks (descent, Selmer, Sha, heights)

| File | Reference | Local PDF | Role |
|---|---|---|---|
| `Silverman-Arithmetic-of-Elliptic-Curves-GTM106.pdf` | J. H. Silverman, "The Arithmetic of Elliptic Curves," 2nd ed., GTM 106, Springer (2009) | note only | The substrate: Ch VIII (descent, Mordell-Weil, heights), Ch X (Selmer/$\mathrm{Sha}$ and the descent exact sequence). Finiteness of $\mathrm{Sha}$ left OPEN here, the honest baseline. |
| `Silverman-Advanced-Topics-Arithmetic-Elliptic-Curves-GTM151.pdf` | J. H. Silverman, "Advanced Topics in the Arithmetic of Elliptic Curves," GTM 151, Springer (1994) | note only | CM and the local Neron height / canonical-height decomposition (Ch VI); the regulator side of strong BSD, where height-pairing positive-definiteness lives. |
| `Cassels-1966-Diophantine-Equations-Elliptic-Curves.pdf` | J. W. S. Cassels, "Diophantine equations with special reference to elliptic curves," J. LMS 41 (1966), 193-291 | note only | The classic descent survey; introduced $\mathrm{Sel}$/$\mathrm{Sha}$ in modern form and the Cassels-Tate pairing forcing $\#\mathrm{Sha}$ a square when finite (a constraint, not finiteness). |
| `Cremona-Algorithms-Modular-Elliptic-Curves-Ch2.pdf`, `-Ch3.pdf`, `-Contents.pdf` | J. E. Cremona, "Algorithms for Modular Elliptic Curves," 2nd ed., CUP (1997) | yes (Ch 2-3 + contents) | The computational substrate (modular symbols, $L(E,1)$/$L'(E,1)$, periods, regulators); the source of this repo's bundled Cremona invariants. |

## 08 Surveys + originals

| File | Reference | Local PDF | Role |
|---|---|---|---|
| `Birch-Swinnerton-Dyer-1965-Notes-on-Elliptic-Curves-II.pdf` | B. Birch, H. P. F. Swinnerton-Dyer, "Notes on elliptic curves. II," J. Reine Angew. Math. (Crelle) 218 (1965), 79-108 | yes | The ORIGINAL conjecture and the EDSAC computations ($\prod_{p \leq X} N_p/p \sim C (\log X)^r$); the empirical birth of BSD and its defining object. |
| `Wiles-2006-Clay-Birch-Swinnerton-Dyer-Official-Description.pdf` | A. Wiles, "The Birch and Swinnerton-Dyer Conjecture," Clay Millennium Problem official description (2006) | yes | The official statement (weak + strong) and status: proven only for analytic rank 0 and 1; the canonical citation for the rank-boundary wall. |
| `Coates-2013-Lectures-on-the-Birch-Swinnerton-Dyer-Conjecture.pdf` | J. Coates, "Lectures on the Birch-Swinnerton-Dyer conjecture," ICCM Notices 1 (2013), 29-46 | yes | A modern Iwasawa-tradition survey naming finiteness of $\mathrm{Sha}$ and the rank $\geq 2$ cases as the open core. |

## Data sources (bundled curve invariants)

- **The LMFDB Collaboration**, The L-functions and Modular Forms Database, https://www.lmfdb.org. Source of the bundled curve invariants in [`experiments/_shared/curve_data.py`](../experiments/_shared/curve_data.py).
- **J. E. Cremona**, Elliptic Curve Data (ecdata), https://johncremona.github.io/ecdata/. Cremona labels and invariants.

See [`../docs/03_research/reading_notes/`](../docs/03_research/reading_notes/) for the per-source reading notes that record what each source proves, its exact regime, and its detector verdicts.
