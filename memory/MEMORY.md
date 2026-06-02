# MEMORY

> Cross-session context. Read at session start (per OPERATIONS.md). Durable facts and decisions that should survive between sessions; operational state lives in PHASE_STATE.md.

## What this repo is

A deep study + proof-program substrate for the Birch and Swinnerton-Dyer Conjecture. Layered docs, a validated computational thread, a Lean 4 skeleton, six agent role specs, and the three wrong-approach detectors.

## Durable facts (the math that does not change)

- BSD statement: weak form `ord_{s=1} L(E, s) = rank E(Q)`; strong form pins the leading coefficient to `Omega * Reg * prod c_p * #Sha / (#tors)^2`.
- PROVEN only for analytic rank 0 and 1 (Gross-Zagier 1986 + Kolyvagin 1990). Finiteness of Sha is a theorem only there.
- Modularity (Wiles; BCDT 2001) gives continuation, functional equation, and the root number `w = (-1)^{analytic rank}` (parity only).
- The rank-boundary thesis: every proven method is powered by a rank-1 object (one Heegner point), so it cannot certify rank >= 2. The open part of BSD is the rank >= 2 construction.
- Smallest curves by rank: 11a1 (rank 0), 37a1 (rank 1), 389a1 (rank 2), 5077a1 (rank 3).

## The three detectors (the discipline)

1. Parity-only: root number gives rank mod 2, not the rank.
2. Sha-finiteness assumed: finite Sha is open in rank >= 2; flag any use.
3. Function-field mirage: BSD over F_q(C) is a theorem (Tate/Artin-Tate); a method that runs there verbatim imported a geometric Frobenius.

## Key decisions and gotchas

- The experimental substrate is validated: smoke test 6/6; weak BSD holds 15/15 on the bundled table; strong BSD solved for #Sha lands at a perfect square; Sato-Tate matches (chi-square ~0.014).
- DATA GOTCHA: validate every bundled Weierstrass model by an independent L-value computation, not just by label. During scaffolding, several rank-2 records had wrong models (one was a copy of 37a1) and several periods/regulators were inconsistent; they were corrected so that L(1) (and L'(1)) vanish to the right order and #Sha lands at 1. The bundled `real_period` is the Cremona AGM value on the minimal b-form cubic; for rank >= 1 the `regulator` is set consistent with #Sha = 1.
- The AGM real period uses the b-form cubic y^2 = x^3 + (b2/4)x^2 + (b4/2)x + b6/4: two real components (3 real roots) give `2 pi / AGM(sqrt(e3-e1), sqrt(e3-e2))`; one component gives `pi / AGM(sqrt(D), sqrt((D + (e1-alpha))/2))`.
- Lean toolchain pinned to `leanprover/lean4:v4.13.0` to match the sibling zeta repo. The skeleton has documented `sorry`; it is not expected to build without Mathlib API that does not yet exist (canonical height, MW rank, Hasse-Weil L).

## The most-leveraged next move

Specify the rank-2 object (Research Direction 01) and run the spec through Detector 1 and Detector 3.

## Owner context

Owen, wheelchair user with muscular dystrophy. Typing is hard: be proactive, make decisions, offer A/B/C choices when input is needed. PowerShell on Windows. No em dashes or en dashes anywhere.
