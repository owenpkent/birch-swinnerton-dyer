/-
  The root number and the parity statement.

  The root number w = ±1 is the sign of the functional equation. It forces
  w = (-1)^(analytic rank). The parity conjecture (a THEOREM: Nekovar;
  Dokchitser-Dokchitser) then equates the parity of the analytic rank with the
  parity of the Mordell-Weil rank. This is the LEVEL-0 statement: it gives only
  the rank mod 2, NOT the rank. Detector 1 in the experimental thread guards
  exactly against confusing this with full BSD.
-/

import BSD.LFunction
import BSD.MordellWeil

namespace BSD

/-- The root number `w ∈ {-1, +1}` of `E`, the sign of the functional equation.
    MISSING MATHLIB INPUT: the functional equation from modularity. -/
noncomputable def rootNumber (_E : RationalEC) : ℤ :=
  sorry

/-- The functional-equation sign fixes the parity of the analytic rank:
    `rootNumber E = (-1) ^ analyticRank E`.
    This is a consequence of the functional equation, not of BSD. -/
theorem rootNumber_eq_neg_one_pow_analyticRank (E : RationalEC) :
    rootNumber E = (-1 : ℤ) ^ (analyticRank E) := by
  -- Follows from Λ(E,s) = w Λ(E, 2-s) once `LFunction` and its continuation exist.
  sorry

/-- Parity conjecture (THEOREM, Nekovar; Dokchitser-Dokchitser): the analytic
    rank and the Mordell-Weil rank have the same parity.

    NOTE: this is the LEVEL-0 statement. It gives rank mod 2 only. It does NOT
    give the rank, so it cannot distinguish rank 0 from 2. Proving it does not
    prove BSD; see Detector 1. -/
theorem parity (E : RationalEC) :
    analyticRank E % 2 = mordellWeilRank E % 2 := by
  sorry

end BSD
