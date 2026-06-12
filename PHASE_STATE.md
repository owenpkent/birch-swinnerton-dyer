# PHASE_STATE

> Operational state of the BSD proof program. Read by ORCHESTRATOR at session start. Companion to the strategic [`STATE_OF_THE_PROGRAM.md`](STATE_OF_THE_PROGRAM.md) and the synthesis surface [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md). Last updated: 2026-06-11.

## Current phase

**Phase 1: Mapping (STARTED).** The computational side of mapping is underway: the proven machine has been implemented and its ceiling measured (experiment e), the constructible half of the rank-2 object built (experiment f), the parity-blind locus mapped in a family (experiment g), and the Gross-Zagier identity itself verified to 20 digits with all factors computed independently (experiment h). The written architecture scorecards and the precise rank-2 object spec remain.

| Phase | Goal | Status |
|---|---|---|
| 0. Foundation | EllipticCurve / L-function interface, detectors, bundled curves, runnable experiments, docs, Lean skeleton | COMPLETE |
| 1. Mapping | Score every architecture against the three detectors; specify the rank-2 object precisely | STARTED 2026-06-09 (computational probes e, f, g, h done; written scorecards and spec pending) |
| 2. Construction | Attempt a higher-rank analog of the Heegner point or a rank >= 2 Euler system | NOT STARTED (operational bar now defined by experiment e) |
| 3. Verification | Formalize verified structural claims in Lean 4 / Mathlib | NOT STARTED |

## Last verification

- `python -m experiments._shared.smoke_test`: 7/7 PASS (2026-06-10). Check 7 (new): exact off-center functional equation for every bundled curve, 12 digits.
- Experiments (a)-(d): re-verified 2026-06-10 after the bad-a_p data fix (see below).
- Experiment (e) heegner_ceiling: 37a1 -> exact rational point (1357/841, 28888/24389), height = 144 x regulator (Heegner index 12); 389a1 and 5077a1 -> the zero point. The rank-1 ceiling measured; parity ruled out as the explanation (5077a1 shares w = -1 with 37a1).
- Experiment (f) independent_points: generators found by exact search on all five open-regime curves; Neron-Tate Gram determinant reproduces every LMFDB regulator at index 1 (rank lower bounds certified; upper bound identified as the one-sided gap).
- Experiment (g) twist_parity: 131 twists of 11a1/37a1 scanned with closed-form central values; 11 parity-blind analytic-rank-2 twists found (e.g. 11a1 x -47); four confirmed rank exactly 2 via the AFE; every root number cross-checked against the Fricke fixed point.
- DATA FIX (2026-06-09): nine bundled bad-prime a_p signs were wrong (37a1, 43a1, 53a1, 57a1, 58a1, 433a1, 571a1, 643a1, 5077a1); found by experiment (g)'s functional-equation self-check, confirmed by the -c6 split criterion and the prime-level identity a_N = w, fixed in curve_data.py, guarded forever by smoke check 7 and a build-time root-number consistency assert.
- DATA FIX (2026-06-10): the corrected a_p exposed two compensating errors: the bundled regulators of 57a1 and 58a1 (now 0.0375746 and 0.0424203, generators (2,1) and (0,1) re-derived by exact search + doubling) and 58a1's Tamagawa product (2, not 1; nonsplit I_2 at p = 2). Experiment (c) now gives #Sha = 1.0000 on all 15 curves; experiments (a), (b), (d) re-verified 15/15 after both fixes.
- Experiment (i) strong_bsd_hp (2026-06-11/12): strong BSD rebuilt at working precision in the open regime (sigma-function regulators to 20 digits, Cauchy-integral leading coefficients): #Sha = 1 to within 4.5e-28 on all five rank >= 2 curves. First run caught TWO substrate flaws: the bundled 5077a1 regulator was wrong at 3.4e-4 (now 0.4171435588, confirmed by heights, doubling, and the L-side to 20 digits: fourth data-integrity instance) and the rhombic period quadrature silently lost 5 digits on 571a1 (vertex-breakpoint fix). Experiments (c), (f), smoke 7/7 re-verified after the data fix.
- Experiment (h) gross_zagier_check (2026-06-11): the Gross-Zagier identity L'(E,1) L(E_D,1) = Vol(Lambda) hhat(P)/sqrt|D| verified with every factor computed independently: 37a1 over Q(sqrt -67) and Q(sqrt -11), 43a1 and 53a1 over Q(sqrt -163); worst |ratio - 1| = 5.7e-25 after the period-quadrature breakpoint fix (the first run's 1e-20 outlier on 43a1 was quadrature softness); Heegner indices exactly integral (6, 1, 7, 5). New substrate: period lattice extended to Delta < 0 (rhombic, direct period integrals), and sigma-function canonical heights to ~20 digits ([`experiments/_shared/analytic_height.py`](experiments/_shared/analytic_height.py)), normalization pinned by quadraticity + three bundled regulators. Smoke test still 7/7.

## Sub-task in progress

None blocking. New shared machinery available to all future experiments: exact group law + Neron-Tate heights ([`experiments/_shared/rational_points.py`](experiments/_shared/rational_points.py)), period lattice + Weierstrass parametrization ([`experiments/_shared/period_lattice.py`](experiments/_shared/period_lattice.py)).

## Recommended next steps (for the next session)

1. DONE 2026-06-11: **the rank-2 object is specified precisely** ([`docs/03_research/research_directions/01_rank_two_object.md`](docs/03_research/research_directions/01_rank_two_object.md)): three clauses (nondegeneracy on 389a1, second-order analytic tie, Sha control), an executable test battery T1-T4 wired to experiments (e)-(h), and multi-field Heegner inputs retired by Gross-Kohnen-Zagier (proportionality exhibited numerically in (h): both fields' points on 37a1 are multiples of the same generator).
2. DONE 2026-06-11: **surveyor pass on the Kudla program**, two new reading notes ([Kudla 2004](docs/03_research/reading_notes/Kudla-2004-Special-Cycles-Derivatives-Eisenstein.md), [Yun-Zhang 2017](docs/03_research/reading_notes/Yun-Zhang-2017-Shtukas-Taylor-Expansion.md), both note-only, indexes + atlas scorecard updated). Verdict: the program's proven number-field layer is first-derivative only; Yun-Zhang's all-orders theorem over function fields localizes the wall to two named imports (the r moving legs over X^r, the Frobenius twist). Direction 01's sharpest current question: what replaces those two imports over Q.
3. Score architectures 3 (Iwasawa) and 4 (Euler systems) against the detectors in a research direction document; the computational side of 3 is a p-adic L-function (Mazur-Tate-Teitelbaum) thread.
4. 2-descent Selmer bounds on the bundled rank-2 curves, to exhibit the upper-bound gap of experiment (f) curve by curve.
5. DONE 2026-06-12: **the high-precision regulator pipeline** (experiment (i) strong_bsd_hp): #Sha = 1 to 27+ digits on every open-regime curve; found and fixed the wrong bundled 5077a1 regulator and a quiet quadrature precision loss on the way.

## Falsifiability triggers (none hit)

- Detector 1 (parity-only): not triggered by any method here; positively EXHIBITED by experiments (e) and (g) as a property of the landscape (the machine's ceiling is not parity; 11 twists are invisible to w).
- Detector 2 (Sha-finiteness): correctly flagged OPEN for every rank >= 2 curve; experiment (f) shows the missing input is exactly one-sided (upper bound).
- Detector 3 (function-field mirage): not triggered. No method here imports a geometric Frobenius; experiment (f) names the absent object (H^2 of the arithmetic surface).

## Budget

Phase 0 used the scaffolding session. The 2026-06-09/10 session opened Phase 1's computational front locally (experiments e, f, g plus substrate hardening). The 2026-06-11 session closed the numerical Gross-Zagier item (experiment h) and added the Delta < 0 lattice and sigma-height substrate. The written scorecards, the rank-2 spec, and Phases 2 to 3 remain multi-year, multi-person work.
