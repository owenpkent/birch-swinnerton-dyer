# Lean 4 / Mathlib formalization skeleton

> A skeleton, not a build. It states the BSD rank equality, the strong-form identity, the root-number/parity statement, and the rank-2 certificate as Lean targets with documented `sorry`. The skeleton is not expected to compile against a fixed Mathlib without the canonical-height and Mordell-Weil API that Mathlib does not yet expose; the value is the precise statements.

## Toolchain

`lean-toolchain` pins `leanprover/lean4:v4.13.0`, matching the sibling Riemann (zeta) repo. `lakefile.lean` requires Mathlib at the same tag.

## Build (requires elan + lake)

```powershell
cd lean
lake update
lake build
```

This pulls Mathlib (large). The skeleton modules contain `sorry`, so a full build is not the point; the point is that the statements typecheck against Mathlib's `EllipticCurve` / `WeierstrassCurve` API where that API exists.

## What Mathlib already has

- `WeierstrassCurve` and `EllipticCurve` over a commutative ring, with the discriminant and $j$-invariant.
- The group law on the points of a `WeierstrassCurve` (in progress / partial across Mathlib versions).

## What Mathlib does not yet have (so we `sorry` it)

- The canonical (Neron-Tate) height and the height pairing / regulator.
- The Mordell-Weil theorem in a usable "rank" form.
- The Hasse-Weil $L$-function $L(E, s)$ and its analytic continuation.
- The Tate-Shafarevich group and the strong-BSD product.

Each is marked in the module that needs it, with a note on the missing API.

## Modules

| File | States |
|---|---|
| `BSD.lean` | Root module; imports the submodules. |
| `BSD/EllipticCurveDefs.lean` | A rational elliptic curve and its conductor (wraps Mathlib). |
| `BSD/MordellWeil.lean` | The Mordell-Weil group and its rank. |
| `BSD/LFunction.lean` | The Hasse-Weil $L$-function and the analytic rank. |
| `BSD/RootNumber.lean` | The root number and the parity statement. |
| `BSD/RankEquality.lean` | Weak BSD (the rank equality) and the rank-2 certificate. |
| `BSD/StrongBSD.lean` | The strong-form leading-coefficient identity. |

Every `sorry` carries a comment naming the missing input. None of these is claimed proven.
