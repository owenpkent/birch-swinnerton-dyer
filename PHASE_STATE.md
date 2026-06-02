# PHASE_STATE

> Operational state of the BSD proof program. Read by ORCHESTRATOR at session start. Companion to the strategic [`STATE_OF_THE_PROGRAM.md`](STATE_OF_THE_PROGRAM.md) and the synthesis surface [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md). Last updated: 2026-06-02.

## Current phase

**Phase 0: Foundation.** Build the substrate (interfaces, detectors, bundled data, runnable experiments, layered docs, Lean skeleton). This phase is COMPLETE.

| Phase | Goal | Status |
|---|---|---|
| 0. Foundation | EllipticCurve / L-function interface, detectors, bundled curves, runnable experiments, docs, Lean skeleton | COMPLETE |
| 1. Mapping | Score every architecture against the three detectors; specify the rank-2 object precisely | NOT STARTED |
| 2. Construction | Attempt a higher-rank analog of the Heegner point or a rank >= 2 Euler system | NOT STARTED |
| 3. Verification | Formalize verified structural claims in Lean 4 / Mathlib | NOT STARTED |

## Last verification

- `python -m experiments._shared.smoke_test`: 6/6 PASS (2026-06-02).
- Experiment (a) analytic rank: analytic rank matches Mordell-Weil rank on the bundled curves.
- Experiment (b) weak BSD table: rank equality holds on every bundled curve.
- Experiment (c) strong BSD: the BSD formula solved for #Sha lands at a perfect square; AGM reproduces the LMFDB period.
- Experiment (d) Sato-Tate: empirical a_p / (2 sqrt p) tracks the semicircle, validating the point-count pipeline.

## Sub-task in progress

None. Phase 0 is closed. The repo is a handoff artifact awaiting expert collaborators for Phase 1.

## Recommended next steps (for the next session)

1. **Specify the rank-2 object** (the single most-leveraged move from STATE_OF_THE_PROGRAM.md): write down precisely what a rank-2 generalization of the Heegner-point construction must produce, then run it through Detector 1 (parity-only) and Detector 3 (function-field mirage).
2. Score architectures 3 (Iwasawa) and 4 (Euler systems) against the detectors in a research direction document.
3. Expand the Lean skeleton: state the Gross-Zagier formula structurally once Mathlib has canonical heights.

## Falsifiability triggers (none hit)

- Detector 1 (parity-only): not triggered. The experiments use derivative vanishing, not just the root number.
- Detector 2 (Sha-finiteness): correctly flagged OPEN for every rank >= 2 curve.
- Detector 3 (function-field mirage): not triggered. No method here imports a geometric Frobenius.

## Budget

Phase 0 used the scaffolding session. Phases 1 to 3 are multi-year, multi-person, and not yet funded or staffed. This is a target design plus a validated experimental substrate, not an operating program.
