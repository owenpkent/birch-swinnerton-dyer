/-
  A rational elliptic curve and its conductor.

  Wraps Mathlib's `WeierstrassCurve` / `EllipticCurve` over `ℚ`. Mathlib has the
  Weierstrass model, discriminant, and j-invariant. The conductor is not yet in
  Mathlib in a usable form, so we carry it as data.
-/

import Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass

namespace BSD

open WeierstrassCurve

/-- A rational elliptic curve: a Mathlib `EllipticCurve ℚ` together with its
    conductor `N` as carried data (Mathlib does not yet compute the conductor). -/
structure RationalEC where
  curve : EllipticCurve ℚ
  conductor : ℕ
  conductor_pos : 0 < conductor

/-- The set of rational points `E(ℚ)`. Mathlib's point type for the affine
    Weierstrass model; the group structure is recorded in `MordellWeil`. -/
def RationalEC.points (E : RationalEC) : Type :=
  (E.curve).toWeierstrassCurve.Point

end BSD
