# Research: the proof program and current frontier

> Prerequisites: graduate arithmetic geometry. This is the frontier layer. It states the proof program, the rank-boundary thesis, and points to the numbered research directions and reading notes.

## The proof program in one paragraph

BSD is a theorem for analytic rank 0 and 1 (Gross-Zagier + Kolyvagin) and open beyond. The program's organizing thesis is the **rank-boundary thesis**: every proven technique is powered by a rank-1 object (a single Heegner point, or an Euler system tied to it), so it structurally cannot certify rank $\geq 2$. The open part of BSD is the construction of $\geq 2$ independent rational points, or an unconditional bound on $\operatorname{Sha}$, in the rank $\geq 2$ regime. The program is a disciplined search for that missing object, with three detectors that reject the standard ways an argument secretly stays in the proven regime.

## The frontier, sharpened

What is in hand versus missing (see [`STATE_OF_THE_PROGRAM.md`](../../STATE_OF_THE_PROGRAM.md) for the full table):

- **In hand.** Rank 0, 1 fully proven. The $p$-adic main conjecture (Skinner-Urban) and Kato's Euler system give the $p$-part of BSD in many rank $\leq 1$ cases. The function-field template (Tate/Artin-Tate). A validated experimental substrate.
- **Missing.** A construction producing $\geq 2$ independent points (a higher-rank Heegner analog), OR an Euler system bounding $\operatorname{Sha}$ unconditionally in rank $\geq 2$.

## The three detectors as research discipline

Any candidate is scored against the detectors in [`experiments/_shared/controls.py`](../../experiments/_shared/controls.py):

1. **Parity-only.** Does the method pin the exact rank, or only its parity? Parity is free from modularity and the parity conjecture; it is not BSD.
2. **Sha-finiteness assumed.** Does the argument silently assume finite $\operatorname{Sha}$ in the open regime?
3. **Function-field mirage.** Would the argument run verbatim over $\mathbb{F}_q(C)$? If so it imported a geometric Frobenius the number-field case lacks.

A candidate that survives all three on a rank $\geq 2$ curve is a genuine construction target.

## Subfolders

- [`research_directions/`](research_directions/): numbered, research-grade execution specs. Each states a concrete object to build, the detector checks it must pass, and a falsifiability trigger.
- [`reading_notes/`](reading_notes/): notes on the reference library (Gross-Zagier, Kolyvagin, Skinner-Urban, Bhargava-Shankar, the function-field literature).

## Honest odds

An unconditional BSD proof in rank $\geq 2$ is a generational result. The near-term value of this program is the sharp map of the rank boundary and a substrate that lets a collaborator rule out a parity-only or function-field-only dead end quickly. The most-leveraged next move is to specify the rank-2 object precisely (Research Direction 01) and run it through Detectors 1 and 3.
