# Shared substrate

> The common infrastructure every experiment imports. The BSD analog of the Riemann sibling repo's shared `zeta` / `lfunction` modules.

## Modules

| File | Role |
|---|---|
| `elliptic_curve.py` | The `EllipticCurve` class: point-count $a_p$, multiplicative $a_n$, the smoothed approximate functional equation for $L(E, s)$ and its derivatives at $s = 1$, the root number. |
| `curve_data.py` | Bundled table of curves by Cremona label, ranks 0 to 3, with public LMFDB/Cremona invariants. Runs offline. |
| `controls.py` | The three wrong-approach detectors (parity-only, Sha-finiteness assumed, function-field mirage) and the proven-vs-open control pair. |
| `rational_points.py` | Exact (Fraction) group law, small-height point search, Neron-Tate canonical heights by exact doubling, Gram matrices and determinants. The Mordell-Weil side the $L$-function cannot see. |
| `period_lattice.py` | Period lattice (rectangular $\Delta > 0$ and rhombic $\Delta < 0$), 2-torsion roots, Weierstrass parametrization. |
| `analytic_height.py` | $\sigma$-function canonical heights to ~20 digits and the elliptic logarithm; the high-precision height substrate for experiments (h) and (i). |
| `descent.py` | The 2-isogeny descent engine (experiment j): $\mathbb{Q}_p$-solubility lifter, Selmer group of a rational 2-isogeny, rigorous rank upper bound, and the long-model-to-2-torsion-form transform. |
| `smoke_test.py` | Phase 0 validation: 8 checks on the substrate, detectors, and descent engine. |
| `__init__.py` | Re-exports the public interface. |

## The EllipticCurve interface

A curve is a long Weierstrass equation $y^2 + a_1 xy + a_3 y = x^3 + a_2 x^2 + a_4 x + a_6$ plus its conductor and bundled arithmetic invariants. The methods experiments rely on:

- `a_p(p)`: trace of Frobenius $a_p = p + 1 - \#E(\mathbb{F}_p)$ at good primes by honest enumeration; bundled local value in $\{-1, 0, +1\}$ at bad primes.
- `a_n(n)`: the $n$-th Dirichlet coefficient, built multiplicatively from the $a_p$.
- `L_value(s)`: $L(E, s)$ via the smoothed AFE at the current `mpmath` precision.
- `L_derivative_at_one(order)`: $L^{(k)}(E, 1)$ by complex differentiation.
- `analytic_rank(...)`: least $k$ with $L^{(k)}(E, 1) \neq 0$.
- `root_number`: the sign $w = (-1)^{\text{analytic rank}}$.

## The smoothed approximate functional equation

The Dirichlet series $\sum a_n n^{-s}$ diverges at the central point $s = 1$ where BSD lives, so the functional equation is mandatory. With $\Lambda(E, s) = N^{s/2}(2\pi)^{-s}\Gamma(s) L(E, s)$ and $Q = \sqrt N / (2\pi)$, the smoothed AFE (incomplete-Gamma test function $G_z(x) = \Gamma(z, x)/\Gamma(z)$) gives
$$L(E, s) = \sum_n \frac{a_n}{n^s} G_s(n/Q) + w\, X(s) \sum_n \frac{a_n}{n^{2-s}} G_{2-s}(n/Q),$$
with $X(s) = Q^{2-2s}\Gamma(2 - s)/\Gamma(s)$. Both sums converge geometrically because $G$ decays like $\exp(-n/Q)$.

## The detectors

See `controls.py` docstrings. In short: a method that gives only parity (Detector 1), or silently assumes finite $\operatorname{Sha}$ in rank $\geq 2$ (Detector 2), or would run verbatim over a function field (Detector 3), has not closed BSD. The control pair (37a1 proven vs 389a1 open) demands a method do something genuinely new in the open regime.

## Run the smoke test

```powershell
python -m experiments._shared.smoke_test
```

Expected: `Smoke test: 8/8 passed`.

## Data attribution

Curve invariants are public, from the LMFDB (The L-functions and Modular Forms Database) and Cremona's ecdata tables, reproduced for offline use. Every bundled Weierstrass model is validated by an independent $L$-value computation (a rank-$r$ curve must have $L^{(k)}(E,1) \approx 0$ for $k < r$).
