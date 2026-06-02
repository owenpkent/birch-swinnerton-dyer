/-
  BSD: Birch and Swinnerton-Dyer formalization skeleton.

  Root module. Imports the submodules that state, with documented `sorry`,
  the rank equality (weak BSD), the parity statement, the strong-form identity,
  and the rank-2 certificate target.

  This is a skeleton. The statements are the deliverable; the proofs await
  Mathlib API (canonical height, Mordell-Weil rank, Hasse-Weil L-function)
  that does not yet exist. No theorem here is claimed proven.
-/

import BSD.EllipticCurveDefs
import BSD.MordellWeil
import BSD.LFunction
import BSD.RootNumber
import BSD.RankEquality
import BSD.StrongBSD
