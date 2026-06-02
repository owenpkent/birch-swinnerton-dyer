import Lake
open Lake DSL

package BSD where
  -- Package configuration for the Birch-Swinnerton-Dyer formalization skeleton.

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.13.0"

@[default_target]
lean_lib BSD where
  -- Library configuration. The root module is BSD.lean; submodules live in BSD/.
