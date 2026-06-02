# Birch and Swinnerton-Dyer Conjecture: Deep Study Repo

A multi-level exploration of the Birch and Swinnerton-Dyer Conjecture (BSD): from intuitive understanding through graduate-level arithmetic geometry to the frontier of current research. Includes a computational experimental thread organized around testing the candidate BSD proof architectures and a set of wrong-approach detectors that keep claims honest.

**Operational substrate**: this repo is also structured as the substrate for an AI-augmented (and, speculatively, AI-only) proof program for BSD. See [`STATE_OF_THE_PROGRAM.md`](STATE_OF_THE_PROGRAM.md) for a one-page strategic snapshot (where every architecture stands and the single most-leveraged next move), [`OPERATIONS.md`](OPERATIONS.md) for how to operate it, [`PHASE_STATE.md`](PHASE_STATE.md) for current state, and [`docs/03_research/`](docs/03_research/) for the proof program and research directions. The repo is a handoff artifact: Phase 0 infrastructure is in place; the deep phases require expert collaborators and multi-year work.

## What's Here

This repo is structured so you can enter at any level and go as deep as you want.

```
birch-swinnerton-dyer/
├── docs/                        # All written explanations
│   ├── 00_intuitive/            # No math required: rational points, the slope of a curve
│   ├── 01_undergraduate/        # Elliptic curves, the group law, L-series
│   ├── 02_graduate/             # Modularity, Heegner points, Selmer/Sha, the four-level framing
│   ├── 03_research/             # Current approaches, PROOF PROGRAM, research directions
│   │   ├── research_directions/ # Numbered research-grade specs
│   │   └── reading_notes/       # Notes on the reference library
│   ├── implications/            # Why it matters (ranks, cryptography, Diophantine equations)
│   ├── solutions/               # Known approaches to BSD and their obstructions
│   ├── research_atlas/          # Master research map: all attempts, regimes, open problems
│   └── researcher_mindset.md    # Operating philosophy: target not monument
├── experiments/                 # Computational thread; proof-architecture tests
│   ├── PLAN.md                  # Test plan + methodology
│   ├── LEARNINGS.md             # Cross-cutting findings
│   ├── _shared/                 # EllipticCurve / L-function interface + wrong-approach detectors + smoke test
│   ├── l_function_rank/         # (a) analytic rank from L(E,s) derivatives at s=1
│   ├── weak_bsd_table/          # (b) weak BSD: analytic rank == Mordell-Weil rank on a table
│   ├── strong_bsd_quantities/   # (c) Omega, Reg, c_p, torsion -> conjectural #Sha
│   └── sato_tate/               # (d) Sato-Tate semicircle as an a_p sanity check
├── references/                  # Reference library index (gitignored PDFs) + tracked bibliography
├── lean/                        # Lean 4 / Mathlib formal verification (skeleton)
│   ├── lakefile.lean
│   ├── BSD.lean                 # Main module
│   └── BSD/                     # EllipticCurve, MordellWeil, LFunction, RankEquality, RootNumber, ...
├── .claude/agents/              # Six AI agent role specifications
├── sources/                     # Original PDFs and their converted text
├── visualizations/              # manim animation scripts
├── memory/MEMORY.md             # Cross-session context
├── OPERATIONS.md                # How to operate this repo as the proof-program substrate
├── PHASE_STATE.md               # Current operational state
└── CLAUDE.md                    # Project + owner context for AI assistants
```

## The Question

The **Birch and Swinnerton-Dyer Conjecture** states, in its weak form:

> For an elliptic curve $E$ over $\mathbb{Q}$, the order of vanishing of the Hasse-Weil $L$-function $L(E, s)$ at $s = 1$ (the analytic rank) equals the rank of the Mordell-Weil group $E(\mathbb{Q})$.

In its strong form it pins the leading Taylor coefficient of $L(E, s)$ at $s = 1$ to an exact arithmetic expression:

$$\lim_{s \to 1} \frac{L(E, s)}{(s-1)^r} = \frac{\Omega_E \cdot \mathrm{Reg}_E \cdot \prod_p c_p \cdot \#\mathrm{Sha}(E)}{(\#E(\mathbb{Q})_{\mathrm{tors}})^2},$$

where $r$ is the rank, $\Omega_E$ the real period, $\mathrm{Reg}_E$ the regulator of the Neron-Tate height pairing, $c_p$ the Tamagawa numbers, and $\mathrm{Sha}(E)$ the Tate-Shafarevich group.

It has been open since 1965. It is one of the Millennium Prize Problems (worth \$1,000,000). It connects the analytic behavior of an $L$-function to the arithmetic of rational solutions of cubic equations.

## Stance

We are trying to solve this. That is the posture of the whole repo.

It is hard. BSD is fully proven only in the **analytic rank 0 and 1** regimes (Gross-Zagier 1986 + Kolyvagin 1990), and finiteness of $\mathrm{Sha}$, a necessary input to the strong form, is known only there. The rest is open.

Read every negative result here in that spirit. The fact that only ranks 0 and 1 are proven is not a wall; it is a **compass**. It tells us the entire difficulty lives in the **rank $\geq 2$ structure**: the Heegner-point construction that powers the proven regime produces a single point and therefore cannot reach rank 2, so a proof must build something genuinely new where the rank is at least 2. Each "this method only reaches rank 1" is a coordinate that narrows where the real proof must live.

## Levels

| Level | Folder | Prerequisites |
|-------|--------|---------------|
| Intuitive | `docs/00_intuitive/` | None, curiosity only |
| Undergraduate | `docs/01_undergraduate/` | Calculus, modular arithmetic, group basics |
| Graduate | `docs/02_graduate/` | Algebraic number theory, some algebraic geometry |
| Research | `docs/03_research/` | Graduate arithmetic geometry |
| **Research Atlas** | `docs/research_atlas/` | **Start here for the strategic map** of approaches and obstructions |

## Experimental thread

See [`experiments/PLAN.md`](experiments/PLAN.md). Four runnable experiments built on a shared `EllipticCurve` / Hasse-Weil $L$-function interface and three wrong-approach detectors:

- (a) **Analytic rank** from $L(E, s)$ derivatives at $s = 1$ via the approximate functional equation.
- (b) **Weak BSD** on a bundled table of curves of rank 0, 1, 2, 3: analytic rank vs Mordell-Weil rank.
- (c) **Strong BSD quantities**: real period (AGM), regulator, Tamagawa product, torsion, solved for the conjectural $\#\mathrm{Sha}$.
- (d) **Sato-Tate** semicircle as a sanity check on the $a_p$ point-count pipeline.

Smoke test:
```powershell
python -m experiments._shared.smoke_test
```

## Wrong-approach discipline

The Riemann sibling repo uses one counterexample $L$-function (Davenport-Heilbronn) as a wrong-approach detector. BSD's discipline is encoded as three detectors in [`experiments/_shared/controls.py`](experiments/_shared/controls.py):

1. **Parity-only**: the root number gives the analytic rank mod 2, and the parity conjecture (Nekovar; Dokchitser-Dokchitser) gives the Mordell-Weil rank mod 2. A method whose output is only a parity statement cannot prove the full rank equality.
2. **Sha-finiteness assumed**: $\#\mathrm{Sha}$ finite is a theorem only for analytic rank $\leq 1$. Any strong-BSD computation that uses it in the open regime must flag the assumption.
3. **Function-field mirage**: BSD over a function field $\mathbb{F}_q(C)$ is a theorem under finite Sha (Tate; Artin-Tate; Milne). It is the structural template. A method that "works" verbatim over a function field has imported a geometric Frobenius the number-field case lacks.

Plus a **control pair**: a rank $\leq 1$ curve (BSD proven) versus an explicit rank $\geq 2$ curve (BSD open), so a method must show it does something genuinely new in the open regime.

## Status

| Area | Status |
|------|--------|
| Repo structure | Complete |
| Experiments: Phase 0 infrastructure (EllipticCurve / L-function + detectors + smoke test) | Complete, smoke test 6/6 |
| Experiment (a): analytic rank from L-derivatives | Runnable |
| Experiment (b): weak BSD on rank 0-3 table | Runnable |
| Experiment (c): strong BSD quantities -> conjectural #Sha | Runnable |
| Experiment (d): Sato-Tate semicircle | Runnable, matches to chi-square ~0.014 |
| Solutions / approach catalog | `docs/solutions/` |
| Research atlas | `docs/research_atlas/` |
| Docs (intuitive, undergrad, graduate, research) | Substantial |
| Lean 4 / Mathlib skeleton | Skeleton with documented sorries (need not build) |
| manim visualizations | One scene |

## Quick Start

```powershell
# Set up environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Smoke test the experimental framework
python -m experiments._shared.smoke_test

# Run the experiments
python -m experiments.l_function_rank.e_a_analytic_rank
python -m experiments.weak_bsd_table.e_b_weak_bsd
python -m experiments.strong_bsd_quantities.e_c_strong_bsd
python -m experiments.sato_tate.e_d_sato_tate
```
