# Experiment (d): Sato-Tate semicircle as an a_p pipeline check

> The most direct test of the point-counting machinery. For a non-CM curve, $a_p / (2\sqrt p)$ should follow the Sato-Tate semicircle. A systematic point-counting bug would distort the histogram.

## What it does

For 37a1 (non-CM, conductor 37), compute $a_p / (2\sqrt p)$ for all good primes up to 5000, bin the values into 10 bins on $[-1, 1]$, and compare the empirical distribution to the semicircle density $\frac{2}{\pi}\sqrt{1 - x^2}$.

## Run

```powershell
python -m experiments.sato_tate.e_d_sato_tate
```

## Result

Over 668 primes up to 5000 the empirical distribution tracks the semicircle closely, with a chi-square-like summed relative deviation of $\approx 0.014$. The histogram visibly peaks near the center and tapers at $\pm 1$, as the semicircle predicts.

## Why this validates everything else

The Sato-Tate conjecture is a THEOREM for non-CM elliptic curves over $\mathbb{Q}$ (Clozel-Harris-Shepherd-Barron-Taylor; Barnet-Lamb-Geraghty-Harris-Taylor). So a good fit is not evidence about Sato-Tate; it is a validation of the $a_p$ computation that feeds the $L$-function in every other experiment. If point counting had a systematic error, the histogram would deviate from the semicircle.

## Note

This experiment does not test BSD. It tests the foundation BSD's analytic side is built on: correct traces of Frobenius.
