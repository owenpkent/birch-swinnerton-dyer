# CLAUDE.md

Project-specific instructions for Claude Code. Read on every session start. This file carries both the project's technical context (architectures, conventions, the EllipticCurve / L-function interface) and the human-side context (owner, tech stack, agent infrastructure).

## What this repo is

A research-and-study project on the Birch and Swinnerton-Dyer Conjecture (BSD). It contains:
- Layered docs (intuitive, undergraduate, graduate, research) on elliptic curves, their $L$-functions, and BSD.
- A strategic landscape document ([`docs/research_atlas/`](docs/research_atlas/)) cataloging every known approach with its obstructions.
- A computational experimental thread ([`experiments/`](experiments/)) organized around testing the candidate BSD proof architectures.
- A Lean 4 / Mathlib formalization skeleton ([`lean/`](lean/)) wired to Mathlib's `EllipticCurve` / `WeierstrassCurve`.

It is **not** a tool or product. It is a research codebase. Output is markdown documents, numerical experiments, visualizations, and Lean proofs.

## Stance (read this before writing any framing)

The posture of this project is that we are trying to solve BSD. It is hard and the odds are long, but it is a target, not a monument, and nothing here should be written as if the problem were impossible.

When you document a negative result, frame it as progress. BSD is proven only for analytic rank 0 and 1 (Gross-Zagier + Kolyvagin), and finiteness of $\mathrm{Sha}$ is known only there. That is not a verdict; it is a coordinate. It says the entire difficulty is concentrated in the **rank $\geq 2$ structure**, because the Heegner-point machine that powers the proven regime produces one point and so structurally cannot reach rank 2. Spend effort where the proof must live.

Avoid fatalistic phrasing. Prefer the directional reading: the rank-1 ceiling is a compass pointing at the rank $\geq 2$ object that a proof must construct. Keep the math exactly as rigorous as it is (a method that only gives parity still only gives parity; an open finiteness is still open). Change the tone, not the theorems.

## About the owner

The owner is Owen, a wheelchair user with muscular dystrophy.

- **Typing is hard.** Be proactive. Make decisions. Don't ask for confirmation on small things.
- **Offer A/B/C choices** when input is needed. One letter is faster than a sentence.
- **PowerShell on Windows.** Use PowerShell syntax. Prefer single-line commands.
- **Accessibility matters.** Many of Owen's projects are tools he actually uses.

## START HERE

- **Mindset and philosophy**: [`docs/researcher_mindset.md`](docs/researcher_mindset.md). The problem is a target not a monument; we advance a front; negative results are coordinates; honesty is the engine.
- **Research strategy**: [`docs/research_atlas/README.md`](docs/research_atlas/README.md). Catalog of all approaches, what is proven, what is open.
- **Experiments**: [`experiments/PLAN.md`](experiments/PLAN.md). The test plan with current status per architecture.
- **Operational state**: [`PHASE_STATE.md`](PHASE_STATE.md), [`OPERATIONS.md`](OPERATIONS.md), [`STATE_OF_THE_PROGRAM.md`](STATE_OF_THE_PROGRAM.md).

## Core conceptual framework

The project is organized around the candidate **proof architectures** for BSD (see [`docs/solutions/README.md`](docs/solutions/README.md)):

1. **Modularity** (Wiles; Taylor-Wiles; Breuil-Conrad-Diamond-Taylor 2001): every $E/\mathbb{Q}$ is modular, so $L(E, s)$ has analytic continuation and a functional equation, and the root number $w$ gives the parity of the analytic rank.
2. **Heegner points and Gross-Zagier + Kolyvagin**: for analytic rank 0 and 1, the rank equality and finiteness of $\mathrm{Sha}$ are PROVEN. This is the only fully proven regime.
3. **Iwasawa theory / main conjectures** (Mazur; Kato; Skinner-Urban 2014; Mazur-Tate-Teitelbaum $p$-adic BSD): $p$-adic $L$-functions and Euler systems bounding Selmer / Sha.
4. **Euler systems** (Kolyvagin, Kato): bound the Selmer and Tate-Shafarevich groups.
5. **Statistics / averages** (Bhargava-Shankar bounded average rank; Bhargava-Skinner-Zhang positive proportion satisfying BSD; Goldfeld's minimalist conjecture, density 1/2 each for rank 0 and 1).

The **four-level framing** (see [`docs/02_graduate/`](docs/02_graduate/)) places BSD's hard content at the level of constructing rational points / bounding Sha in rank $\geq 2$, not at the level of parity (which modularity already delivers).

## The wrong-approach discipline

Three detectors in [`experiments/_shared/controls.py`](experiments/_shared/controls.py), the BSD analog of the Riemann repo's Davenport-Heilbronn discipline:

1. **Parity-only**: the root number gives rank mod 2; the parity conjecture gives Mordell-Weil rank mod 2. A method that recovers only parity cannot prove the full rank equality.
2. **Sha-finiteness assumed**: $\#\mathrm{Sha}$ finite is a theorem only for analytic rank $\leq 1$. A method that uses it in the open regime must flag the assumption.
3. **Function-field mirage**: BSD over $\mathbb{F}_q(C)$ is a theorem under finite Sha (Tate; Artin-Tate; Milne). A method that "works" verbatim over a function field has imported the geometric Frobenius the number-field case lacks.

Plus the **control pair**: rank $\leq 1$ (proven) vs rank $\geq 2$ (open). A method must do something genuinely new in the open regime.

Run `python -m experiments._shared.smoke_test` (11/11) to verify the substrate and detectors. Check 7 is the exact off-center functional equation, the test that catches a single wrong bad-prime $a_p$ (it found nine in the original bundled table). Check 8 guards the 2-isogeny descent engine of experiment (j) (Selmer orders are 2-powers; bundled rank-0 2-torsion curves give upper bound = rank; the rank $\geq 2$ curves carry no rational 2-isogeny). Check 9 guards the p-adic engine of experiment (k) (j-series self-check $c_0=744$, $c_1=196884$; $\operatorname{ord}_p(q) = v_p(\Delta)$ on split-multiplicative curves; the Iwasawa log round-trips under exp; the exceptional zero is classified correctly). Check 10 guards the theta-shadow engine of experiment (m), the codim-1 Kudla shadow (Tunnell $c_3=-4$ by from-scratch lattice counting; the Waldspurger constant $\kappa = \Omega_{E_1}/32$ matches the CM closed form $2\pi/\mathrm{AGM}(1,\sqrt2)/32$; the rank-2 / codim-2 Clause-2 object stays OPEN). Check 11 guards the p-adic height regulator engine of experiment (n) (the formal group, Mazur-Tate $p$-adic $\sigma$, and formal-group reduction; quadraticity and bilinearity of $h_p$; the $c$-independent valuation $v_5(\mathrm{Reg}_5(389a1)) = v_7(\mathrm{Reg}_7) = 2$ matching the canonical Mazur-Stein-Tate example; the unit digits gated behind the named missing constant $c$).

## Tech stack

- **Language**: Python (primary). Lean 4 (formal verification).
- **Python libraries**: `mpmath` (high-precision arithmetic for the AFE), `numpy`, `scipy`, `sympy`, `matplotlib`. `manim` for visualizations.
- **Formal verification**: Lean 4 + Mathlib (`lean/`, requires `elan` to build). Mathlib has `EllipticCurve` and `WeierstrassCurve`.
- **Docs**: Markdown with LaTeX math (`$...$` inline, `$$...$$` block in files; plain Unicode in chat).

## Conventions

- **High-precision arithmetic**: `mpmath` at $\geq 25$ digits for $L$-values and derivatives. The smoothed approximate functional equation (incomplete-Gamma test function) is the standard tool for evaluating $L(E, s)$ at the center $s = 1$.
- **a_p from point counting**: $a_p = p + 1 - \#E(\mathbb{F}_p)$ at good primes by honest enumeration; bad-prime $a_p \in \{-1, 0, 1\}$ supplied from the bundled data.
- **Bundled curve data**: a small table of curves by Cremona label with public LMFDB/Cremona invariants ([`experiments/_shared/curve_data.py`](experiments/_shared/curve_data.py)), so everything runs offline. Attribution is in the file header.
- **EllipticCurve interface**: every experiment manipulates an `EllipticCurve` exposing `a_p`, `a_n`, `L_value`, `L_derivative_at_one`, `analytic_rank`. Used uniformly so the same code runs on every curve.

## Style

- **No em dashes** anywhere (global preference). Use periods, colons, parentheses, or hyphens. Do not use en dashes as a workaround. Rewrite the sentence instead.
- Inline math in markdown uses `$...$`, display uses `$$...$$`.
- In chat output use Unicode and plain text for math.
- Code: explanatory module-level docstrings, minimal inline comments. Comments explain WHY, not WHAT.

## Running things

```powershell
python -m experiments._shared.smoke_test
python -m experiments.l_function_rank.e_a_analytic_rank
python -m experiments.weak_bsd_table.e_b_weak_bsd
python -m experiments.strong_bsd_quantities.e_c_strong_bsd
python -m experiments.sato_tate.e_d_sato_tate
python -m experiments.two_descent.e_j_two_descent

# Build the Lean skeleton (requires elan + lake)
cd lean; lake build
```

Working dir is the repo root. Scripts use `from experiments._shared import ...`, which resolves only from the root.

## Git commits

```powershell
git add -A; git commit -m "docs: add intuitive explanation"
```

Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`. Never commit or push without per-action authorization.

## Agent infrastructure

Six agent roles in [`.claude/agents/`](.claude/agents/): SURVEYOR (literature + scorecards), BUILDER (constructions), VERIFIER (Lean 4), ADVERSARY (the three detectors + counterexample search), SYNTHESIZER (integrate into the dossier), ORCHESTRATOR (schedule, budget, abandonment). See [`OPERATIONS.md`](OPERATIONS.md).

## Known landmarks

- BSD is PROVEN only for analytic rank 0 and 1 (Gross-Zagier 1986 + Kolyvagin 1990); finiteness of $\mathrm{Sha}$ is known only there.
- The smallest rank-1 curve is **37a1** ($y^2 + y = x^3 - x$); the smallest rank-2 is **389a1**; the smallest rank-3 is **5077a1**.
- The root number $w = (-1)^{\text{analytic rank}}$: $w = +1$ for even analytic rank, $w = -1$ for odd.
- Bhargava-Shankar: the average rank of elliptic curves over $\mathbb{Q}$ is bounded (below 1); a positive proportion have rank 0 and a positive proportion rank 1, and a positive proportion satisfy BSD (Bhargava-Skinner-Zhang).
- Goldfeld's minimalist conjecture: density 1/2 each for rank 0 and rank 1.

## When in doubt

- The atlas ([`docs/research_atlas/README.md`](docs/research_atlas/README.md)) is the master reference for what is proven and what is open.
- The plan ([`experiments/PLAN.md`](experiments/PLAN.md)) is the master reference for the experimental thread.
- The three detectors are the project's structural sanity checks.
- If a proposed method only gives the parity of the rank, it is modularity-level and not BSD-closing.

## Constellation

This repo is tracked by Constellation. It has `README.md` with `## Status` and `TODO.md` with checkboxes.
