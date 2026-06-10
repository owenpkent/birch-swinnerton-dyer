"""Experiment (e): run the proven rank-1 machine and measure its ceiling.

This is the experiment PLAN.md called the next needle-mover: implement the
Heegner-point construction (the engine of the ONLY proven BSD regime) and
watch what it outputs on either side of the rank boundary.

The machine, end to end, from first principles on our substrate:

  1. MODULARITY: the modular parametrization phi: X_0(N) -> E is computed
     from the curve's own point counts, phi(tau) = sum_n (a_n / n) q^n,
     q = e^{2 pi i tau} (Manin constant 1 for these optimal curves).
  2. HEEGNER POINTS: a fundamental discriminant D < 0 with every prime
     dividing N split in K = Q(sqrt D) gives CM points tau_A on X_0(N), one
     per ideal class A of K, via binary quadratic forms [A, B, C] with N | A
     and a fixed square root B0 of D mod 4N.
  3. THE POINT: y_K = sum_A phi(tau_A) lands in E(K) (theory of complex
     multiplication); its trace z = y_K + conj(y_K) lands in E(Q) as a
     lattice point z in C / Lambda. The period lattice comes from the AGM
     and is checked against the bundled real period; the Weierstrass
     parametrization converts z back to coordinates, exactly rationalized.

What Gross-Zagier proves: hhat(y_K) = c L'(E/K, 1) with c > 0. So the
machine outputs a NON-TORSION point exactly when L'(E/K, 1) != 0, which
(under the Heegner hypothesis, sign of E/K forced to -1) happens exactly
when the analytic rank of E/Q is <= 1. The experiment runs the SAME code on:

  - 37a1  (rank 1, w = -1): expect an actual rational point of infinite
    order, recovered exactly. The proven regime, working.
  - 389a1 (rank 2, w = +1): L(E,1) = L'(E,1) = 0 forces L'(E/K,1) = 0,
    so the machine must output TORSION. Rank 2 in, zero out.
  - 5077a1 (rank 3, w = -1): SAME root number as 37a1, yet the output is
    again torsion (this is Gross-Zagier's own witness, their Prop 7.4
    example). Parity cannot explain the difference: the ceiling is the
    one-point structure of the construction, not the sign.

That last contrast is the experiment's thesis, and the reason Detector 1 is
invoked at the end: the Heegner machine is strictly stronger than parity in
rank <= 1 and strictly silent above it. A rank >= 2 proof needs a construction
whose output does not factor through one derivative of one L-function.

Run from the repo root (takes ~1-2 minutes, dominated by 5077a1's a_n):
    python -m experiments.heegner_ceiling.e_e_heegner_ceiling
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd, isqrt
from typing import List, Tuple

import mpmath as mp

from experiments._shared import get_curve, parity_detector
from experiments._shared.period_lattice import (
    period_lattice,
    reduce_mod_lattice,
    x_from_z,
)
from experiments._shared.rational_points import canonical_height, lift_x, on_curve

LABELS = ["37a1", "389a1", "5077a1"]
TORSION_DENOM = 12     # torsion on these curves is tiny; 12 is generous
TORSION_TOL = 1e-6


# --------------------------------------------------------------------------
# binary quadratic forms: reduction, class number, Heegner representatives
# --------------------------------------------------------------------------

def is_fundamental(D: int) -> bool:
    if D >= 0:
        return False
    if D % 4 == 1:
        m = -D
    elif D % 4 == 0 and (D // 4) % 4 in (2, 3):
        m = -D // 4
    else:
        return False
    return all(m % (p * p) for p in range(2, isqrt(m) + 1))


def reduce_form(a: int, b: int, c: int) -> Tuple[int, int, int]:
    """Gauss reduction of a positive-definite form to its canonical reduced rep."""
    for _ in range(10000):
        if c < a:
            a, b, c = c, -b, a
            continue
        if b > a or b <= -a:
            r = (b + a) % (2 * a) - a            # lands in [-a, a)
            if r == -a:
                r = a                            # normalize to (-a, a]
            c = c + (r * r - b * b) // (4 * a)
            b = r
            continue
        if a == c and b < 0:
            b = -b
            continue
        return a, b, c
    raise RuntimeError(f"form reduction did not terminate: ({a}, {b}, {c})")


def reduced_forms(D: int) -> List[Tuple[int, int, int]]:
    """All reduced forms of discriminant D < 0; their count is h(D)."""
    forms = []
    for a in range(1, isqrt(-D // 3) + 1):
        for b in range(-a + 1, a + 1):
            if (b * b - D) % (4 * a):
                continue
            c = (b * b - D) // (4 * a)
            if c < a or (a == c and b < 0):
                continue
            forms.append((a, b, c))
    return forms


def heegner_representatives(N: int, D: int) -> List[Tuple[int, int]]:
    """One form [A, B, *] with N | A and B = B0 mod 2N per ideal class.

    These are the CM points tau = (-B + sqrt(D)) / (2A) on X_0(N) whose
    images under phi sum to the Heegner point y_K in E(K).
    """
    h = len(reduced_forms(D))
    B0 = next(B for B in range(2 * N) if (B * B - D) % (4 * N) == 0)
    found = {}
    a = 1
    while len(found) < h:
        if a > 200:
            raise RuntimeError(f"class reps not found for N={N}, D={D}")
        A = a * N
        # walk the progression B = B0 + 2Nj inside (-A, A] directly: ~a values
        j_min = (-A - B0) // (2 * N) + 1
        j_max = (A - B0) // (2 * N)
        for j in range(j_min, j_max + 1):
            B = B0 + 2 * N * j
            if (B * B - D) % (4 * A):
                continue
            C = (B * B - D) // (4 * A)
            key = reduce_form(A, B, C)
            if key not in found:
                found[key] = (A, B)
        a += 1
    return list(found.values())


def pick_discriminant(N: int, w_check) -> Tuple[int, List[Tuple[int, int]]]:
    """The admissible fundamental D minimizing total q-expansion terms.

    Admissible: fundamental, gcd(D, 2N) = 1 conditions via the Heegner
    hypothesis (N prime here, so (D/N) = +1), D not in {-3, -4} (extra
    units). Larger |D| converges FASTER (Im tau grows), so the cost metric
    rewards both large |D| and small class number.
    """
    best = None
    for D in range(-7, -600, -1):
        if not is_fundamental(D) or D in (-3, -4):
            continue
        if gcd(D, 2 * N) != 1:
            continue
        if w_check(D, N) != 1:
            continue
        reps = heegner_representatives(N, D)
        cost = sum(A for A, _ in reps) / mp.sqrt(-D)
        if best is None or cost < best[0]:
            best = (cost, D, reps)
    assert best is not None, f"no admissible Heegner discriminant for N={N}"
    return best[1], best[2]


# --------------------------------------------------------------------------
# the modular parametrization phi(tau) = sum a_n / n q^n
# --------------------------------------------------------------------------

def phi(E, A: int, B: int, D: int):
    """phi(tau_A) for tau_A = (-B + i sqrt(|D|)) / (2A), summed to dps digits."""
    tau = (mp.mpf(-B) + mp.mpc(0, 1) * mp.sqrt(mp.mpf(-D))) / (2 * A)
    q = mp.exp(2j * mp.pi * tau)
    qa = abs(q)
    n_max = int(mp.ceil((mp.mp.dps + 3) * mp.log(10) / (-mp.log(qa)))) + 60
    if n_max > 200000:
        raise RuntimeError(f"q-expansion needs {n_max} terms; pick a better D")
    acc = mp.mpc(0)
    qpow = mp.mpc(1)
    for n in range(1, n_max + 1):
        qpow *= q
        an = E.a_n(n)
        if an:
            acc += mp.mpf(an) / n * qpow
    return acc, n_max


# --------------------------------------------------------------------------
# classification of the output lattice point
# --------------------------------------------------------------------------

def classify(E, z, w1, w2, roots):
    """Reduce z mod Lambda and decide: zero / torsion / honest rational point."""
    alpha, beta = reduce_mod_lattice(z, w1, w2)
    fa, fb = float(alpha), float(beta)
    ra = Fraction(fa).limit_denominator(TORSION_DENOM)
    rb = Fraction(fb).limit_denominator(TORSION_DENOM)
    if abs(fa - float(ra)) < TORSION_TOL and abs(fb - float(rb)) < TORSION_TOL:
        kind = "ZERO POINT" if ra == 0 and rb == 0 else f"TORSION ({ra}, {rb})"
        return kind, (fa, fb), None
    # non-torsion: invert the Weierstrass parametrization and rationalize
    zz = alpha * w1 + beta * w2
    x = mp.re(x_from_z(zz, *roots))
    xr = Fraction(float(x)).limit_denominator(10 ** 8)
    P = lift_x(E, xr)
    return "NON-TORSION", (fa, fb), P


def main():
    mp.mp.dps = 22

    # kronecker for the Heegner admissibility test (N prime: need (D/N) = 1)
    def legendre(D, N):
        r = pow(D % N, (N - 1) // 2, N)
        return 1 if r == 1 else -1

    print("The Heegner machine, one code path, three curves across the boundary.")
    print()
    summary = []
    for label in LABELS:
        E = get_curve(label)
        N = E.conductor
        w1, w2, roots = period_lattice(E)

        # substrate checks: AGM lattice vs bundled period; p-function vs roots
        assert abs(2 * w1 - mp.mpf(E.real_period)) < 1e-6 * E.real_period, label
        x_half = x_from_z(w1 / 2, *roots)
        assert abs(x_half - roots[0]) < 1e-8, "Weierstrass param sanity"

        D, reps = pick_discriminant(N, legendre)
        h = len(reps)
        print(f"--- {label}: N={N}, rank {E.rank}, w={E.root_number:+d} ---")
        print(f"  lattice: w1={float(w1):.8f} (2 w1 = bundled Omega), "
              f"|w2|={float(mp.im(w2)):.8f}")
        print(f"  Heegner data: D={D} (h={h}), forms " +
              ", ".join(f"[{A},{B},.]" for A, B in reps))

        yK = mp.mpc(0)
        terms = 0
        for A, B in reps:
            zi, n_used = phi(E, A, B, D)
            yK += zi
            terms = max(terms, n_used)
        z_trace = yK + mp.conj(yK)

        kind, (fa, fb), P = classify(E, z_trace, w1, w2, roots)
        ya, yb = (float(t) for t in reduce_mod_lattice(yK, w1, w2))
        print(f"  q-expansion terms: {terms};  y_K mod Lambda = "
              f"({ya:+.10f}, {yb:+.10f})")
        print(f"  trace to E(Q) mod Lambda = ({fa:+.10f}, {fb:+.10f})  ->  {kind}")
        if kind == "NON-TORSION":
            assert P is not None and on_curve(E, P), (
                "non-torsion output failed exact rationalization: "
                "convention bug, do not trust this run")
            hh = canonical_height(E, P)
            m2 = hh / E.regulator
            print(f"  recovered rational point: ({P[0]}, {P[1]})  EXACT, on curve")
            print(f"  canonical height = {hh:.6f} = {m2:.3f} x regulator "
                  f"(Heegner index^2 ~ {round(m2)})")
        summary.append((label, E.rank, E.root_number, kind))
        print()

    print("=" * 72)
    print(f"{'curve':>8} {'MW rank':>8} {'w':>4} {'machine output':>28}")
    for label, r, w, kind in summary:
        print(f"{label:>8} {r:>8} {w:>+4} {kind:>28}")
    print("=" * 72)
    print()
    print("READING THE TABLE (the rank-1 ceiling, measured):")
    print("  37a1: the machine MANUFACTURES a rational point from modularity and")
    print("        CM alone. This is why analytic rank <= 1 is a theorem.")
    print("  389a1: same machine, rank-2 curve: output torsion. Gross-Zagier says")
    print("        hhat(y_K) is proportional to L'(E/K,1), which rank 2 kills.")
    print("  5077a1: w = -1, the SAME parity as 37a1, output still torsion. The")
    print("        ceiling is therefore NOT the root number: it is the fact that")
    print("        the construction outputs ONE point controlled by ONE derivative.")
    print()
    verdict = parity_detector(claims_full_rank=True, uses_only_root_number=True)
    print("DISCIPLINE (Detector 1):", verdict.message)
    print()
    print("CONSEQUENCE FOR THE PROGRAM: the rank >= 2 object cannot be a cleverer")
    print("Heegner point. Any candidate construction must output something whose")
    print("nonvanishing is NOT equivalent to L'(E/K, 1) != 0; this experiment is")
    print("the operational test any Research Direction 01 candidate must beat:")
    print("produce non-torsion output on 389a1 where this machine provably cannot.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
