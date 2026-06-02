/-
  The strong-form leading-coefficient identity.

  Strong BSD pins the leading Taylor coefficient of L(E, s) at s = 1 to
    Ω_E · Reg_E · ∏_p c_p · #Sha(E) / (#E(ℚ)_tors)^2.
  Every factor except L itself is an arithmetic invariant; Sha must be finite
  for the statement to make sense. We `sorry` the construction of each factor
  and the identity.
-/

import BSD.RankEquality

namespace BSD

/-- The real period Ω_E. MISSING MATHLIB INPUT: integration of the Neron
    differential over the real points (the AGM gives it numerically). -/
noncomputable def realPeriod (_E : RationalEC) : ℝ := sorry

/-- The regulator Reg_E: the determinant of the Neron-Tate height pairing on a
    basis of the free part of E(ℚ). MISSING MATHLIB INPUT: the canonical height. -/
noncomputable def regulator (_E : RationalEC) : ℝ := sorry

/-- The Tamagawa product ∏_p c_p. MISSING MATHLIB INPUT: Néron models / Kodaira
    types. -/
noncomputable def tamagawaProduct (_E : RationalEC) : ℕ := sorry

/-- The order of the torsion subgroup #E(ℚ)_tors. -/
noncomputable def torsionOrder (_E : RationalEC) : ℕ := sorry

/-- The order of the Tate-Shafarevich group #Sha(E), PRESUPPOSING it is finite.
    Finiteness is PROVEN only for analytic rank ≤ 1; in rank ≥ 2 it is OPEN
    (this is Detector 2). MISSING MATHLIB INPUT: Sha and its finiteness. -/
noncomputable def shaOrder (_E : RationalEC) : ℕ := sorry

/-- The leading Taylor coefficient `L^(r)(E,1)/r!` at the central point. -/
noncomputable def leadingCoefficient (_E : RationalEC) : ℝ := sorry

/-- Strong BSD: the leading coefficient equals the arithmetic product.
    Presupposes `shaOrder` is the order of a finite group. OPEN beyond rank ≤ 1
    (the p-part is known in many cases: Skinner-Urban, Kato). -/
theorem strongBSD (E : RationalEC) :
    leadingCoefficient E
      = (realPeriod E * regulator E * (tamagawaProduct E : ℝ) * (shaOrder E : ℝ))
        / ((torsionOrder E : ℝ) ^ 2) := by
  sorry

end BSD
