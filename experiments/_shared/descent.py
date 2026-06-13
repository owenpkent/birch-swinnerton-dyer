"""Descent by a rational 2-isogeny: rigorous, number-field-free rank bounds.

This module supplies the UPPER-BOUND half of the rank-r object that experiment
(f) (independent_points) leaves open. Experiment (f) builds the lower bound
rank E(Q) >= r by exhibiting r independent points; the matching upper bound
rank E(Q) <= r is the Selmer/Sha side. For one special but classical class of
curves the upper bound is computable today with no number fields, no class
groups, and no assumption that Sha is finite: curves with a rational 2-torsion
point, via descent by the 2-isogeny they carry (Silverman, AEC X.4).

Setup. A curve with a rational 2-torsion point at the origin is

    E : y^2 = x^3 + a x^2 + b x          (b != 0, a^2 - 4b != 0)

It carries a 2-isogeny phi : E -> E' to

    E': Y^2 = X^3 - 2a X^2 + (a^2 - 4b) X

with dual phi-hat : E' -> E. The descent maps

    alpha   : E(Q)/phi-hat(E'(Q))  ->  Q*/(Q*)^2,   (x, y) |-> x  (x != 0)
    alpha'  : E'(Q)/phi(E(Q))      ->  Q*/(Q*)^2,   (X, Y) |-> X

have images supported on the squarefree divisors of b and of a^2 - 4b
respectively. Silverman X.4.9 then gives, EXACTLY,

    rank E(Q) = dim_F2 (im alpha) + dim_F2 (im alpha') - 2.

Replacing each image by its Selmer group (everywhere-locally-soluble classes)
gives a rigorous UPPER bound

    rank E(Q) <= dim_F2 Sel^phi + dim_F2 Sel^phi' - 2,

because im alpha <= Sel^phi with quotient a piece of Sha. A squarefree d | b is
in Sel^phi iff the torsor

    C_d : N^2 = d M^4 + a M^2 e^2 + (b/d) e^4

has a Q_v-point for every place v (the reals and the primes dividing
2 b (a^2 - 4b)); at all other primes C_d has good reduction and a smooth point
lifts by Hensel, so finitely many places decide it.

WHAT THIS HONESTLY DELIVERS, and where the wall stays (the project's
discipline):
  - The rank upper bound is UNCONDITIONAL. When it meets experiment (f)'s lower
    bound the Mordell-Weil rank is pinned with no BSD input.
  - It bounds Sha only through the 2-isogeny: the gap upper - lower is
    dim Sha(E)[phi] + dim Sha(E')[phi-hat], a single 2-power slice. It does NOT
    prove #Sha finite (the odd part and the higher 2-power part are untouched).
    That is Detector 2, exhibited precisely rather than assumed away.
  - It needs a RATIONAL 2-isogeny, i.e. a rational 2-torsion point. The bundled
    rank-2 curves have trivial torsion, so E[2] is irreducible and this
    elementary route does not start; the general 2-descent there runs in the
    cubic field Q[x]/(2-division polynomial) and needs its class group and
    units. That missing arithmetic object is exactly what Detector 3 names.

The p-adic solubility engine here is the standard recursive lifter; it is
validated in experiment (j) against a battery of curves of independently known
rank before any conclusion is drawn from it.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt
from typing import List, Tuple


# --------------------------------------------------------------------------
# small-integer factorization (the integers here are tiny: b, a^2 - 4b are
# bounded by a few thousand for every curve we touch)
# --------------------------------------------------------------------------

def prime_factors(n: int) -> List[int]:
    """Sorted distinct prime factors of |n| (trial division)."""
    n = abs(n)
    out: List[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


def squarefree_divisors(n: int) -> List[int]:
    """All squarefree divisors of |n|, sign +1 (1 included, |n|'s radical too)."""
    ps = prime_factors(n)
    divs = [1]
    for p in ps:
        divs += [d * p for d in divs]
    return sorted(divs)


def signed_squarefree_divisors(n: int) -> List[int]:
    """Squarefree divisors of |n| with both signs: the candidate classes d."""
    pos = squarefree_divisors(n)
    return sorted(set(pos + [-d for d in pos]))


# --------------------------------------------------------------------------
# p-adic squares
# --------------------------------------------------------------------------

def valuation(n: int, p: int) -> int:
    """p-adic valuation of a nonzero integer."""
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def is_unit_square(u: int, p: int) -> bool:
    """Is the p-adic unit u (p does not divide u) a square in Z_p*?

    p odd: iff u is a quadratic residue mod p. p = 2: iff u == 1 mod 8.
    """
    if p == 2:
        return u % 8 == 1
    return pow(u % p, (p - 1) // 2, p) == 1


def is_padic_square(n: int, p: int) -> bool:
    """Is the nonzero integer n a square in Q_p*? (even valuation, unit square)."""
    if n == 0:
        return True
    v = valuation(abs(n), p)
    if v % 2 != 0:
        return False
    u = n // (p ** v)
    return is_unit_square(u, p)


# --------------------------------------------------------------------------
# local solubility of y^2 = g(x) over Q_p, g an integer-coefficient quartic
# --------------------------------------------------------------------------

def _poly_eval(coeffs: List[int], x: int) -> int:
    """Horner evaluation. coeffs are low-to-high: g(x) = sum coeffs[i] x^i."""
    acc = 0
    for c in reversed(coeffs):
        acc = acc * x + c
    return acc


def _poly_shift_scale(coeffs: List[int], r: int, p: int) -> List[int]:
    """Coefficients (low-to-high) of h(X) = g(r + p X), exact integers."""
    n = len(coeffs) - 1
    # g(r + pX) = sum_i coeffs[i] (r + pX)^i ; expand by repeated binomial.
    out = [0] * (n + 1)
    for i, ci in enumerate(coeffs):
        if ci == 0:
            continue
        # (r + pX)^i = sum_{k=0..i} C(i,k) r^{i-k} (pX)^k
        binom = 1
        for k in range(i + 1):
            term = ci * binom * (r ** (i - k)) * (p ** k)
            out[k] += term
            binom = binom * (i - k) // (k + 1)
    return out


def _content_valuation(coeffs: List[int], p: int) -> int:
    """min p-adic valuation over the nonzero coefficients (v_p of the content)."""
    vs = [valuation(abs(c), p) for c in coeffs if c != 0]
    return min(vs) if vs else 0


def _zp_has_square(coeffs: List[int], p: int, t: int, depth: int, maxdepth: int) -> bool:
    """Does there exist x in Z_p with t * g(x) a square in Q_p (or 0)?

    t in {1, p} tracks the odd part of an accumulated power of p that has been
    pulled out of g during lifting. The recursion walks the residues mod p:
    a residue with a unit value decides immediately; a residue where g vanishes
    mod p is blown up by x = r + p X, with the parity of the extracted p-power
    folded into t. Terminates by maxdepth (set from v_p of the discriminant).
    """
    if depth > maxdepth:
        # The depth bound is sized from v_p(disc); exceeding it would be a
        # soundness risk, so make it loud rather than silently wrong.
        raise RuntimeError("descent lifter exceeded its depth bound")
    for r in range(p):
        val = _poly_eval(coeffs, r)
        if val == 0:
            return True  # exact zero: N = 0 gives a Q_p point
        v = valuation(abs(val), p)
        if v == 0:
            # unit value. t * val has valuation v_p(t); a square needs v_p(t)
            # even, so t == p (an odd accumulated p-power) kills this residue.
            if t == p:
                continue
            if p != 2:
                # p odd: a unit's square class is stable across x ≡ r (mod p).
                if is_unit_square(val, p):
                    return True
                continue
            # p == 2: g(x) is odd for every x ≡ r (mod 2), and an odd 2-adic
            # number is a square iff it is 1 mod 8. The value mod 8 depends only
            # on x mod 8, so the four lifts r, r+2, r+4, r+6 are exhaustive.
            if any(_poly_eval(coeffs, xr) % 8 == 1 for xr in range(r, 8, 2)):
                return True
            continue
        # v >= 1: g(r) == 0 mod p. If r is a SIMPLE root mod p (g'(r) != 0),
        # Hensel lifts it to an exact root x* in Z_p, so (x*, 0) is a Q_p-point
        # of N^2 = g(x) and the torsor is soluble. (Following the root by
        # repeated lifting instead would never terminate.)
        deriv = [i * coeffs[i] for i in range(1, len(coeffs))]
        if _poly_eval(deriv, r) % p != 0:
            return True
        # multiple root mod p: must lift x = r + p X and pull even p-powers out.
        h = _poly_shift_scale(coeffs, r, p)
        e = _content_valuation(h, p)
        h1 = [c // (p ** e) for c in h]
        # t * h(X) = t * p^e * h1(X); the surviving odd p-part is p^((parity)).
        t_new = p if ((1 if t == p else 0) + e) % 2 == 1 else 1
        if _zp_has_square(h1, p, t_new, depth + 1, maxdepth):
            return True
    return False


def quartic_disc(d: int, a: int, c: int) -> int:
    """Discriminant of g(x) = d x^4 + a x^2 + c (used only to size maxdepth)."""
    # disc of a biquadratic d x^4 + a x^2 + c is 16 d c (a^2 - 4 d c)^2.
    return 16 * d * c * (a * a - 4 * d * c) ** 2


def qp_soluble(d: int, a: int, c: int, p: int) -> bool:
    """Does C : N^2 = d M^4 + a M^2 e^2 + c e^4 have a Q_p-point?

    Equivalently y^2 = g(u), g(u) = d u^4 + a u^2 + c, over Q_p, including the
    points at u = infinity (leading coefficient d must be a Q_p-square).
    """
    if is_padic_square(d, p):
        return True  # points at infinity (e = 0)
    if is_padic_square(c, p):
        return True  # u = 0
    disc = quartic_disc(d, a, c)
    md = 2 * valuation(abs(disc) if disc != 0 else 1, p) + 10
    g = [c, 0, a, 0, d]            # low-to-high: c + a x^2 + d x^4
    g_rev = [d, 0, a, 0, c]        # reversed: covers u in Q_p \ Z_p
    return (_zp_has_square(g, p, 1, 0, md)
            or _zp_has_square(g_rev, p, 1, 0, md))


def real_soluble(d: int, a: int, c: int) -> bool:
    """Does C : N^2 = d M^4 + a M^2 e^2 + c e^4 have a real point != 0?

    Solvable over R iff the form d s^2 + a s + c is >= 0 for some s = M^2/e^2 >= 0,
    or d > 0 (the e = 0 point), or c > 0 (the M = 0 point).
    """
    if d > 0 or c > 0:
        return True
    if d == 0:
        return a > 0 or c >= 0
    # d < 0: downward parabola in s; max at s* = -a/(2d), value c - a^2/(4d)
    if a >= 0:
        # vertex value >= 0  <=>  4 d c <= a^2  (multiply by 4d < 0 flips the sign)
        return 4 * d * c <= a * a
    return c >= 0


# --------------------------------------------------------------------------
# the Selmer group of the 2-isogeny and the rank bound
# --------------------------------------------------------------------------

def bad_primes(b: int, bprime: int) -> List[int]:
    """Primes that can obstruct C_d: those dividing 2 b (a^2 - 4b)."""
    ps = set(prime_factors(2 * b * bprime))
    ps.update([2, 3])  # always test 2 and 3 (cheap; safe at small good primes)
    return sorted(ps)


def selmer_phi(a: int, b: int) -> List[int]:
    """Sel^phi: squarefree d | b (both signs) with C_d soluble at every place.

    C_d : N^2 = d M^4 + a M^2 e^2 + (b/d) e^4.
    Returns the list of surviving classes d (a subgroup of Q*/(Q*)^2 of size a
    power of 2; 1 and b always survive, being images of O and (0,0)).
    """
    bprime = a * a - 4 * b
    if b == 0 or bprime == 0:
        raise ValueError(
            f"y^2 = x^3 + {a}x^2 + {b}x is singular (b={b}, a^2-4b={bprime}); "
            "the 2-isogeny descent needs a nonsingular curve with a rational "
            "2-torsion point at the origin"
        )
    primes = bad_primes(b, bprime)
    survivors: List[int] = []
    for d in signed_squarefree_divisors(b):
        c = b // d  # exact: d | b
        if not real_soluble(d, a, c):
            continue
        if all(qp_soluble(d, a, c, p) for p in primes):
            survivors.append(d)
    return survivors


def isogenous_curve(a: int, b: int) -> Tuple[int, int]:
    """The 2-isogenous curve E': Y^2 = X^3 + a' X^2 + b' X, (a', b') = (-2a, a^2-4b)."""
    return (-2 * a, a * a - 4 * b)


def descent_rank_bound(a: int, b: int) -> dict:
    """Full 2-isogeny descent on E: y^2 = x^3 + a x^2 + b x.

    Returns a dict with the two Selmer groups, their F2-dimensions, and the
    rigorous rank upper bound rank E(Q) <= dim Sel^phi + dim Sel^phi' - 2.
    """
    ap, bp = isogenous_curve(a, b)
    sel = selmer_phi(a, b)
    sel_p = selmer_phi(ap, bp)
    dim = (len(sel) - 1).bit_length() if len(sel) else 0
    dim_p = (len(sel_p) - 1).bit_length() if len(sel_p) else 0
    # |Sel| is a power of 2; dim = log2 |Sel|.
    dim = _log2_exact(len(sel))
    dim_p = _log2_exact(len(sel_p))
    return {
        "a": a, "b": b, "a_prime": ap, "b_prime": bp,
        "selmer_phi": sel, "selmer_phi_prime": sel_p,
        "dim_phi": dim, "dim_phi_prime": dim_p,
        "rank_upper_bound": dim + dim_p - 2,
    }


def rational_two_torsion_x(a_invariants: List[int]) -> List[Fraction]:
    """Rational x-coordinates of the 2-torsion of a long Weierstrass model.

    The 2-torsion x-coordinates are the rational roots of
        psi(x) = 4 x^3 + b2 x^2 + 2 b4 x + b6,
    b2 = a1^2 + 4 a2, b4 = 2 a4 + a1 a3, b6 = a3^2 + 4 a6 (found by the rational
    root theorem: a root num/den in lowest terms has num | b6, den | 4).
    An empty list means E[2] is irreducible over Q: no rational 2-isogeny, so
    the elementary descent here does not apply.
    """
    a1, a2, a3, a4, a6 = a_invariants
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    coeffs = [b6, 2 * b4, b2, 4]  # psi low-to-high

    def divisors(m: int) -> List[int]:
        m = abs(m)
        if m == 0:
            return [0]
        out = []
        i = 1
        while i * i <= m:
            if m % i == 0:
                out += [i, m // i]
            i += 1
        return sorted(set(out))

    if b6 == 0:
        roots = {Fraction(0)}
    else:
        roots = set()
    nums = divisors(b6) if b6 != 0 else [0]
    for num in nums + [-n for n in nums]:
        for den in [1, 2, 4]:
            x = Fraction(num, den)
            if _poly_eval([Fraction(c) for c in coeffs], x) == 0:
                roots.add(x)
    return sorted(roots)


def to_2torsion_form(a_invariants: List[int]):
    """Integer (a, b) with E isomorphic to y^2 = x^3 + a x^2 + b x, or None.

    Returns None exactly when E has no rational 2-torsion point (E[2]
    irreducible), the case where 2-isogeny descent cannot start. Otherwise the
    model is built by completing the square, translating a rational 2-torsion
    x-coordinate to the origin, and scaling x -> x/u^2, y -> y/u^3 to clear
    denominators. The descent rank is an isomorphism invariant, so the integer
    model returned has the same Mordell-Weil rank as the input.
    """
    xs = rational_two_torsion_x(a_invariants)
    if not xs:
        return None
    a1, a2, a3, a4, a6 = (Fraction(c) for c in a_invariants)
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    x0 = xs[0]
    # completed-square cubic f(x) = x^3 + (b2/4) x^2 + (b4/2) x + (b6/4); x0 is a
    # root, so f(x + x0) = x^3 + a' x^2 + b' x.
    a_prime = 3 * x0 + b2 / 4
    b_prime = 3 * x0 * x0 + (b2 / 2) * x0 + b4 / 2  # = f'(x0)
    u = 1
    for fr in (a_prime, b_prime):
        u = u * fr.denominator // _gcd(u, fr.denominator)
    a_int = a_prime * u * u
    b_int = b_prime * u ** 4
    assert a_int.denominator == 1 and b_int.denominator == 1
    return (int(a_int), int(b_int))


def _gcd(x: int, y: int) -> int:
    while y:
        x, y = y, x % y
    return abs(x)


def _log2_exact(n: int) -> int:
    """log2 of a positive power of two; raise if n is not a power of two."""
    if n <= 0 or (n & (n - 1)) != 0:
        raise ValueError(f"Selmer group size {n} is not a power of two")
    return n.bit_length() - 1
