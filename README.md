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
│   │   ├── reading_notes/       # Notes on the reference library
│   │   └── engine/              # Design doc for the proof-search engine
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
│   ├── sato_tate/               # (d) Sato-Tate semicircle as an a_p sanity check
│   ├── heegner_ceiling/         # (e) the Heegner machine run across the rank boundary
│   ├── independent_points/      # (f) r independent points + regulator from scratch (rank >= 2)
│   ├── twist_parity/            # (g) twist family scan: where the root number goes blind
│   ├── gross_zagier_check/      # (h) numerical Gross-Zagier, every factor independent
│   ├── strong_bsd_hp/           # (i) strong BSD at working precision in the open regime
│   ├── two_descent/             # (j) 2-isogeny descent: the rigorous rank upper bound
│   ├── padic_lfunction/         # (k) p-adic L-function: exceptional zero + MTT L-invariant
│   └── engine/                  # (l) the proof-search engine: atlas-as-graph, frontier, AUDIT gate
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

See [`experiments/PLAN.md`](experiments/PLAN.md). Eleven runnable experiments built on a shared `EllipticCurve` / Hasse-Weil $L$-function interface and three wrong-approach detectors, plus a proof-search engine that ties them into one loop:

- (a) **Analytic rank** from $L(E, s)$ derivatives at $s = 1$ via the approximate functional equation.
- (b) **Weak BSD** on a bundled table of curves of rank 0, 1, 2, 3: analytic rank vs Mordell-Weil rank.
- (c) **Strong BSD quantities**: real period (AGM), regulator, Tamagawa product, torsion, solved for the conjectural $\#\mathrm{Sha}$.
- (d) **Sato-Tate** semicircle as a sanity check on the $a_p$ point-count pipeline.
- (e) **Heegner ceiling**: the proven rank-1 machine (modular parametrization + CM points), run identically on 37a1 (rank 1), 389a1 (rank 2) and 5077a1 (rank 3), measuring exactly where and why it dies.
- (f) **Independent points**: the constructible half of the rank $\geq 2$ object, $r$ independent points with the regulator rebuilt from scratch by exact arithmetic.
- (g) **Twist parity scan**: quadratic twist families with closed-form central values; locates the twists whose analytic rank 2 is invisible to the root number.
- (h) **Gross-Zagier check**: the identity behind the only proven regime, verified to 24 digits with every factor (the Heegner point, its $\sigma$-function height, both $L$-values) computed independently.
- (i) **Strong BSD high precision**: $\#\mathrm{Sha} = 1$ to 27 digits on all five open-regime curves, with $\sigma$-function regulators and Cauchy-integral leading coefficients rebuilt from scratch.
- (j) **2-isogeny descent**: the rigorous rank UPPER bound (f) leaves open, number-field-free; pins $\mathrm{rank}\,E_{34} = 2$ with no BSD input and names the cubic-field obstruction on the rank $\geq 2$ curves that carry no rational 2-isogeny.
- (k) **p-adic L-function**: the Mazur-Tate-Teitelbaum thread (architecture 3); the exceptional zero classified and the $\mathcal{L}$-invariant computed to 20 base-$p$ digits across the bundled curves.

Built on the same substrate and detectors, a **proof-search engine** ([`experiments/engine/`](experiments/engine/), spec in [`docs/03_research/engine/`](docs/03_research/engine/README.md)) encodes the research atlas as a typed proof graph and computes the frontier of the open regime: weak BSD in rank $\geq 2$ reduces to the single open object {rank_two_object}, strong BSD to {rank_two_object, higher_euler_system}, never through parity. It wires the three detectors as an automatic AUDIT gate, runs a PROPOSE+FALSIFY mining pass over the curve invariants, and LOCALIZEs where a candidate breaks (curve $\times$ rank and curve $\times$ prime residual heat-maps with an automatic cliff diagnosis). It is a sound bookkeeper and falsifier, not a solver. See experiment (l).

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
| Experiments: Phase 0 infrastructure (EllipticCurve / L-function + detectors + smoke test) | Complete, smoke test 9/9 (check 7: exact off-center functional equation; check 8: 2-isogeny descent engine; check 9: p-adic engine) |
| Experiment (a): analytic rank from L-derivatives | Runnable |
| Experiment (b): weak BSD on rank 0-3 table | Runnable |
| Experiment (c): strong BSD quantities -> conjectural #Sha | Runnable |
| Experiment (d): Sato-Tate semicircle | Runnable, matches to chi-square ~0.014 |
| Experiment (e): Heegner machine across the rank boundary | Runnable; rational point out on 37a1, torsion on 389a1 and 5077a1 |
| Experiment (f): independent points + regulator from scratch | Runnable; all five open-regime regulators reproduced at index 1 |
| Experiment (g): twist parity scan | Runnable; 11 parity-blind analytic-rank-2 twists found |
| Experiment (h): numerical Gross-Zagier | Runnable; 4 (E, K) pairs to 24 digits, Heegner indices exactly integral |
| Experiment (i): strong BSD high precision | Runnable; #Sha = 1 to 27 digits on all five open-regime curves |
| Experiment (j): 2-isogeny descent | Runnable; rank E_34 = 2 proven, rank >= 2 curves carry no rational 2-isogeny |
| Experiment (k): p-adic L-function (Mazur-Tate-Teitelbaum) | Runnable; exceptional zero classified, L-invariant computed to 20 base-p digits, Greenberg-Stevens RHS assembled on 11a1 |
| Experiment (l): proof-search engine (atlas-as-graph + frontier + AUDIT) | Runnable; frontier of rank >= 2 BSD computes to {rank_two_object}, never via parity; detectors wired as an automatic gate; smoke still 9/9 |
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
python -m experiments.heegner_ceiling.e_e_heegner_ceiling
python -m experiments.independent_points.e_f_independent_points
python -m experiments.twist_parity.e_g_twist_parity
python -m experiments.gross_zagier_check.e_h_gross_zagier
python -m experiments.strong_bsd_hp.e_i_strong_bsd_hp
python -m experiments.two_descent.e_j_two_descent
python -m experiments.padic_lfunction.e_k_padic_lfunction

# Run the proof-search engine (frontier + AUDIT + mining)
python -m experiments.engine.e_l_engine
```
