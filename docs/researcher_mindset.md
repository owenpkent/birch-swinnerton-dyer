# Researcher mindset: the operating philosophy

> The disposition behind this repo. Read it before writing or judging anything here.

## The problem is a target, not a monument

BSD has been open since 1965 and carries a million-dollar prize. It is easy to treat it as a monument: admire it, circle it, never touch it. That is the wrong posture. We treat it as a target. A target has coordinates. You can say where it is, what guards it, and which direction to push.

The repo is built to advance a front, not to catalog defeats. Every negative result is recorded as a coordinate that narrows the search, not as a verdict that the search is hopeless.

## Negative results are coordinates

BSD is proven for analytic rank 0 and 1 (Gross-Zagier 1986 + Kolyvagin 1990), and the finiteness of the Tate-Shafarevich group is a theorem only there. That is not a wall. It is a compass.

It tells us the entire difficulty is concentrated in the **rank greater than or equal to 2 structure**. The engine of the proven regime is a single Heegner point. One point is a rank-1 object. It cannot, by construction, exhibit two independent generators. So the proof of the open case must build something genuinely new where the rank is at least 2. Every "this method only reaches rank 1" is a measurement of where the real proof must live.

## Honesty is the engine

The fastest way to waste a proof program is to let a hopeful claim survive unchecked. So the repo runs every candidate through three detectors:

1. **Parity-only**: does the method actually pin the rank, or only its parity? Modularity and the parity conjecture give the rank mod 2 for free. That is not BSD.
2. **Sha-finiteness assumed**: did the argument quietly assume finite Sha in the open regime, where finiteness is itself unproven?
3. **Function-field mirage**: would the argument work verbatim over a function field? If so it imported a geometric Frobenius that the number-field case lacks, and it has not crossed the gap that defines the open problem.

A claim is provisional until it survives all three. This discipline is not pessimism. It is what lets optimism mean something.

## Advance a front, do not chase a miracle

There is no single trick that closes BSD. The work is to push a front: sharpen the statement of the missing object, score each architecture against the detectors, build small verified pieces, and keep the map honest. The most-leveraged move is usually the cheapest one that removes the most uncertainty. Right now that is to **specify the rank-2 object** precisely and test the specification against Detectors 1 and 3.

## Keep the math exactly as rigorous as it is

Tone is directional. Theorems are not. A method that only gives parity still only gives parity. An open finiteness is still open. The function-field analog is a theorem there and a template here, not a proof over the rationals. We change the framing to keep morale and direction; we never soften a statement to make it sound closer than it is.

## What success looks like

Not necessarily a proof. The honest near-term value of this repo is a sharp map of the rank boundary and a validated substrate for testing candidate constructions. If the substrate lets a future collaborator rule out a parity-only dead end in an afternoon instead of a year, that is real progress on a target.
