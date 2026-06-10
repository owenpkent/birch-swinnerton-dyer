# TODO

Tracked by Constellation. Checkboxes reflect real state.

## Phase 0: Foundation (complete)

- [x] Root docs: README, CLAUDE, OPERATIONS, STATE_OF_THE_PROGRAM, PHASE_STATE
- [x] requirements.txt, .gitignore, .gitattributes
- [x] EllipticCurve / Hasse-Weil L-function interface (`experiments/_shared/elliptic_curve.py`)
- [x] Bundled curve table, ranks 0 to 3, public LMFDB/Cremona invariants (`curve_data.py`)
- [x] Three wrong-approach detectors + control pair (`controls.py`)
- [x] Smoke test, 7/7 passing (`smoke_test.py`; check 7 added 2026-06-09)
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
- [ ] Score architecture 3 (Iwasawa theory) against the three detectors
- [ ] Score architecture 4 (Euler systems) against the three detectors
- [ ] Specify the rank-2 object precisely (the most-leveraged next move)
- [ ] Run the rank-2 spec through Detector 1 and Detector 3
- [ ] Numerical Gross-Zagier identity check (L'(E/K,1) = c hhat(y_K), extending experiment e)
- [ ] p-adic L-function / Mazur-Tate-Teitelbaum thread (architecture 3 scoring, computational side)
- [ ] 2-descent Selmer bound to make experiment (f)'s upper-bound gap explicit per curve

## Phase 2: Construction (not started)

- [ ] Attempt a higher-rank analog of the Heegner point
- [ ] OR attempt a rank >= 2 Euler system bounding Sha
- [ ] Adversarial review of any construction against all three detectors

## Phase 3: Verification (not started)

- [ ] Expand Lean skeleton: canonical height, Mordell-Weil rank (await Mathlib API)
- [ ] State the Gross-Zagier formula structurally in Lean
- [ ] Formalize any verified structural claim from Phase 2
