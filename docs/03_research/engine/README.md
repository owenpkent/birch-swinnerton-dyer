# The BSD proof-search engine: design doc

> The formal spec for a sound proof-search loop over the BSD landscape. Not a solver. A bookkeeper plus a falsifier plus a soundness oracle, wired into one closed loop with shared state. It turns "BSD is open" into a monotonically shrinking, regime-tagged set of explicit open lemmas.

## 1. The honest reframe

A guaranteed BSD solver cannot exist. BSD in analytic rank $\geq 2$ is open, the rank-$\geq 2$ construction is the [one missing object](../../research_atlas/README.md#the-one-missing-object), and no scaffolding conjures it. So the engine is not a solver. It is a **sound proof-search loop**: CEGIS (counterexample-guided inductive synthesis) pointed at mathematics rather than programs.

The loop is the classic three beats:

$$\textbf{propose} \;\longrightarrow\; \textbf{falsify} \;\longrightarrow\; \textbf{refine},$$

with two oracles that make it sound rather than merely suggestive:

- **The soundness oracle** is the three detectors in [`controls.py`](../../../experiments/_shared/controls.py): parity-only, Sha-finiteness-assumed, function-field mirage. Every proposed reduction is audited before it can enter the proof graph. A reduction that launders parity into full rank, or quietly assumes $\#\mathrm{Sha} < \infty$ in the open regime, or imports a geometric Frobenius, is rejected at the gate.
- **The counterexample oracle** is the bundled curve database (ranks 0 to 3, with the control pair $37a1$ vs $389a1$). A numerical claim that fails at $\geq 25$ digits on any curve in the database is killed before any theory is spent on it.

The payoff is precise. The engine never outputs "BSD is proven." It outputs, for a fixed regime $R$ (rank $0$, rank $1$, or rank $\geq 2$):

> In regime $R$, BSD reduces to **this** explicit minimal set of open lemmas $\{L_1, \dots, L_k\}$, each detector-clean, each falsified-against-the-database-and-survived.

and that set shrinks monotonically as reductions are admitted. The honest win is **soundness plus perfect bookkeeping plus fast falsification**, not a proof.

## 2. The state: a typed proof graph

The shared state is a typed directed graph $G = (V, E)$, the [atlas](../../research_atlas/README.md) promoted from prose to data.

**Nodes** $v \in V$ are statements. Each carries:

- **regime**: one of `rank0`, `rank1`, `rank_ge2`, or `all` (regime-neutral, e.g. the descent exact sequence).
- **status**: `proven`, `conditional`, `open`, or `refuted`.
- **provenance**: the source (a reading note in [`reading_notes/`](../reading_notes/)) or the experiment that measured it, plus the exact theorem/conjecture label.
- **depends_on**: for a `conditional` node, the keys it leans on (the strong-BSD nodes depend on the Iwasawa main conjecture). A planned `arch` tag (`archimedean` vs `p-adic`, recording which side the leading term lives on) is future work, not in v0.

**Edges** $u \to v$ are **reductions**: "if $u$ then $v$ (in this regime, under these side conditions)." Every edge carries a **detector audit** (the three-bit verdict from section 3's AUDIT). An edge is admissible only if its audit is clean for the regime it claims. The reduction's side conditions (e.g. "uses $\#\mathrm{Sha}<\infty$", "needs a base curve") are recorded on the edge, not hidden.

**The frontier** is computed, not asserted: for a target node $T$ (say strong BSD in `rankGE2`), the frontier is a **minimal set of open nodes** whose collective proof discharges $T$ through admissible edges. See FRONTIER in section 3.

### The modelling rule that makes the parity wall structural

Parity is its **own node**, separate from rank. Concretely:

- `parity` (regime `all`, status `proven`): the root number gives analytic rank mod $2$; the parity conjecture gives Mordell-Weil rank mod $2$.
- `rankEquality` (per regime): the full $\operatorname{ord}_{s=1} L = \operatorname{rank} E(\mathbb{Q})$.

**There is no edge `parity` $\to$ `rankEquality`.** This is not an oversight, it is the encoding of Detector 1. Parity fixes rank mod $2$ and cannot separate rank $0$ from $2$ or rank $1$ from $3$. By refusing to draw that edge, the graph makes the parity wall a structural property of the data: any path the engine reports as discharging full rank cannot route through the parity node. Experiment [(g)](../../../experiments/twist_parity/) supplies the live witness (11 twists with $w = +1$ yet analytic rank $2$).

## 3. The six operators

The engine is six operators over the graph. Each is a pure function of the shared state plus the curve database, so they compose into the loop without hidden coupling.

### 3.1 FRONTIER: compute minimal open sets, rank by leverage

Given a target $T$, FRONTIER walks admissible edges backward and returns the **minimal open lemma-sets** that discharge $T$: the antichains of `open` nodes that form a cut between $T$ and the proven base. When several cuts exist, it ranks them by **leverage**: how many distinct targets a node sits on, how many edges it would unlock, and how close it is to an existing partial result. For BSD this is expected to compute, not assume, that the rank-$\geq 2$ minimal set is essentially the singleton [one missing object](../../research_atlas/README.md#the-one-missing-object): the rank-$\geq 2$ point construction (Direction 01) or the rank-$\geq 2$ Sha bound (Direction 02). FRONTIER is the atlas's "where the proof must live" made mechanical.

### 3.2 PROPOSE: reduction proposals and data-mined conjectures

PROPOSE generates new candidate edges and nodes. Two modes:

- **Reduction proposals.** A candidate edge $u \to v$ with a regime tag and side conditions, sourced from a surveyed result or a human construction. This is the BUILDER's lane; the creative rank-$\geq 2$ construction enters here (and only here).
- **Data-mined numerical conjectures.** Over the curve database, mine relations among invariants ($\Omega_E$, $\operatorname{Reg}_E$, $\prod c_p$, $\#\mathrm{tors}$, $\#\mathrm{Sha}$, $L^{(r)}(E,1)/r!$, $a_p$ statistics). This is the Ramanujan-Machine / Graffiti move pointed at BSD: propose an identity or inequality that holds across the database, hand it to FALSIFY immediately. A mined relation is a **conjecture node**, never a theorem; it earns an edge only after AUDIT and FALSIFY, and even then it is `conditional` until VERIFY.

PROPOSE is where the engine is honest about its limits: it scaffolds proposals and tests them, it does not invent the missing construction (section 6).

### 3.3 AUDIT: run the three detectors before spending compute

AUDIT is [`controls.py`](../../../experiments/_shared/controls.py) promoted from a manual checklist to an automatic gate. Before any proposed edge is admitted, and before FALSIFY spends precision on it, AUDIT runs:

1. **`parity_detector`**: does the proposal claim full rank from only the root number $w$? If so, reject (or down-rank to a parity-only node with no edge to `rankEquality`).
2. **`sha_finiteness_flag`**: does it use $\#\mathrm{Sha} < \infty$? If the regime is rank $\geq 2$, this is open, so the edge is stamped `conditional` with the assumption recorded, never silently `proven`.
3. **`function_field_mirage`**: does it need a base curve or a geometric Frobenius? If so, flag the import; an edge that survives only over $\mathbb{F}_q(C)$ cannot certify a number-field target.

AUDIT is cheap and runs first, so the expensive operators never burn cycles on a proposal that was unsound on its face.

### 3.4 FALSIFY: test at $\geq 25$ digits across the whole database

FALSIFY is the adversary. It evaluates the proposal numerically on every curve in the database at $\geq 25$ digits (the smoothed AFE substrate), looking for a single violation. Its sharpest instruments:

- **The rank-1 $\to$ rank-2 cliff.** Run the proposal on the proven regime, then push it across the boundary. The Heegner machine [(e)](../../../experiments/heegner_ceiling/) outputs a non-torsion point on $37a1$ and exactly the zero point on $389a1$; any proposal claiming to cross the cliff must not silently degenerate there.
- **The control pair $37a1$ vs $389a1$** ([`control_pair`](../../../experiments/_shared/controls.py)). A proposal must do something genuinely new on $389a1$, not merely reproduce the rank-$\leq 1$ behavior.
- **The Direction-01 operational bar** ([Direction 01](../research_directions/01_rank_two_object.md)). For a rank-$\geq 2$ point construction, FALSIFY demands two measured facts: (i) **non-torsion output on $389a1$**, where the Heegner machine in [(e)](../../../experiments/heegner_ceiling/) provably and measurably returns zero ($|z| < 10^{-10} \bmod \Lambda$); and (ii) output whose **size does not factor through $L'(E/K,1)$**, since experiment [(h)](../../../experiments/gross_zagier_check/) showed that one first derivative is the old machine's entire output and is $0$ on rank-$\geq 2$ input. A proposal whose magnitude is any multiple of $L'(E/K,1)$ is the rank-1 machine in disguise (the Gross-Kohnen-Zagier pattern) and FALSIFY kills it.

Numerical survival is **evidence**, never proof: a relation that holds to $10^{-27}$ on every rank-$\geq 2$ curve is a strong candidate edge, not a theorem. That label is enforced by status (`conditional` until VERIFY).

### 3.5 LOCALIZE: measure where a candidate breaks

When FALSIFY finds a violation, LOCALIZE measures **where**: it builds a curve $\times$ prime $\times$ rank heat-map of the residual, so a near-miss becomes a diagnosis rather than a binary fail. A proposal that holds in rank $0,1$ and breaks exactly at rank $2$ has localized the wall (and probably tripped Detector 1). A proposal that breaks at a specific bad prime has localized a missing local condition. LOCALIZE turns the experiments [(a)-(k)](../../../experiments/PLAN.md) from fixed scripts into a parametrized residual map, and it feeds the next PROPOSE: the heat-map says which side condition to add.

### 3.6 VERIFY: turn a survivor into a Lean statement

A proposal that passes AUDIT, survives FALSIFY across the database, and LOCALIZEs cleanly is promoted to a **Lean statement** against Mathlib's `EllipticCurve` / `WeierstrassCurve` API, in the [`lean/BSD/`](../../../lean/BSD/) skeleton. The rank-$\geq 2$ target already exists as a `sorry`: `rankTwoCertificate` in [`RankEquality.lean`](../../../lean/BSD/RankEquality.lean) (two points, nonzero height-pairing determinant). VERIFY's output is a typed obligation, not a closed proof: it states the lemma precisely and connects it to the API, so the open frontier becomes a concrete `sorry` target the VERIFIER can attack. Only a discharged Lean obligation moves a node from `conditional` to `proven`.

## 4. Why this is this repo's engine

The engine invents no new machinery. It is the closed loop with shared state laid over pieces that already exist, scattered, in the repo.

| Operator | Existing repo piece | Agent role |
|---|---|---|
| AUDIT | [`controls.py`](../../../experiments/_shared/controls.py) detectors, promoted from manual to automatic gate | ADVERSARY |
| graph (state) | the [atlas](../../research_atlas/README.md) and scorecard, promoted from prose to data | SURVEYOR / SYNTHESIZER |
| FRONTIER | the ["one missing object"](../../research_atlas/README.md#the-one-missing-object), computed instead of asserted | SURVEYOR / SYNTHESIZER |
| PROPOSE | new: data-mining over the curve table + reduction proposals | BUILDER |
| FALSIFY | experiments [(a)-(k)](../../../experiments/PLAN.md) generalized to a database sweep at $\geq 25$ digits | the experimental substrate |
| LOCALIZE | experiments [(a)-(k)](../../../experiments/PLAN.md) generalized to a curve/prime/rank heat-map | the experimental substrate |
| VERIFY | the [`lean/BSD/`](../../../lean/BSD/) skeleton vs Mathlib's `EllipticCurve` API | VERIFIER |
| the loop | new: scheduling, budget, abandonment across the six | ORCHESTRATOR |

The six [agent roles](../../../CLAUDE.md) were already the six operators waiting for a shared object to act on. The **new thing** is exactly that object: the closed loop with one typed proof graph as shared state, so PROPOSE feeds AUDIT feeds FALSIFY feeds LOCALIZE feeds VERIFY feeds the graph feeds FRONTIER feeds PROPOSE, monotonically.

## 5. The v0 build

What ships now (`experiments/engine/`):

| File | Role |
|---|---|
| `graph.py` | the typed proof graph: node/edge dataclasses (regime, arch, status, provenance, detector audit), admissibility check, the parity-is-its-own-node invariant |
| `atlas_graph.py` | the atlas and scorecard encoded as graph data: the proven base, the architectures and their walls, the no-edge `parity` $\to$ `rankEquality` rule |
| `frontier.py` | FRONTIER: backward cut search, minimal open lemma-sets, leverage ranking |
| `audit.py` | AUDIT: the three detectors from [`controls.py`](../../../experiments/_shared/controls.py) wired as an automatic edge gate |
| `mine.py` | PROPOSE (data-mining mode): relation search over curve invariants, emits conjecture nodes for FALSIFY |
| `localize.py` | FALSIFY/LOCALIZE: residual heat-maps (curve $\times$ rank, curve $\times$ prime) with an automatic break-rank diagnosis (cliff vs proven-regime break vs survivor) |
| `propose.py` | PROPOSE: candidate rank $\geq 2$ construction classes run through the Direction-01 battery (T1 nondegeneracy, T2 second-order tie) plus the detectors |
| `verify.py` | VERIFY: emits a Lean obligation (a `sorry` statement) per open frontier node against the skeleton API, written to [`lean/BSD/EngineObligations.lean`](../../../lean/BSD/EngineObligations.lean) |
| `e_l_engine.py` | the driver: runs all six operators over the bundled database, prints the current minimal open set per regime |

Run it offline as a module, consistent with the rest of the thread:

```powershell
python -m experiments.engine.e_l_engine
```

Future work (named, not shipped):

- **Live PROPOSE of a new construction.** v0 mines numerical relations and runs the candidate construction CLASSES through the Direction-01 battery (T1/T2 plus the detectors), reproducing which are first-derivative-bottlenecked, retired (GKZ), or the live Clause-2 candidate. What it does not do is GENERATE a genuinely new rank-$\geq 2$ construction; that is the BUILDER's open creative core (section 6).
- **Lean PROMOTE.** v0's VERIFY emits a Lean statement; closing the `sorry` (the actual proof) is the VERIFIER's manual work, not automated.
- **Adaptive LOCALIZE.** v0 produces the heat-map; using it to auto-suggest the next side condition is future work.

## 6. Honest scope and limits

The creative core of PROPOSE, the **actual rank-$\geq 2$ construction**, is the open problem. The engine does not conjure it. It scaffolds and tests it: it holds the bookkeeping perfectly, it audits every proposal for the three failure modes before any compute is spent, and it falsifies fast and broadly so a dead proposal dies in seconds rather than in a paper.

Three guardrails keep the engine honest:

1. **No upgrade without VERIFY.** Numerical survival is `conditional` at best. Nothing reaches `proven` without a discharged Lean obligation.
2. **Regime is mandatory.** Every node and edge carries its regime. "Proven in rank $\leq 1$" never silently becomes "proven."
3. **The parity wall is in the data.** No edge `parity` $\to$ `rankEquality`, ever. A reported discharge of full rank cannot launder parity.

The win is **soundness plus perfect bookkeeping plus fast falsification**: BSD stays open, but at every moment the engine can state, per regime, the exact minimal set of detector-clean, database-survived open lemmas it has been reduced to, and that set only shrinks. See the [atlas](../../research_atlas/README.md), [`controls.py`](../../../experiments/_shared/controls.py), the [experiment plan](../../../experiments/PLAN.md), and [Direction 01](../research_directions/01_rank_two_object.md).
