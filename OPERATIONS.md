# Operations Guide: running this repo as a BSD proof-program substrate

> How to operate this repository as the substrate for an AI-augmented (and, speculatively, AI-only) proof program for the Birch and Swinnerton-Dyer Conjecture. This guide covers how to launch sessions, deploy agents, maintain state, and escalate to human review. The mathematical content lives in [`experiments/`](experiments/), [`docs/03_research/`](docs/03_research/), and [`lean/`](lean/).

## 1. The repo as substrate

| Component | Path | Role |
|---|---|---|
| Agent role specifications | [`.claude/agents/`](.claude/agents/) | Six agents: surveyor, builder, verifier, adversary, synthesizer, orchestrator. Deployable via the `Agent` tool. |
| Phase state | [`PHASE_STATE.md`](PHASE_STATE.md) | Current phase, sub-task, last verification, next steps. Read by ORCHESTRATOR at session start. |
| Strategic snapshot | [`STATE_OF_THE_PROGRAM.md`](STATE_OF_THE_PROGRAM.md) | One-page repo-wide status: where each architecture stands and the most-leveraged next move. |
| Project narrative | [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md) | Cross-architecture findings. Updated by SYNTHESIZER. |
| Test plan | [`experiments/PLAN.md`](experiments/PLAN.md) | Per-experiment status. |
| Research directions | [`docs/03_research/research_directions/`](docs/03_research/research_directions/) | Per-direction execution roadmaps. |
| Formal verification | [`lean/`](lean/) | Lean 4 / Mathlib. Every structural claim verified here is canonical. |
| Persistent memory | [`memory/MEMORY.md`](memory/MEMORY.md) | Cross-session context. Read at session start. |

## 2. The session loop

### 2.1 Session start

1. ORCHESTRATOR reads [`PHASE_STATE.md`](PHASE_STATE.md) and [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md).
2. ORCHESTRATOR decides the session goal from the prior session's recommended next steps.
3. ORCHESTRATOR deploys agents via the `Agent` tool with `subagent_type` matching the role.

### 2.2 Agent deployment

For mapping work: 1-3 SURVEYORs on the relevant sub-corpus, 3-5 BUILDERs on the same direction with different angles, 1-2 VERIFIERs, 1-2 ADVERSARYs.

For construction work: 5-10 BUILDERs in parallel; VERIFIER and ADVERSARY scale with output.

### 2.3 Synthesis

SYNTHESIZER integrates verified outputs and updates LEARNINGS.md, PLAN.md, PHASE_STATE.md.

### 2.4 Session end

ORCHESTRATOR writes to PHASE_STATE.md: current phase + sub-task, sessions used / budgeted, pending agent outputs, recommended next deployments, falsifiability triggers approaching or hit.

### 2.5 Commit

The session's work is committed with a clear message.

## 3. Verification stack

Every claim passes four layers before becoming canonical:

1. **Mechanical computation**: at least two independent code paths agree (e.g. the bundled `mpmath` AFE vs an independent `pari`/`sage` evaluation if available).
2. **Symbolic verification** where applicable (`sympy`).
3. **Formal proof in Lean 4**: structural claims in [`lean/BSD/`](lean/BSD/) via Mathlib.
4. **Multi-agent consensus**: three independent VERIFIER runs agree.

A claim is canonical only when all four agree. Until then it is provisional.

## 4. Escalation to human review

- **A claimed proof of BSD** (or any sub-case in the open rank $\geq 2$ regime): human peer review before any announcement.
- **A claimed construction of points / a Sha bound in rank $\geq 2$**: this is the open frontier; surface to expert review.
- **A novel object requiring expert judgment** (an arithmetic surface, a new Euler system): expert review of mathematical taste.

ORCHESTRATOR flags such situations and pauses pending human input.

## 5. Falsifiability triggers

The program is restructured if:

- The chosen construction (e.g. a higher-rank generalization of Heegner points) is shown to be structurally parity-only (Detector 1), so it cannot exceed the proven regime.
- A Sha-finiteness input silently assumed in the open regime (Detector 2) cannot be discharged.
- A method proves to be a function-field mirage (Detector 3): it transports verbatim to $\mathbb{F}_q(C)$, so it has not crossed the gap that defines the open problem.

ORCHESTRATOR tracks these in PHASE_STATE.md.

## 6. Current state

**Phase 0 (Foundation) and Phase 1's computational and scoring front are complete.** The repo has:
- The `EllipticCurve` / Hasse-Weil $L$-function interface with point-count $a_p$, multiplicative $a_n$, and the smoothed AFE for $L(E, s)$ and its derivatives at $s = 1$.
- The three wrong-approach detectors plus the proven-vs-open control pair.
- A bundled table of curves (rank 0-3) by Cremona label with public LMFDB/Cremona invariants.
- Thirteen runnable experiments (a)-(n): the substrate validators (analytic rank, weak BSD table, strong BSD quantities, Sato-Tate), the rank-2-wall probes (Heegner ceiling, independent points, twist parity, Gross-Zagier, strong BSD high-precision, 2-descent, the $p$-adic $L$-function), and the live research fronts (the Kudla theta shadow (m), the $p$-adic height regulator (n)). Smoke test 11/11.
- The proof-search engine (experiment (l), [`experiments/engine/`](experiments/engine/)): the atlas as a typed proof graph, the three detectors as an automatic AUDIT gate, and FRONTIER / PROPOSE / LOCALIZE / VERIFY over the bundled curves.
- The layered docs, the research atlas, five numbered research directions (01-05), and the Lean skeleton (with engine-emitted obligations).

**Not yet started**: full multi-agent orchestration software (the proof-search engine is a first, single-process step toward it), Lean Mathlib expansion beyond the skeleton, a serious multi-year compute budget. As of 2026, this is a target design plus a working experimental substrate, not an operating multi-year program.

## 7. For someone picking up this repo

1. **Read** [`PHASE_STATE.md`](PHASE_STATE.md).
2. **Read** [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md).
3. **Read** [`STATE_OF_THE_PROGRAM.md`](STATE_OF_THE_PROGRAM.md).
4. **Read** [`.claude/agents/orchestrator.md`](.claude/agents/orchestrator.md).
5. **Run** the smoke test (11/11) and the experiments to confirm the substrate.
6. **Deploy** the agents ORCHESTRATOR recommends.
7. **Commit** the session's work.
8. **Update** PHASE_STATE.md.
