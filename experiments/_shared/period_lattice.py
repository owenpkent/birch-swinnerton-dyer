"""Period lattice and the Weierstrass parametrization C/Lambda -> E(C).

For a curve with positive discriminant (three real 2-torsion x-coordinates,
two real components, which covers 37a1, 389a1 and 5077a1, the control chain
of the Heegner experiment) the period lattice is RECTANGULAR:

    Lambda = Z w1 + Z w2,   w1 real,  w2 purely imaginary,

and both periods come from the arithmetic-geometric mean of root differences
(Gauss). With r1 > r2 > r3 the roots of the completed-square cubic

    (2y + a1 x + a3)^2 = 4x^3 + b2 x^2 + 2 b4 x + b6,

the periods are

    w1 = pi / AGM(sqrt(r1 - r3), sqrt(r1 - r2)),
    w2 = i pi / AGM(sqrt(r1 - r3), sqrt(r2 - r3)),

and the LMFDB real period (integral over BOTH real components) is 2 w1,
which the experiments assert against the bundled value.

The inverse map z -> (x, y) uses the Jacobi-sn form of the Weierstrass
p-function:

    x(z) = r3 + (r1 - r3) / sn(z sqrt(r1 - r3), m)^2,
    m = (r2 - r3)/(r1 - r3),

valid for complex z, so a point handed to us as a lattice element (e.g. by
the modular parametrization phi(tau) = sum a_n/n q^n) can be converted back
to an x-coordinate and tested for rationality. That round trip is what lets
the Heegner experiment certify "the machine produced an actual rational
point" or "the machine produced torsion".

The rectangular helpers (two_torsion_roots, period_lattice, x_from_z,
reduce_mod_lattice) cover Delta > 0 only, which is all the original Heegner
experiment needed. period_lattice_any extends to Delta < 0 (one real
component, RHOMBIC lattice): there the real period w1 and the imaginary
height c of the lattice come from direct numerical integration of the Neron
differential dx / (2y + a1 x + a3), whose square is f(x) = 4x^3 + b2 x^2 +
2 b4 x + b6:

    w1 = 2 int_{e1}^{inf} dx / sqrt(f(x))        (the single real circle),
    c  = 2 int_{-inf}^{e1} dx / sqrt(-f(x)),     w2 = (w1 + i c) / 2,

with e1 the unique real root of f. The substitution x = e1 +- t^2 removes
the endpoint singularity, so mpmath's quadrature delivers full precision.
Callers that need x(z) on a rhombic lattice should use the theta-function
Weierstrass machinery in analytic_height.py (x_from_z here is sn-based and
rectangular-only).
"""

from __future__ import annotations

from typing import Tuple

import mpmath as mp


def two_torsion_roots(E) -> Tuple[mp.mpf, mp.mpf, mp.mpf]:
    """Roots r1 > r2 > r3 of 4x^3 + b2 x^2 + 2 b4 x + b6 (must be real)."""
    a1, a2, a3, a4, a6 = [mp.mpf(a) for a in E.a_invariants]
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    roots = mp.polyroots([4, b2, 2 * b4, b6])
    tol = mp.mpf(10) ** (-(mp.mp.dps - 8))
    if any(abs(mp.im(r)) > tol for r in roots):
        raise ValueError(
            f"{E.label}: discriminant < 0 (one real component); "
            "this helper covers the rectangular-lattice case only"
        )
    r = sorted((mp.re(z) for z in roots), reverse=True)
    return r[0], r[1], r[2]


def period_lattice(E):
    """(w1, w2, (r1, r2, r3)): real and imaginary periods plus the roots."""
    r1, r2, r3 = two_torsion_roots(E)
    w1 = mp.pi / mp.agm(mp.sqrt(r1 - r3), mp.sqrt(r1 - r2))
    w2 = mp.mpc(0, 1) * mp.pi / mp.agm(mp.sqrt(r1 - r3), mp.sqrt(r2 - r3))
    return w1, w2, (r1, r2, r3)


def period_lattice_any(E):
    """Lattice generators (w1, w2) for either sign of the discriminant.

    Delta > 0: delegates to the rectangular AGM code (w1 real, w2 imaginary;
    the LMFDB real period is 2 w1). Delta < 0: rhombic, w1 IS the LMFDB real
    period and w2 = (w1 + i c)/2 with c the imaginary cycle integral. In both
    cases Im(w2/w1) > 0 and the covolume is w1 * Im(w2).
    """
    a1, a2, a3, a4, a6 = [mp.mpf(a) for a in E.a_invariants]
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    roots = mp.polyroots([4, b2, 2 * b4, b6])
    tol = mp.mpf(10) ** (-(mp.mp.dps - 8))
    if all(abs(mp.im(r)) < tol for r in roots):
        w1, w2, _ = period_lattice(E)
        return w1, w2
    e1 = next(mp.re(r) for r in roots if abs(mp.im(r)) < tol)
    # f(x) = (x - e1) g(x) with g a positive-definite real quadratic
    c1 = b2 + 4 * e1
    d1 = 2 * b4 + e1 * c1

    def g(x):
        return 4 * x * x + c1 * x + d1

    def half_period(sign):
        # breakpoints where g(e1 + sign t^2) bottoms out (vertex of g),
        # otherwise tanh-sinh quietly loses digits there (571a1 did)
        points = [mp.mpf(0)]
        x_vertex = -c1 / 8
        if sign * (x_vertex - e1) > 0:
            t_peak = mp.sqrt(sign * (x_vertex - e1))
            points += [t_peak, 2 * t_peak + 1]
        points.append(mp.inf)
        return 4 * mp.quad(lambda t: 1 / mp.sqrt(g(e1 + sign * t * t)),
                           points, maxdegree=9)

    w1 = half_period(+1)
    c = half_period(-1)
    return w1, (w1 + mp.mpc(0, 1) * c) / 2


def x_from_z(z, r1, r2, r3):
    """x-coordinate of the point with elliptic logarithm z (complex ok)."""
    m = (r2 - r3) / (r1 - r3)
    u = z * mp.sqrt(r1 - r3)
    sn = mp.ellipfun("sn", u, m=m)
    return r3 + (r1 - r3) / (sn * sn)


def reduce_mod_lattice(z, w1, w2) -> Tuple[mp.mpf, mp.mpf]:
    """Lattice coordinates (alpha, beta) of z, each reduced to [-1/2, 1/2).

    z = alpha w1 + beta w2 with the rectangular basis, so alpha is the real
    part over w1 and beta the imaginary part over |w2|. A torsion point of
    order n has alpha, beta in (1/n) Z; the zero point has both ~ 0.
    """
    alpha = mp.re(z) / w1
    beta = mp.im(z) / mp.im(w2)
    return alpha - mp.nint(alpha), beta - mp.nint(beta)
