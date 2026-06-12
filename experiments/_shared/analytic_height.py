"""High-precision canonical heights via the Weierstrass sigma function.

WHY this module exists: the doubling-limit height in rational_points.py is
exact-arithmetic-honest but converges like C / 4^k, so nine doublings give
only ~1e-5. A numerical Gross-Zagier check needs canonical heights to the
working precision (20+ digits). The classical local decomposition delivers
that:

    hhat(P) = 2 G(z) + sum_p max(0, -v_p(x(P))) log p,

in the LMFDB normalization (hhat = lim h(x(2^k P)) / 4^k, twice Silverman's),
where the non-archimedean sum is just log(denominator of x(P)) on the minimal
model, PROVIDED every bad prime has trivial component group (v_p(Delta) = 1
suffices; this module asserts it). G(z) = -log |sigma-hat(z)| is the
archimedean local height at the elliptic logarithm z of P, with sigma-hat
the quasi-period-corrected sigma, exactly lattice-periodic by the Legendre
relation. Everything is built from Jacobi theta functions on tau = w2 / w1,
which mpmath evaluates to full precision for either lattice shape
(rectangular Delta > 0 or rhombic Delta < 0).

NORMALIZATION NOTE: textbook statements of the local decomposition carry a
-(1/6) log |Delta| at the archimedean place. With sigma built from theta
functions normalized by theta1'(0) as below, that discriminant term is
already inside G (the eta-correction and the theta1'(0)^... scaling absorb
it): empirically, 2 G + log den matches the exact doubling-limit height on
37a1 / 43a1 / 53a1 generators to the doubling limit's own 1e-5 accuracy,
and hhat(2P) = 4 hhat(P) holds to ~20 digits, while adding any multiple of
log |Delta| breaks quadraticity by exactly 3x that multiple. The constant is
therefore pinned by the computation itself, not by a convention citation.

CONVENTION SAFETY: theta/sigma/quasi-period conventions are notorious, so the
SigmaLattice constructor self-checks at runtime: sigma(z) ~ z for small z,
wp(w1/2) hits a 2-torsion x-coordinate, and G is verified periodic in both
lattice directions. A convention slip cannot pass silently. Callers should
additionally check hhat against the doubling-limit height once per curve
(1e-4 agreement) and the quadraticity hhat(2P) = 4 hhat(P) at full precision.
"""

from __future__ import annotations

import mpmath as mp

from experiments._shared.period_lattice import period_lattice_any


def curve_discriminant(E) -> int:
    """The discriminant of the (minimal) Weierstrass model, exact integer."""
    a1, a2, a3, a4, a6 = E.a_invariants
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    return -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6


class SigmaLattice:
    """Period lattice of E with sigma / wp / local-height machinery.

    Precomputes the lattice (any discriminant sign), the nome, the
    quasi-periods eta1 = zeta(w1/2), eta2 = zeta(w2/2), and the covolume.
    Provides wp(z) (so x(z) = wp(z) - b2/12 works on rhombic lattices where
    the sn-based x_from_z cannot), reduce(z) to the fundamental cell, and
    G(z), the lattice-periodic archimedean local height.
    """

    def __init__(self, E):
        self.E = E
        a1, a2, a3, a4, a6 = E.a_invariants
        self.b2 = mp.mpf(a1 * a1 + 4 * a2)
        self.disc = curve_discriminant(E)
        self.w1, self.w2 = period_lattice_any(E)
        if mp.im(self.w2 / self.w1) < 0:
            self.w2 = -self.w2
        self.tau = self.w2 / self.w1
        self.q = mp.exp(1j * mp.pi * self.tau)
        self._th1p0 = mp.jtheta(1, 0, self.q, 1)
        th1ppp0 = mp.jtheta(1, 0, self.q, 3)
        self.eta1 = -mp.pi ** 2 * th1ppp0 / (6 * self.w1 * self._th1p0)
        # Legendre relation eta1 w2 - eta2 w1 = i pi (full-period form)
        self.eta2 = (self.eta1 * self.w2 - 1j * mp.pi) / self.w1
        self.vol = abs(mp.im(mp.conj(self.w1) * self.w2))
        self._self_check()

    # ---- core special functions -------------------------------------

    def sigma(self, z):
        v = mp.pi * z / self.w1
        return (self.w1 / mp.pi) * mp.exp(self.eta1 * z * z / self.w1) * \
            mp.jtheta(1, v, self.q) / self._th1p0

    def wp(self, z):
        """Weierstrass p-function: wp = -(d/dz)^2 log sigma."""
        v = mp.pi * z / self.w1
        t0 = mp.jtheta(1, v, self.q)
        t1 = mp.jtheta(1, v, self.q, 1)
        t2 = mp.jtheta(1, v, self.q, 2)
        return -2 * self.eta1 / self.w1 - (mp.pi / self.w1) ** 2 * \
            (t2 / t0 - (t1 / t0) ** 2)

    def x_of_z(self, z):
        """x-coordinate on the Weierstrass model: x = wp(z) - b2/12."""
        return self.wp(z) - self.b2 / 12

    # ---- lattice bookkeeping ----------------------------------------

    def coords(self, z):
        """Real (a, b) with z = a w1 + b w2 (works for any lattice shape)."""
        x1, y1 = mp.re(self.w1), mp.im(self.w1)
        x2, y2 = mp.re(self.w2), mp.im(self.w2)
        det = x1 * y2 - x2 * y1
        a = (mp.re(z) * y2 - mp.im(z) * x2) / det
        b = (x1 * mp.im(z) - y1 * mp.re(z)) / det
        return a, b

    def reduce(self, z):
        """Lattice coordinates of z, each reduced to [-1/2, 1/2)."""
        a, b = self.coords(z)
        return a - mp.nint(a), b - mp.nint(b)

    # ---- archimedean local height -----------------------------------

    def G(self, z):
        """-log |sigma-hat(z)|, exactly Lambda-periodic (Legendre relation).

        With z = a w1 + b w2, the periodic combination is
        G = -log|sigma(z)| + a^2 Re(eta1 w1) + 2ab Re(eta1 w2)
            + b^2 Re(eta2 w2).
        """
        a, b = self.coords(z)
        return -mp.log(abs(self.sigma(z))) \
            + a * a * mp.re(self.eta1 * self.w1) \
            + 2 * a * b * mp.re(self.eta1 * self.w2) \
            + b * b * mp.re(self.eta2 * self.w2)

    # ---- construction-time convention checks ------------------------

    def _self_check(self):
        tol = mp.mpf(10) ** (-(mp.mp.dps - 10))
        # sigma(z) ~ z near the origin
        z0 = self.w1 / mp.mpf(10 ** 4)
        assert abs(self.sigma(z0) / z0 - 1) < mp.mpf("1e-10"), \
            "sigma normalization broken"
        # wp(w1/2) - b2/12 must be a 2-torsion x-coordinate: f(x) = 0
        x2t = self.x_of_z(self.w1 / 2)
        a1, a2, a3, a4, a6 = [mp.mpf(a) for a in self.E.a_invariants]
        b2, b4 = self.b2, 2 * a4 + a1 * a3
        b6 = a3 * a3 + 4 * a6
        f = 4 * x2t ** 3 + b2 * x2t ** 2 + 2 * b4 * x2t + b6
        scale = max(1, abs(x2t)) ** 3
        assert abs(f) / scale < mp.mpf(10) ** (-(mp.mp.dps - 12)), \
            f"wp(w1/2) is not 2-torsion on {self.E.label}: f = {f}"
        # G must be periodic in both lattice directions
        zt = mp.mpf("0.31") * self.w1 + mp.mpf("0.17") * self.w2
        for w in (self.w1, self.w2):
            assert abs(self.G(zt + w) - self.G(zt)) < tol * 100, \
                f"G not periodic along {w} on {self.E.label}"


def elliptic_log(E, P, L: SigmaLattice, samples: int = 400):
    """Elliptic logarithm of a real rational point, determined up to sign.

    Scans the real locus for a bracket of x(z) = x(P) and bisects: the
    component through O is z in (0, w1), and for Delta > 0 the egg is
    z in w2/2 + (0, w1). The returned z may correspond to P or -P; canonical
    heights are even and Gram matrices here are built from heights of EXACT
    point sums, so the sign ambiguity is harmless to every caller in this
    codebase.
    """
    x0 = mp.mpf(P[0].numerator) / P[0].denominator
    shifts = [mp.mpf(0)]
    if L.disc > 0:
        shifts.append(L.w2 / 2)
    for shift in shifts:
        def f(t):
            return mp.re(L.x_of_z(t + shift)) - x0

        ts = [L.w1 * k / samples for k in range(1, samples)]
        prev_t, prev_v = ts[0], f(ts[0])
        for t in ts[1:]:
            v = f(t)
            if mp.sign(v) != mp.sign(prev_v) and prev_v != 0:
                root = mp.findroot(f, (prev_t, t), solver="bisect",
                                   maxsteps=200)
                return root + shift
            prev_t, prev_v = t, v
    raise ValueError(f"elliptic log not found for x = {x0} on {E.label}")


def canonical_height_sigma(E, P, z, L: SigmaLattice):
    """hhat(P) to working precision, LMFDB normalization.

    P is the exact rational point (Fractions, minimal model), z its elliptic
    logarithm (any lattice representative; G is periodic and even, so the
    sign/representative ambiguity of z is harmless). Requires trivial
    component groups at the bad primes (v_p(Delta) = 1), which makes the
    non-archimedean part exactly log(den x(P)).
    """
    disc = abs(L.disc)
    N = E.conductor
    p, m = 2, N
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            assert disc % (p ** 2) != 0, \
                f"v_{p}(Delta) > 1 on {E.label}: component-group correction needed"
        p += 1
    if m > 1:
        assert disc % (m ** 2) != 0, \
            f"v_{m}(Delta) > 1 on {E.label}: component-group correction needed"
    return 2 * L.G(z) + mp.log(P[0].denominator)
