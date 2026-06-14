# TODO

Tracked by Constellation. Checkboxes reflect real state.

## Phase 0: Foundation (complete)

- [x] Root docs: README, CLAUDE, OPERATIONS, STATE_OF_THE_PROGRAM, PHASE_STATE
- [x] requirements.txt, .gitignore, .gitattributes
- [x] EllipticCurve / Hasse-Weil L-function interface (`experiments/_shared/elliptic_curve.py`)
- [x] Bundled curve table, ranks 0 to 3, public LMFDB/Cremona invariants (`curve_data.py`)
- [x] Three wrong-approach detectors + control pair (`controls.py`)
- [x] Smoke test, 10/10 passing (`smoke_test.py`; check 7 added 2026-06-09, check 8 + check 9 added 2026-06-12, check 10 added 2026-06-13)
- [x] Experiment (a): analytic rank from L-derivatives
- [x] Experiment (b): weak BSD table (analytic rank vs Mordell-Weil rank)
- [x] Experiment (c): strong BSD quantities, conjectural #Sha
- [x] Experiment (d): Sato-Tate semicircle, a_p pipeline check
- [x] Experiment PLAN.md and LEARNINGS.md
- [x] Layered docs: 00_intuitive, 01_undergraduate, 02_graduate, 03_research
- [x] docs/implications, docs/solutions, docs/research_atlas
- [x] docs/researcher_mindset.md
- [x] Lean 4 skeleton (lakefile, toolchain, BSD.lean, BSD/ modules with documented sorry)
- [x] Six agent role specs (`.claude/agents/`)
- [x] references/README.md, sources/README.md, visualizations/README.md + manim scene
- [x] memory/MEMORY.md

## Phase 1: Mapping (started 2026-06-09: the wall probed computationally)

- [x] Experiment (e) `heegner_ceiling/`: the proven rank-1 machine implemented end to end (modular parametrization, CM points, AGM lattice) and run across the boundary; sets the operational bar any rank-2 construction must beat (non-torsion output on 389a1)
- [x] Experiment (f) `independent_points/`: the constructible half of the rank-2 object built from scratch (exact search + Neron-Tate Gram determinant reproduces all five open-regime regulators at index 1); the upper bound named as the one-sided gap
- [x] Experiment (g) `twist_parity/`: parity-blind locus mapped in twist families of 11a1 and 37a1 (11 analytic-rank-2 twists invisible to the root number)
- [x] Substrate hardening: exact off-center functional-equation check installed as smoke test 7; nine wrong bundled bad-prime a_p signs found and fixed three independent ways
- [x] Score architecture 3 (Iwasawa theory) against the three detectors: full scorecard in `03_padic_archimedean.md` + MTT/Greenberg-Stevens reading note + atlas row (2026-06-12)
- [x] Score architecture 4 (Euler systems) against the three detectors: full scorecard + rank-$\geq 2$ norm relations in `02_higher_rank_euler_system.md` (2026-06-12)
- [x] Specify the rank-2 object precisely: three clauses + executable test battery T1-T4 in `docs/03_research/research_directions/01_rank_two_object.md` (2026-06-11)
- [x] Run the rank-2 spec through Detector 1 and Detector 3 (exclusion sections of the spec; multi-field Heegner retired by Gross-Kohnen-Zagier)
- [x] Experiment (h) `gross_zagier_check/`: numerical Gross-Zagier verified on 4 (E, K) pairs to 1e-20 (37a1 over two fields, 43a1, 53a1); sigma-function heights + Delta < 0 lattice added to the substrate
- [x] Surveyor pass on the Kudla program + Yun-Zhang shtukas (2 reading notes, atlas scorecard rows; the wall localized to two imports: the r legs and the Frobenius twist) (2026-06-11)
- [x] Experiment (i) `strong_bsd_hp/`: strong BSD at working precision in the open regime; #Sha = 1 to within 5e-28 on all five rank >= 2 curves; caught + fixed the wrong bundled 5077a1 regulator (third regulator error) and a silent quadrature precision loss (2026-06-12)
- [x] Experiment (k) `padic_lfunction/`: the p-adic L-function / Mazur-Tate-Teitelbaum thread (architecture 3, computational side). New p-adic engine `_shared/padic.py` (Tate parameter by j-series inversion, Iwasawa log, the $\mathcal{L}$-invariant, ordinary unit root); the exceptional zero classified and $\mathcal{L}_p(E)$ computed to 20 base-$p$ digits across the bundled curves; new smoke check 9 (2026-06-12)
- [x] Experiment (j) `two_descent/`: 2-isogeny descent makes experiment (f)'s upper-bound gap explicit per curve; rank E_34 = 2 proven number-field-free, the rank >= 2 curves shown to carry no rational 2-isogeny (cubic-field obstruction named); new descent engine + smoke check 8 (2026-06-12)
- [x] Experiment (l) `engine/`: the proof-search engine v0. The atlas encoded as a typed AND/OR proof graph (`atlas_graph.py`, 19 nodes / 9 edges), the frontier of the open regime computed (`frontier.py`: minimal open-lemma antichains + leverage, cycle-safe), the three detectors wired as an automatic AUDIT gate (`audit.py`, pure wrapper over `controls.py`), a PROPOSE+FALSIFY mining prototype (`mine.py`), a LOCALIZE pass (`localize.py`: curve x rank + curve x prime residual heat-maps with an automatic break-rank / cliff diagnosis), a PROPOSE construction battery (`propose.py`: candidate classes vs the Direction-01 T1/T2 bar; only T1-passer is non-constructive search, Kudla the live Clause-2 candidate), a VERIFY Lean-obligation emitter (`verify.py` -> `lean/BSD/EngineObligations.lean`, sorry-only, proven: 0, adversary-cleared), and a driver (`e_l_engine.py`); spec in `docs/03_research/engine/README.md`. Frontier of weak BSD rank >= 2 = {rank_two_object}, strong = {rank_two_object, higher_euler_system}, never via parity. Smoke still 10/10 (2026-06-13)
- [x] Experiment (m) `theta_shadow/` + Direction 04: the Kudla Clause-2 front opened. Spec `docs/03_research/research_directions/04_kudla_clause_two_bridge.md` (both bridges stated precisely, Detector-3 audit of each, the two Yun-Zhang function-field imports named as the substitution problem); experiment (m) the computable codim-1 shadow (Waldspurger / Tunnell on the congruent-number family, kappa = Omega/32 constant to ~30 digits, Tunnell coefficients from scratch by lattice counting, n=41 BSD-conditional caveat retained); smoke check 10. Adversary-cleared for Detector 3 + overclaiming. The rank-2 / codim-2 Clause-2 object stays OPEN (2026-06-13)

## Phase 2: Construction (not started)

- [ ] Attempt a higher-rank analog of the Heegner point
- [ ] OR attempt a rank >= 2 Euler system bounding Sha
- [ ] Adversarial review of any construction against all three detectors

## Phase 3: Verification (not started)

- [ ] Expand Lean skeleton: canonical height, Mordell-Weil rank (await Mathlib API)
- [ ] State the Gross-Zagier formula structurally in Lean
- [ ] Formalize any verified structural claim from Phase 2
