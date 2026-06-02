/-
  The Mordell-Weil group and its rank.

  Mathlib has the group law on the points of a Weierstrass curve. It does NOT
  yet have the Mordell-Weil theorem (finite generation of E(ℚ)) in a form that
  exposes a usable `rank : ℕ`. We state the rank as the target invariant and
  `sorry` the finite-generation input.
-/

import BSD.EllipticCurveDefs

namespace BSD

/-- The Mordell-Weil rank of `E(ℚ)`: the free rank of the finitely generated
    abelian group `E(ℚ)`.

    MISSING MATHLIB INPUT: the Mordell-Weil theorem (E(ℚ) is finitely generated)
    and an API exposing the free rank. Until then this is a placeholder marked
    `sorry`. -/
noncomputable def mordellWeilRank (_E : RationalEC) : ℕ :=
  sorry

/-- The Mordell-Weil theorem: `E(ℚ)` is finitely generated.
    MISSING MATHLIB INPUT: not yet formalized in usable form. -/
theorem mordellWeil_fg (_E : RationalEC) :
    True := by
  -- Placeholder for: `AddGroup.FG (E(ℚ))`.
  trivial

end BSD
