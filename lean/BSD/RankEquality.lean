/-
  Weak BSD (the rank equality) and the rank-2 certificate target.

  The headline statement: the analytic rank equals the Mordell-Weil rank. This
  is PROVEN for analytic rank ≤ 1 (Gross-Zagier + Kolyvagin) and OPEN for rank
  ≥ 2. We state the full equality as a `sorry` target and, separately, the
  rank-2 certificate (two independent points with nonzero height-pairing
  determinant) that Research Direction 01 is trying to construct.
-/

import BSD.LFunction
import BSD.MordellWeil

namespace BSD

/-- Weak BSD: the analytic rank equals the Mordell-Weil rank.
    PROVEN for `analyticRank E ≤ 1` (Gross-Zagier 1986 + Kolyvagin 1990).
    OPEN for `analyticRank E ≥ 2`. Stated here as the goal. -/
theorem weakBSD (E : RationalEC) :
    analyticRank E = mordellWeilRank E := by
  -- Proven regime: analyticRank ≤ 1. Open regime: analyticRank ≥ 2.
  sorry

/-- The proven regime, isolated: when the analytic rank is at most 1, the rank
    equality is a theorem. MISSING MATHLIB INPUT: Heegner points, the
    Gross-Zagier height formula, Kolyvagin's Euler system. -/
theorem weakBSD_of_analyticRank_le_one (E : RationalEC)
    (_h : analyticRank E ≤ 1) :
    analyticRank E = mordellWeilRank E := by
  sorry

/-- The rank-2 certificate target (Research Direction 01): a construction that,
    on a curve of analytic rank ≥ 2, produces two rational points whose
    Neron-Tate height-pairing matrix has nonzero determinant, certifying
    Mordell-Weil rank ≥ 2.

    This is the OPEN frontier object. The `sorry` here is the construction we do
    not have. A single Heegner point cannot fill it (one point gives a rank-1
    pairing matrix). -/
theorem rankTwoCertificate (E : RationalEC)
    (_h : 2 ≤ analyticRank E) :
    2 ≤ mordellWeilRank E := by
  sorry

end BSD
