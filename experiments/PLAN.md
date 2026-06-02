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

## Detector coverage

- **Detector 1 (parity-only):** invoked in (a) and (b). The rank is found by derivative vanishing, not by the root number alone; the detector confirms a parity-only conclusion would be incomplete.
- **Detector 2 (Sha-finiteness):** invoked in (b) and (c). Flagged OPEN for every rank $\geq 2$ curve.
- **Detector 3 (function-field mirage):** documented in [`_shared/controls.py`](_shared/controls.py); none of the experiments imports a geometric Frobenius.

## How to run

```powershell
python -m experiments._shared.smoke_test
python -m experiments.l_function_rank.e_a_analytic_rank
python -m experiments.weak_bsd_table.e_b_weak_bsd
python -m experiments.strong_bsd_quantities.e_c_strong_bsd
python -m experiments.sato_tate.e_d_sato_tate
```

Run from the repo root so `from experiments._shared import ...` resolves. The rank-3 derivative search at high precision is the slowest step (tens of seconds to a few minutes).

## What would move the needle

The experiments validate the substrate; they do not attempt the open problem. The next computational step that would matter is to implement a candidate rank-2 construction (Research Direction 01) and test whether its output passes Detector 1 and Detector 3 on the bundled rank-2 curves (389a1, 433a1, 571a1, 643a1).
