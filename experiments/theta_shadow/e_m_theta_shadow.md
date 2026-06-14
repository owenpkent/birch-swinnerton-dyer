# Experiment (m): the rank-1 theta shadow of the Kudla generating series

Run: `python -m experiments.theta_shadow.e_m_theta_shadow` (offline, ~7s).

## One-line claim, stated honestly

This experiment computes the **proven codimension-1 case** of Kudla's
modularity, end to end, on the congruent-number family. That case is
Waldspurger's theorem. It is a **theorem in the proven analytic-rank-$\leq 1$
regime**. It is the **rank-1 / codimension-1 / genus-1 SHADOW** of the rank-2 /
codimension-2 / genus-2 object that Direction 01's Clause 2 actually demands.
It is **NOT** progress on that open object, and nothing here implies Kudla
solves rank 2. The experiment prints this gap loudly and audits it against
Detector 3.

## Why this is the Kudla shadow

Kudla's program (reading note
[`Kudla-2004-Special-Cycles-Derivatives-Eisenstein.md`](../../docs/03_research/reading_notes/Kudla-2004-Special-Cycles-Derivatives-Eisenstein.md))
attaches to a quadratic space of signature $(n, 2)$ a Shimura variety carrying
special cycles $Z(T, \varphi)$ of codimension $r$, and conjectures that the
generating series $\sum_T \widehat{Z}(T, v)\, q^T$ is a Siegel modular form of
genus $r$ whose arithmetic degrees match the central **derivative** of a
genus-$r$ Siegel-Eisenstein series. The only fully proven case is $r = 1$
(codimension 1), and there it has classical names: Gross-Kohnen-Zagier on the
height side, **Waldspurger** on the value side.

The genus-1 / codimension-1 case has $r = 1$: a single moving leg. Over $\mathbb{Q}$
that leg degenerates to CM points on a modular curve, a genuine number-field
object, which is exactly why this case is computable offline. The genus-2 /
codimension-2 case ($r = 2$) is the open Clause-2 object, and it is precisely
the case with no number-field shadow (see the Detector-3 audit below).

## The measured equation

For the quadratic-twist family $E_n : y^2 = x^3 - n^2 x$ (the $n$-th
congruent-number curve, $n$ odd squarefree), Waldspurger's theorem gives a
**value identity**: for $n$ with root number $w(E_n) = +1$ (Tunnell's branch
$n \equiv 1, 3 \pmod 8$),

$$L(E_n, 1) = \kappa \cdot \frac{c_n^2}{\sqrt{n}}, \qquad \kappa > 0 \text{ CONSTANT in } n.$$

Here $c_n$ is the $n$-th Fourier coefficient of Tunnell's explicit weight-$3/2$
theta form, the Shimura-Waldspurger partner of the weight-2 newform $f_{E_1}$.
The experiment computes both sides independently and prints the residual:

- $c_n$ **from scratch** by integer-triple lattice counting (Tunnell 1983):
$$c_n = \#\{2x^2 + y^2 + 8z^2 = n\} - 2\,\#\{2x^2 + y^2 + 32z^2 = n\};$$
- $L(E_n, 1)$ by the same $w = +1$ closed form as experiment (g),
$L(E_n,1) = 2\sum_k (a_k/k)\,e^{-2\pi k/\sqrt{N}}$, $N = 32 n^2$.

The headline number is $\kappa_n = L(E_n,1)\sqrt{n}/c_n^2$ and its residual
against the closed form. Observed:

```
worst |kappa_n / kappa_closed - 1| over the scan = 7.889e-31
```

so $\kappa$ is constant to ~30 digits across $n \in \{1,3,11,17,19,33,35,43,51,57,59\}$.
This is Waldspurger exhibited numerically.

## Three independent ground-truth anchors (all offline)

1. **Tunnell coefficients $c_n$.** Computed in-repo by lattice enumeration; no
   imported half-integral-weight table. A tiny bundled spot-check
   (`TUNNELL_KNOWN`, with Tunnell-1983 citation) asserts
   $c_1 = -2$, $c_3 = -4$, $c_{11} = 4$, $c_{17} = 8$, $c_{33} = -8$, etc.
2. **The proportionality constant, two ways.**
   (a) measured $\kappa_n = L(E_n,1)\sqrt{n}/c_n^2$, required constant
   (Waldspurger); observed $0.163878597143257488$.
   (b) closed form $\kappa = \Omega_{E_1}/32$ with $\Omega_{E_1}$ the real
   period of $E_1$, computed from `period_lattice_any` and cross-checked
   against the CM closed form $2\pi/\mathrm{AGM}(1, \sqrt{2}) = 5.24411510858\ldots$.
   The two agree to all printed digits.
3. **Congruent-number vanishing.** $c_n = 0 \iff L(E_n, 1) = 0$, checked
   against the classical small congruent numbers (`CONGRUENT_ODD_SQUAREFREE`,
   Koblitz; OEIS A003273). The $n = 41$ row is **retained and labeled**: $41$
   is not congruent, yet $c_{41} = 0$ and $L(E_{41}, 1) = 6.7\times 10^{-31}$
   (E_{41} has analytic rank 2). The implication $c_n = 0 \Rightarrow L = 0$ is
   Waldspurger (proven); the converse $L = 0 \Rightarrow$ congruent $\Rightarrow$
   rank $\geq 1$ is **BSD-conditional**, and $n = 41$ is exactly the row where
   it bites. Flagged, not dropped.

## Detector audit

### Detector 3 (function-field mirage), the HEADLINE risk

The Kudla higher-derivative layer is a **theorem over function fields**
(Yun-Zhang, all orders $r$; reading note
[`Yun-Zhang-2017-Shtukas-Taylor-Expansion.md`](../../docs/03_research/reading_notes/Yun-Zhang-2017-Shtukas-Taylor-Expansion.md))
and only a **vision over $\mathbb{Q}$**. The two function-field imports the
rank-2 case needs, and which this shadow does **not** supply:

1. **The $r$ moving legs over $X^r$.** $\mathrm{Sht}^r_G$ fibers over $X^r$:
   $r$ modification points move along $r$ independent copies of the curve. The
   number-field analog of even $X \times X$ (something like
   $\mathrm{Spec}\,\mathbb{Z} \times_{\mathbb{F}_1} \mathrm{Spec}\,\mathbb{Z}$)
   does not exist. One leg degenerates to CM points on a modular curve (a
   number-field object); the **second leg has no $\mathbb{Q}$-shadow**.
2. **The Frobenius twist.** A shtuka is a bundle with an isomorphism to its
   Frobenius pullback away from the legs; geometric $\mathrm{Frob}_q$ enters the
   definition itself.

The codimension-1 shadow has $r = 1$ (one leg, a genuine number-field object)
and **no Frobenius dependence**, which is exactly why it is computable over
$\mathbb{Q}$. This experiment crosses **neither** import and makes **no**
transfer-to-$\mathbb{Q}$ claim. `function_field_mirage(False, False)` returns
clean. The mirage would fire only if the writeup pretended genus-1 success
extends to genus 2. It does not.

### Detector 1 (parity-only)

Not a risk in the usual direction: the proportionality is a **value identity**,
strictly finer than parity. Guarded: the $c_n = 0 \iff L = 0$ readout is
central-value vanishing (analytic); the converse $\Rightarrow$ congruent
$\Rightarrow$ rank $\geq 1$ is flagged BSD-conditional via the retained $n = 41$
row. No rank certificate is claimed.

### Detector 2 (Sha-finiteness)

Not applicable. The shadow lives in the proven analytic-rank-$\leq 1$ regime
(Kolyvagin), so no Sha-finiteness assumption is imported into the open regime.

## The honest gap (the point of the experiment)

- **VERIFIED:** Waldspurger's theorem, the codim-1 theta correspondence. The
  proportionality ties a **first** central value to the **square of one**
  weight-$3/2$ coefficient. It factors through a single Taylor coefficient by
  design: the same one-coefficient bottleneck experiments (e), (g), (h)
  measured, now seen from the theta side.
- **OPEN (the actual Clause-2 object):** the rank-2 / codim-2 / genus-2 case,
  where Kudla's vision demands
  $\det R = \kappa \cdot L''(E/K, 1)/2!$ ($\det R$ a $2\times 2$ regulator) tied
  to a **second** derivative via a codim-2 arithmetic special cycle and a
  genus-2 Siegel-Eisenstein series. **Nothing here** computes or implies that
  identity.
- **Both bridges remain uncrossed.**
  - **Bridge 1** (Eisenstein/doubling $L \to L(E, s)$): in the shadow this is
    the classical Shimura correspondence, fine at codim 1. At codim 2,
    transferring a genus-2 central derivative into the **second Taylor
    coefficient** of one Hasse-Weil $L(E, s)$ is not in the proven layer.
  - **Bridge 2** (cycle class $\to$ rational point): **even in this shadow no
    point is produced.** The output is an $L$-value and a theta coefficient,
    not an element of $E(\mathbb{Q})$. The congruent $n$ with $c_n = 0$ are
    exactly where $E_n$ has rank $\geq 1$, but the shadow does **not** return a
    generator (that is the separate first-derivative Heegner machine, (e)/(h)).

So in analytic rank $\geq 2$, numerical agreement would be **evidence**, never
**proof**. Here there is no rank-2 claim at all. This whole front is a **spec**
(Direction 01, Clause 2) plus a **rank-1 shadow**.

## Reused substrate

- `experiments._shared.EllipticCurve`: honest $a_p$ point counting, $a_n$
  recurrence; $E_1$ and each $E_n$ built directly (bypassing
  `curve_data._build`, since the conductor $32 n^2$ is not squarefree).
- `experiments.twist_parity.e_g_twist_parity`: the `_n_max` term-count helper,
  the Fricke fixed-point root-number test (S5), and `kronecker`.
- `experiments._shared.period_lattice.period_lattice_any`: independent
  $\Omega_{E_1}$.
- `experiments._shared.controls`: `function_field_mirage`,
  `function_field_template`, `parity_detector` for the panel.

Experiment (h)'s sigma-function height machinery is **not** used (Approach A is
$L$-value plus theta-coefficient only), removing the most convention-fragile
dependency.

## Self-tests (assertions; non-zero exit on failure)

- **S1** Tunnell counts match the bundled spot values.
- **S2** $\kappa_n$ constant across the $w = +1$ scan to $10^{-10}$ (observed
  $7.9\times 10^{-31}$).
- **S3** $\Omega_{E_1}$ two ways (period lattice vs CM AGM) agree.
- **S4** vanishing $\iff$ congruent on the bundled list (with the $n = 41$
  caveat), and $|L(E_n, 1)| < 10^{-12}$ on every $c_n = 0$ row.
- **S5** every scanned $E_n$ passes the Fricke root-number test ($w = +1$).
- **Detector panel** prints clean verdicts; Detector 3 is the headline.

A sub-second guard is added to `experiments/_shared/smoke_test.py` as check 10
($c_3 = -4$ and $\kappa = \Omega_{E_1}/32$ to 8 digits); the smoke test stays
green at 10/10.
