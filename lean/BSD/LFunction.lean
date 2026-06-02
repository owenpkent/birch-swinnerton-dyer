/-
  The Hasse-Weil L-function and the analytic rank.

  Mathlib does not yet have the Hasse-Weil L-function of an elliptic curve, its
  analytic continuation (which comes from modularity), or its order of vanishing
  at s = 1. We state the analytic rank as the order of vanishing and `sorry` the
  construction of L itself.
-/

import BSD.EllipticCurveDefs
import Mathlib.Analysis.SpecialFunctions.Complex.Analytic

namespace BSD

/-- The Hasse-Weil L-function `L(E, s)` as a function of a complex variable.
    MISSING MATHLIB INPUT: the Euler product over good/bad primes, and the
    analytic continuation supplied by modularity (Wiles; BCDT). -/
noncomputable def LFunction (_E : RationalEC) : ℂ → ℂ :=
  sorry

/-- The analytic rank: the order of vanishing of `L(E, s)` at the central point
    `s = 1`. MISSING MATHLIB INPUT: analytic continuation, so the order of
    vanishing is well defined. -/
noncomputable def analyticRank (_E : RationalEC) : ℕ :=
  sorry

end BSD
