# Visualizations

> manim animation scripts for BSD concepts. Rendered video output is gitignored; the scene scripts are tracked.

## Scenes

| File | Scene | Shows |
|---|---|---|
| `group_law.py` | `GroupLawScene` | The chord-and-tangent group law on the curve $y^2 = x^3 - x + 1$: two rational points $P, Q$, the line through them, the third intersection, and the reflection giving $P + Q$. |

## Render

```powershell
manim -pql visualizations/group_law.py GroupLawScene
```

`-pql` previews at low quality; use `-qh` for high quality. Output lands in `media/` (gitignored). `manim` is in `requirements.txt`.

## Why the group law

The group law is the single most important picture in the elliptic-curve story: it is why a few rational points can generate infinitely many, why the rank is the central invariant, and why BSD is a statement about the SIZE of a group. Seeing the chord-and-tangent move makes the rank concrete.

## Future scenes (not yet built)

- The $L$-function near $s = 1$: order of vanishing as the analytic rank.
- The Sato-Tate semicircle building up as primes accumulate (the experiment (d) histogram, animated).
