"""Exact rational-point arithmetic and Neron-Tate canonical heights.

This module supplies the MORDELL-WEIL side of BSD, the side the L-function
machinery in elliptic_curve.py cannot see. Everything here is exact rational
arithmetic (fractions.Fraction), so a statement like "these two points are
independent" is backed by an honest computation, not floating-point luck.

What it provides:

  - the group law on a long Weierstrass model E(Q), chord-and-tangent, exact;
  - a naive search for rational points of small height (x = m/e^2 in lowest
    terms, discriminant-is-a-square test, all exact);
  - the Neron-Tate canonical height via the doubling limit
        hhat(P) = lim_k  h(x(2^k P)) / 4^k,
    where h is the naive logarithmic height of the x-coordinate. The exact
    Fraction coordinates of 2^k P make the limit honest: the error after k
    doublings is bounded by C / 4^k for a curve constant C of a few units,
    so k = 9 gives ~1e-5 absolute accuracy;
  - the Neron-Tate height pairing <P, Q> = (hhat(P+Q) - hhat(P) - hhat(Q))/2
    and Gram determinants, i.e. regulators of finite-index subgroups.

NORMALIZATION: hhat here is the LMFDB / Cremona normalization, the one in
which the regulator of 37a1's generator (0, 0) is 0.0511114082. This is
lim h(x(nP))/n^2 WITHOUT the extra factor 1/2 some textbooks use (Silverman
AEC VIII.9 defines the half of this). Experiments calibrate against the
bundled regulator and assert the match, so a normalization slip cannot pass
silently.

WHY this matters for the program: producing r independent points is the HALF
of the rank-r BSD object that is constructible today (a nonzero Gram
determinant of canonical heights certifies independence, hence
rank E(Q) >= r, unconditionally up to numerical error). The OTHER half, the
upper bound rank <= r, is the Selmer/Sha side where every known method stops
at analytic rank <= 1. The experiments use this module to make that asymmetry
concrete.
"""

from __future__ import annotations

import math
from fractions import Fraction
from math import isqrt
from typing import List, Optional, Tuple

Point = Optional[Tuple[Fraction, Fraction]]  # None is the point at infinity


def _ainvs(E) -> List[Fraction]:
    return [Fraction(a) for a in E.a_invariants]


def on_curve(E, P: Point) -> bool:
    """Exact check of y^2 + a1 x y + a3 y = x^3 + a2 x^2 + a4 x + a6."""
    if P is None:
        return True
    a1, a2, a3, a4, a6 = _ainvs(E)
    x, y = P
    return y * y + a1 * x * y + a3 * y == x ** 3 + a2 * x * x + a4 * x + a6


def negate(E, P: Point) -> Point:
    if P is None:
        return None
    a1, _, a3, _, _ = _ainvs(E)
    x, y = P
    return (x, -y - a1 * x - a3)


def add(E, P: Point, Q: Point) -> Point:
    """Chord-and-tangent addition on the long Weierstrass model, exact."""
    if P is None:
        return Q
    if Q is None:
        return P
    a1, a2, a3, a4, _ = _ainvs(E)
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y2 == -y1 - a1 * x1 - a3:
        return None  # Q = -P
    if P == Q:
        lam = (3 * x1 * x1 + 2 * a2 * x1 + a4 - a1 * y1) / (2 * y1 + a1 * x1 + a3)
    else:
        lam = (y2 - y1) / (x2 - x1)
    nu = y1 - lam * x1
    x3 = lam * lam + a1 * lam - a2 - x1 - x2
    y3 = -(lam + a1) * x3 - nu - a3
    return (x3, y3)


def multiply(E, n: int, P: Point) -> Point:
    """[n]P by double-and-add, exact."""
    if n < 0:
        return multiply(E, -n, negate(E, P))
    R: Point = None
    Q = P
    while n:
        if n & 1:
            R = add(E, R, Q)
        Q = add(E, Q, Q)
        n >>= 1
    return R


def lift_x(E, x: Fraction) -> Point:
    """The point (x, y) on E with this exact x-coordinate, or None.

    Solves the y-quadratic y^2 + (a1 x + a3) y - f(x) = 0 exactly: its
    discriminant must be a rational square. Returns the root with the
    + square root; the other point is the negative.
    """
    a1, a2, a3, a4, a6 = _ainvs(E)
    b = a1 * x + a3
    f = x ** 3 + a2 * x * x + a4 * x + a6
    disc = b * b + 4 * f
    if disc < 0:
        return None
    # disc = n/d in lowest terms is a rational square iff n*d is a square
    nd = disc.numerator * disc.denominator
    r = isqrt(nd)
    if r * r != nd:
        return None
    y = (-b + Fraction(r, disc.denominator)) / 2
    return (x, y)


def search_points(E, x_bound: int = 40, denom_bound: int = 4) -> List[Point]:
    """All points with x = m/e^2, |x| <= x_bound, e <= denom_bound, exact.

    On an integral Weierstrass model the denominator of x is a perfect
    square e^2, so this enumeration is the honest small-height search.
    One point per x (the negative is implicit).
    """
    pts: List[Point] = []
    seen = set()
    for e in range(1, denom_bound + 1):
        e2 = e * e
        for m in range(-x_bound * e2, x_bound * e2 + 1):
            if e > 1 and math.gcd(m, e) != 1:
                continue
            x = Fraction(m, e2)
            if x in seen:
                continue
            P = lift_x(E, x)
            if P is not None:
                seen.add(x)
                pts.append(P)
    return pts


def naive_x_height(P: Point) -> float:
    """h(P) = log max(|num x|, den x), the naive logarithmic height."""
    if P is None:
        return 0.0
    x = P[0]
    return math.log(max(abs(x.numerator), x.denominator, 1))


def canonical_height(E, P: Point, doublings: int = 9) -> float:
    """Neron-Tate height, LMFDB normalization: lim h(x(2^k P)) / 4^k.

    Exact doubling keeps the limit honest; the truncation error is
    O(C / 4^doublings) with C a few units, so the default gives ~1e-5.
    Torsion points (some doubling hits O, or the limit is 0) return 0.
    """
    if P is None:
        return 0.0
    Q = P
    for _ in range(doublings):
        Q = add(E, Q, Q)
        if Q is None:
            return 0.0  # torsion of 2-power order
    return naive_x_height(Q) / float(4 ** doublings)


def neron_tate_pairing(E, P: Point, Q: Point, doublings: int = 9) -> float:
    """<P, Q> = (hhat(P+Q) - hhat(P) - hhat(Q)) / 2, the height pairing."""
    return (
        canonical_height(E, add(E, P, Q), doublings)
        - canonical_height(E, P, doublings)
        - canonical_height(E, Q, doublings)
    ) / 2.0


def gram_matrix(E, points: List[Point], doublings: int = 9) -> List[List[float]]:
    """Gram matrix of the Neron-Tate pairing on the given points."""
    n = len(points)
    h = [canonical_height(E, P, doublings) for P in points]
    M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        M[i][i] = h[i]
        for j in range(i + 1, n):
            hij = (
                canonical_height(E, add(E, points[i], points[j]), doublings)
                - h[i]
                - h[j]
            ) / 2.0
            M[i][j] = M[j][i] = hij
    return M


def det(M: List[List[float]]) -> float:
    """Determinant for the small (n <= 3) Gram matrices used here."""
    n = len(M)
    if n == 0:
        return 1.0
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    if n == 3:
        return (
            M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])
        )
    raise ValueError("det implemented for n <= 3 only")
