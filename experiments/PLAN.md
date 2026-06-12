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

## Detector coverage

- **Detector 1 (parity-only):** invoked in (a) and (b); EXHIBITED in (g) (a family where $w$ misclassifies every rank-2 twist) and in (e) (37a1 and 5077a1 share $w = -1$, yet the machine outputs a point on one and torsion on the other, so the ceiling is not parity).
- **Detector 2 (Sha-finiteness):** invoked in (b) and (c). Flagged OPEN for every rank $\geq 2$ curve. (f) makes the asymmetry concrete: the lower bound rank $\geq r$ is constructed; the upper bound is exactly the missing Selmer/Sha input.
- **Detector 3 (function-field mirage):** documented in [`_shared/controls.py`](_shared/controls.py); none of the experiments imports a geometric Frobenius. (f) names the gap: over $\mathbb{F}_q(C)$ the upper bound comes from $H^2$ of the elliptic surface; over $\mathbb{Q}$ nothing here supplies it.

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
```

Run from the repo root so `from experiments._shared import ...` resolves. The slowest steps are the rank-3 derivative search in (b), the 5077a1 Heegner sum in (e), and the twist confirmations in (g) (each tens of seconds to a few minutes).

## What would move the needle

Experiments (a)-(d) validate the substrate. Experiments (e)-(i) probe the rank-2 wall itself: (e) implements the proven machine and measures where it dies, (f) constructs the half of the rank-2 object that is constructible, (g) maps the parity-blind locus in a family, (h) verifies the Gross-Zagier identity itself to 24 digits, so the proven regime is a measured equation on our own substrate, and (i) closes the strong-BSD formula to 27 digits on every open-regime curve with independently rebuilt regulators and leading coefficients. The operational bar for any Research Direction 01 candidate is now concrete and two-sided: **produce non-torsion output on 389a1 where the Heegner machine in (e) provably outputs zero**, and output whose size does NOT factor through $L'(E/K, 1)$ (experiment (h) shows that one number is the machine's entire output), then pass Detector 1 (more than $w$) and Detector 3 (no geometric Frobenius). The next computational steps that would matter: a $p$-adic $L$-function / Mazur-Tate-Teitelbaum thread (scoring architecture 3), and 2-descent Selmer bounds to make (f)'s upper-bound gap explicit curve by curve.
