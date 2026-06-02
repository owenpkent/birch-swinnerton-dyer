# Experiment (c): strong BSD quantities and the conjectural #Sha

> The strong form pins the leading Taylor coefficient of $L(E, s)$ at $s = 1$ to an exact arithmetic product. We solve it for $\#\operatorname{Sha}$ and check the result is a perfect square.

## The formula

With $r = \operatorname{rank} E(\mathbb{Q})$,
$$\frac{L^{(r)}(E, 1)}{r!} = \frac{\Omega_E \cdot \operatorname{Reg}_E \cdot \prod_p c_p \cdot \#\operatorname{Sha}(E)}{(\#E(\mathbb{Q})_{\mathrm{tors}})^2}.$$
Solving for the Tate-Shafarevich order:
$$\#\operatorname{Sha} = \frac{(L^{(r)}(E,1)/r!) \cdot (\#\text{tors})^2}{\Omega_E \cdot \operatorname{Reg}_E \cdot \prod_p c_p}.$$

## What it does

Compute the leading coefficient $L^{(r)}(E, 1)/r!$ from the $L$-function, take the bundled $\Omega$, $\operatorname{Reg}$, $\prod c_p$, torsion, and read off $\#\operatorname{Sha}$. As an independent check, the real period $\Omega$ is recomputed from scratch via the AGM of the Weierstrass roots.

## Run

```powershell
python -m experiments.strong_bsd_quantities.e_c_strong_bsd
```

## Result

On every bundled curve the formula solved for $\#\operatorname{Sha}$ lands near $1$, a perfect square, matching the listed analytic $\operatorname{Sha}$. The AGM recomputation of $\Omega$ reproduces the bundled real period independently, a second-path check on the period.

## Discipline

For a rank $\geq 2$ curve the experiment invokes Detector 2 and prints that finiteness of $\operatorname{Sha}$ is OPEN there: "$\#\operatorname{Sha} = 1$" means "the BSD formula is consistent with $\operatorname{Sha} = 1$," not a theorem. The Cassels-Tate pairing predicts $\#\operatorname{Sha}$ is a perfect square when finite; landing at $1$ is consistent with that.

## Honest status

In rank 0 and 1 the strong form's $p$-part is known in many cases (Skinner-Urban, Kato), so the consistency is expected. In rank $\geq 2$ the leading-coefficient formula and finite $\operatorname{Sha}$ are both open; the experiment is a consistency check, never a proof.
