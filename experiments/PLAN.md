# Experiment plan

> The computational thread. Every experiment runs on the shared `EllipticCurve` / Hasse-Weil $L$-function interface and is scored against the three wrong-approach detectors. Cross-cutting findings live in [`LEARNINGS.md`](LEARNINGS.md).

## Methodology

- **One shared substrate.** All experiments import from [`_shared/`](_shared/): the `EllipticCurve` class (point-count $a_p$, multiplicative $a_n$, the smoothed approximate functional equation for $L(E, s)$ and its derivatives at $s = 1$, the root number), the bundled curve table (ranks 0 to 3, public LMFDB/Cremona invariants), and the three detectors plus the control pair.
- **High precision.** `mpmath` at $\geq 25$ digits for analytic work. The smoothed AFE (incomplete-Gamma test function) is the standard tool for evaluating $L(E, s)$ at the center.
- **Offline.** All curve data is bundled with attribution, so the thread runs without network access.
- **Honesty.** Each experiment prints its regime (proven vs open) and invokes the relevant detector. Numerical agreement in rank $\geq 2$ is labeled evidence, never proof.

## The experiments

| # | Folder | Question | Status |
|---|---|---|---|
| (a) | [`l_function_rank/`](l_function_rank/) | analytic rank from $L^{(k)}(E, 1)$ | RUNNABLE; matches MW rank on bundled curves |
| (b) | [`weak_bsd_table/`](weak_bsd_table/) | weak BSD: analytic rank $=$ MW rank on a rank 0-3 table | RUNNABLE; 15/15 match |
| (c) | [`strong_bsd_quantities/`](strong_bsd_quantities/) | strong BSD: $\Omega, \operatorname{Reg}, \prod c_p, \#\text{tors} \Rightarrow$ conjectural $\#\operatorname{Sha}$ | RUNNABLE; $\#\operatorname{Sha}$ lands at a perfect square |
| (d) | [`sato_tate/`](sato_tate/) | Sato-Tate semicircle as an $a_p$ pipeline check | RUNNABLE; chi-square-like deviation $\approx 0.014$ |
| (e) | [`heegner_ceiling/`](heegner_ceiling/) | run the Heegner machine across the rank boundary: point out on 37a1, what on 389a1 / 5077a1? | RUNNABLE; non-torsion point recovered on 37a1, torsion on 389a1 AND on 5077a1 (same parity as 37a1): the ceiling is the one-point structure, not the sign |
| (f) | [`independent_points/`](independent_points/) | construct the easy half of the rank $\geq 2$ object: $r$ independent points + regulator from scratch | RUNNABLE; generators found on all five open-regime curves, Gram determinant reproduces the LMFDB regulator at index 1 |
| (g) | [`twist_parity/`](twist_parity/) | where exactly does parity go blind in a twist family? | RUNNABLE; 11 twists of 11a1/37a1 with $w = +1$ but $L(E_d, 1) = 0$ (analytic rank 2, invisible to the root number) |
| (h) | [`gross_zagier_check/`](gross_zagier_check/) | verify Gross-Zagier numerically: $L'(E,1) L(E_D,1) = \mathrm{Vol}(\Lambda)\hat{h}(P)/\sqrt{\|D\|}$ | RUNNABLE; 4 (E, K) pairs at $10^{-25}$, Heegner indices exactly integral (6, 1, 7, 5) |
| (i) | [`strong_bsd_hp/`](strong_bsd_hp/) | strong BSD at working precision in the open regime: $\sigma$-function regulators + Cauchy-integral leading coefficients | RUNNABLE; $\#\operatorname{Sha} = 1$ to within $5 \times 10^{-28}$ on all five rank $\geq 2$ curves; first run caught a wrong bundled regulator (5077a1) |
| (j) | [`two_descent/`](two_descent/) | the rigorous upper bound (f) leaves open: 2-isogeny descent, number-field-free | RUNNABLE; $\mathrm{rank}\,E_{34} = 2$ PROVEN with no BSD input; the (f) curves shown to carry no rational 2-isogeny (wall named) |
| (k) | [`padic_lfunction/`](padic_lfunction/) | the $p$-adic L-function thread (architecture 3): the exceptional zero and the Mazur-Tate-Teitelbaum $\mathcal{L}$-invariant | RUNNABLE; $\mathcal{L}_p(E) = \log_p(q)/\operatorname{ord}_p(q)$ computed to 20 base-$p$ digits, $\operatorname{ord}_p(q) = v_p(\Delta)$ verified, exceptional zero classified (split $a_N=+1$) across the bundled curves, Greenberg-Stevens RHS assembled on 11a1 |
| (l) | [`engine/`](engine/) | the proof-search engine (meta-layer, not a numerical probe): atlas as a typed proof graph, the frontier of the open object computed, the three detectors as an AUDIT gate, a PROPOSE+FALSIFY mining pass, a LOCALIZE pass (curve $\times$ rank / curve $\times$ prime residual heat-maps + break-rank diagnosis), a PROPOSE construction battery (candidate classes vs the Direction-01 T1/T2 bar), and a VERIFY pass (emits Lean sorry-obligations from the frontier) | RUNNABLE; frontier of weak BSD rank $\geq 2$ $=$ {rank_two_object}, strong $=$ {rank_two_object, higher_euler_system}, never via parity; 4 methods audited; mining: R4 a cliff casualty, R2 a clean survivor; LOCALIZE diagnoses the regulator-cliff candidate as breaking exactly at rank 2 and isolates bad primes; PROPOSE finds the only T1-passer is non-constructive search and Kudla the live Clause-2 candidate; VERIFY emits 3 Lean sorry-obligations (rank_two_object corresponds to rankTwoCertificate), proven: 0; adversary-cleared for overclaiming; offline $\approx 0.3$s |
| (m) | [`theta_shadow/`](theta_shadow/) | the codim-1 Kudla shadow (Direction 04): Waldspurger's proportionality on the congruent-number family, the rank-1 generating series made a measured equation | RUNNABLE; $L(E_n,1) = \kappa\, c_n^2/\sqrt n$ with $\kappa = \Omega_{E_1}/32$ constant to $\sim 30$ digits (Tunnell coefficients from scratch by lattice counting; $\kappa$ cross-checked against $2\pi/\mathrm{AGM}(1,\sqrt2)/32$); congruent panel $c_n=0 \iff L=0$ with the $n=41$ BSD-conditional caveat; smoke check 10; rank-2 / codim-2 Clause-2 object stays OPEN |
| (n) | [`padic_regulator/`](padic_regulator/) | the p-adic height regulator of 389a1 (Direction 05): the rank-2 object experiment (k) named missing, witnessing that the Clause-2 second-order quantity is computable p-adically where the archimedean leg reads $0 = 0$ | RUNNABLE; from-scratch Mazur-Stein-Tate pipeline (formal group, Mazur-Tate $\sigma$, formal-group reduction, $h_p$, 2x2 Gram) with quadraticity / bilinearity self-checks; $v_5(\mathrm{Reg}_5) = v_7(\mathrm{Reg}_7) = 2$ ($c$-independent, matching the canonical example, so $\mathrm{Reg}_p \neq 0$ observed); unit digits gated behind the named missing constant $c$ (Kedlaya / overconvergent symbols); points are INPUT so Bridge 2 stays open; smoke check 11 |

## Detector coverage

- **Detector 1 (parity-only):** invoked in (a) and (b); EXHIBITED in (g) (a family where $w$ misclassifies every rank-2 twist) and in (e) (37a1 and 5077a1 share $w = -1$, yet the machine outputs a point on one and torsion on the other, so the ceiling is not parity).
- **Detector 2 (Sha-finiteness):** invoked in (b) and (c). Flagged OPEN for every rank $\geq 2$ curve. (f) makes the asymmetry concrete: the lower bound rank $\geq r$ is constructed; the upper bound is exactly the missing Selmer/Sha input. (j) exhibits the detector rather than assuming it: where the upper bound IS computable (a rational 2-isogeny exists) descent still bounds only $\mathrm{Sha}[2]$, and on $E_{17}$ that slice is nonzero, so the rank is not pinned.
- **Detector 3 (function-field mirage):** documented in [`_shared/controls.py`](_shared/controls.py); none of the experiments imports a geometric Frobenius. (f) names the gap: over $\mathbb{F}_q(C)$ the upper bound comes from $H^2$ of the elliptic surface; over $\mathbb{Q}$ nothing here supplies it. (j) makes it per-curve: the rank $\geq 2$ targets carry no rational 2-isogeny, so the general descent there needs the class group and units of a cubic field, the object $\mathbb{Q}$ does not hand over. (k) passes it cleanly: the $p$-adic thread uses the cyclotomic $\mathbb{Z}_p$-extension and weight deformations, no surface and no geometric Frobenius.
- **Architecture 3 (Iwasawa), Detector 2 (Sha):** invoked in (k). The exceptional zero and the $\mathcal{L}$-invariant are exact $p$-adic data (Detector 1 passed: finer than parity), but the bridge $L_p \to \#\mathrm{Sha}[p^\infty]$ is the Iwasawa main conjecture, a conditional input controlling one prime at a time; rank $\geq 2$ global finiteness stays open. See the [architecture-3 scorecard](../docs/03_research/research_directions/03_padic_archimedean.md).
- **The engine (experiment (l)):** the three detectors are promoted from a manual checklist to an automatic AUDIT gate ([`engine/audit.py`](engine/audit.py), a pure wrapper over [`controls.py`](_shared/controls.py)), and the atlas is encoded as a proof graph ([`engine/atlas_graph.py`](engine/atlas_graph.py)) so the frontier of the open regime is computed, not asserted. The parity wall is enforced structurally: parity is its own node with no edge into any full-rank claim, so no support set for weak BSD in rank $\geq 2$ ever routes through it. Spec: [`docs/03_research/engine/`](../docs/03_research/engine/README.md).
- **Experiment (m), Detector 3 (the headline risk):** the codim-1 Kudla shadow is genuinely number-field native (one moving leg, no Frobenius twist), which is exactly why it is computable over $\mathbb{Q}$, and it makes NO transfer claim. Its detector panel names the two function-field imports (the second leg over $X^r$, the Frobenius twist) that the rank-2 / codim-2 case would need and the shadow does not supply; [Direction 04](../docs/03_research/research_directions/04_kudla_clause_two_bridge.md) audits both Kudla bridges against Detector 3.
- **Experiment (n), Detector 2 + Detector 3:** the p-adic height regulator computes the rank-2 regulator side from INPUT points (Bridge 2 untouched, the points are found by search), witnessing the Clause-2 second-order quantity p-adically where the archimedean Gross-Zagier identity reads $0 = 0$. Detector 2: the $\det \mathrm{Reg}_p = (\text{stuff})\,L_p^{(2)}$ identity is p-adic BSD (conditional, one prime at a time), and $\#\mathrm{Sha}$ sits inside that leading term. Detector 3: the cyclotomic / weight axis is the number-field substitute for the Yun-Zhang second leg, no geometric Frobenius (one local-Tate near-miss flagged). The order gap is reframed as archimedean; the equality stays conjectural in rank 2. See [Direction 05](../docs/03_research/research_directions/05_padic_second_leg.md).

## How to run

```powershell
python -m experiments._shared.smoke_test
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
python -m experiments.engine.e_l_engine
python -m experiments.theta_shadow.e_m_theta_shadow
python -m experiments.padic_regulator.e_n_padic_regulator
```

Run from the repo root so `from experiments._shared import ...` resolves. The slowest steps are the rank-3 derivative search in (b), the 5077a1 Heegner sum in (e), and the twist confirmations in (g) (each tens of seconds to a few minutes).

## What would move the needle

Experiments (a)-(d) validate the substrate. Experiments (e)-(j) probe the rank-2 wall itself: (e) implements the proven machine and measures where it dies, (f) constructs the half of the rank-2 object that is constructible, (g) maps the parity-blind locus in a family, (h) verifies the Gross-Zagier identity itself to 24 digits, so the proven regime is a measured equation on our own substrate, (i) closes the strong-BSD formula to 27 digits on every open-regime curve with independently rebuilt regulators and leading coefficients, and (j) supplies the rigorous UPPER bound (f) left open, by 2-isogeny descent: it pins $\mathrm{rank}\,E_{34} = 2$ unconditionally and shows the (f) curves carry no rational 2-isogeny, naming the cubic-field obstruction per curve. The operational bar for any Research Direction 01 candidate is now concrete and two-sided: **produce non-torsion output on 389a1 where the Heegner machine in (e) provably outputs zero**, and output whose size does NOT factor through $L'(E/K, 1)$ (experiment (h) shows that one number is the machine's entire output), then pass Detector 1 (more than $w$) and Detector 3 (no geometric Frobenius). Experiment (k) opens the architecture-3 front: it computes the genuinely $p$-adic content (the exceptional zero and the Mazur-Tate-Teitelbaum $\mathcal{L}$-invariant) and names the two missing computational objects (the overconvergent modular-symbol $L_p$ and the $p$-adic height regulator). The next computational steps that would matter: build the overconvergent $L_p$ to confirm the Greenberg-Stevens derivative numerically, and a $p$-adic height regulator so the rank-$\geq 2$ $p$-adic leading term can be assembled.
