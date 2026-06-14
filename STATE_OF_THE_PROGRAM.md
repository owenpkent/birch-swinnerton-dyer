# State of the proof program (repo-wide)

> A one-page strategic snapshot of the whole project: where every architecture stands, what each proves and where it stops, where the live work is, and the single most-leveraged next move. Companion to the operational [`PHASE_STATE.md`](PHASE_STATE.md) and the synthesis surface [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md). Last updated: 2026-06-13.

## The thesis in one paragraph

The program does not have a proof of BSD and is not close to one. What it has is a sharp map of where the proof is already complete and a precise specification of the one place it must reach. BSD is a THEOREM for analytic rank 0 and 1 (Gross-Zagier 1986 + Kolyvagin 1990), and finiteness of $\mathrm{Sha}$ is known exactly there and nowhere else. The dominant meta-finding is the **rank-boundary thesis**: every proven technique bottoms out at analytic rank 1 because its engine (a single Heegner point) is a rank-1 object. A proof of BSD in general must construct something genuinely new in the rank $\geq 2$ regime. That is a compass, not a verdict.

## The candidate architectures

| Architecture | What it is | Status | The wall (what we learned) |
|---|---|---|---|
| **1. Modularity** (Wiles; BCDT 2001) | every $E/\mathbb{Q}$ is modular, so $L(E,s)$ continues and has a functional equation; $w$ gives parity | **Complete as far as it goes** | Modularity delivers the analytic continuation and the root number, hence the analytic rank mod 2. It does NOT give the rank itself (Detector 1: parity-only). |
| **2. Heegner / Gross-Zagier + Kolyvagin** | a Heegner point has nonzero height iff $L'(E,1) \neq 0$; Kolyvagin's Euler system then bounds Sha | **PROVEN regime (rank 0, 1)** | The single proven route. Structurally capped at rank 1: one Heegner point is a rank-1 object, so it cannot exhibit two independent generators. This is the rank-boundary wall. |
| **3. Iwasawa theory / main conjectures** (Mazur; Kato; Skinner-Urban 2014) | $p$-adic $L$-functions and the main conjecture relate Selmer to $L_p$ | **LIVE** | Gives the $p$-part of strong BSD in many cases and the $p$-adic BSD (Mazur-Tate-Teitelbaum). The archimedean leading term and unconditional Sha-finiteness in rank $\geq 2$ remain open. |
| **4. Euler systems** (Kolyvagin, Kato) | bound $\mathrm{Sel}$ / $\mathrm{Sha}$ from a norm-compatible system of classes | **LIVE** | The most flexible bounding tool. The known systems (Heegner, Beilinson-Kato) are tied to rank $\leq 1$ or to the analytic side; a higher-rank Euler system is the missing object. |
| **5. Statistics / averages** (Bhargava-Shankar; Bhargava-Skinner-Zhang) | bounded average rank; a positive proportion of curves satisfy BSD | **PROVEN at the population level** | Proves BSD holds for a positive proportion of curves and that the average rank is bounded. It is a statement about the family, not about any single given $E$. |

Each entry is a coordinate: modularity gives parity, Heegner gives rank $\leq 1$, statistics gives a positive proportion. None reaches an arbitrary rank-$\geq 2$ curve, which is exactly where effort must concentrate.

## The live front: the rank $\geq 2$ object

The bet (mirroring how the function-field case is fully understood via Tate / Artin-Tate / Milne): the open part of BSD is the construction of rational points and the bounding of Sha in rank $\geq 2$. What is in hand vs missing:

**In hand:**
- Rank 0, 1 fully proven, including the leading-coefficient formula and finite Sha.
- The $p$-adic main conjecture (Skinner-Urban) and Kato's Euler system give the $p$-part of BSD in many rank $\leq 1$ cases.
- The function-field template: BSD over $\mathbb{F}_q(C)$ is a theorem under finite Sha, computed from etale cohomology of the elliptic surface. This is the "what a complete proof looks like" control.
- A computed, validated experimental substrate: analytic rank from $L$-derivatives matches the Mordell-Weil rank on the bundled curves, the strong-BSD formula solved for $\#\mathrm{Sha}$ lands at a perfect square, and Sato-Tate validates the $a_p$ pipeline.
- A proof-search ENGINE (experiment (l), [`experiments/engine/`](experiments/engine/)) that runs the whole discipline as a closed loop: the atlas as a typed proof graph (frontier of rank $\geq 2$ BSD computed to {rank_two_object}, never via parity), the three detectors as an automatic AUDIT gate, residual heat-maps that LOCALIZE where a candidate breaks, a PROPOSE battery scoring the candidate construction classes against the Direction-01 bar, and a VERIFY pass emitting Lean sorry-obligations. It proves nothing in rank $\geq 2$; it makes the boundary auditable and re-runnable.

**The one missing object:** a construction that produces $\geq 2$ independent rational points (a higher-rank analog of the Heegner point) OR an Euler system that bounds Sha unconditionally in rank $\geq 2$. Untouched at the construction level; multi-year, multi-person.

## The cross-cutting compass

- **Rank-boundary thesis**: every proven method is a rank-1 object. Build the rank-$\geq 2$ object.
- **Parity is not rank** (Detector 1): modularity and the parity conjecture give rank mod 2; a full proof needs the exact rank.
- **Sha-finiteness discipline** (Detector 2): finite Sha is proven only in rank $\leq 1$; any rank-$\geq 2$ strong-BSD claim must discharge it, not assume it.
- **Function-field mirage** (Detector 3): a method that works verbatim over $\mathbb{F}_q(C)$ has imported the geometric Frobenius the number-field case lacks.

## Lean substrate

Skeleton (documented `sorry`). Mathlib has `EllipticCurve` and `WeierstrassCurve`; it does not yet have canonical heights, the Mordell-Weil theorem in usable form, the Hasse-Weil $L$-function, or BSD. The skeleton states the rank equality, the root-number/parity statement, and BSD as the goal, and notes where Mathlib already has relevant API. See [`lean/README.md`](lean/README.md).

## The single most-leveraged next move

The rank-2 object is now specified ([Direction 01](docs/03_research/research_directions/01_rank_two_object.md)) and the discipline runs as the engine of experiment (l). The engine's PROPOSE battery leaves exactly one construction class lit as the live candidate: the **Kudla program / arithmetic theta series**, the only formalism with the Clause-2 second-derivative shape (codimension-$r$ arithmetic cycles against genus-$r$ Eisenstein series). This front is now specified ([Direction 04](docs/03_research/research_directions/04_kudla_clause_two_bridge.md)) with its computable rank-1 shadow built and running (experiment (m): Waldspurger's proportionality on the congruent-number family, $\kappa$ constant to $\sim 30$ digits). The most-leveraged next move is to attack its two named bridges over $\mathbb{Q}$: from an Eisenstein / orthogonal $L$-value to $L(E, s)$, and from a cycle class to a rational point. Yun-Zhang prove the all-orders shape over function fields, so the wall is localized to exactly the two imports a number-field version must replace (the $r$ moving legs over $X^r$, the Frobenius twist in the shtuka). Anything claimed here runs through Detector 3 first: the higher-derivative layer is a function-field theorem, so a transfer to $\mathbb{Q}$ must not silently import the surface.

Honest odds: an unconditional BSD proof in rank $\geq 2$ is a generational result; this repo's value is the sharp map of the boundary, the validated substrate, and now an auditable engine for testing candidate constructions against the three detectors.

## Canonical pointers

- Operational state: [`PHASE_STATE.md`](PHASE_STATE.md)
- Cross-architecture findings: [`experiments/LEARNINGS.md`](experiments/LEARNINGS.md)
- Test plan: [`experiments/PLAN.md`](experiments/PLAN.md)
- Master research map: [`docs/research_atlas/README.md`](docs/research_atlas/README.md)
- Research directions: [`docs/03_research/research_directions/`](docs/03_research/research_directions/)
- Lean substrate: [`lean/README.md`](lean/README.md)
