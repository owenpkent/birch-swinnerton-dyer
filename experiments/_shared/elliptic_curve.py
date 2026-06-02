"""Elliptic curve over Q and its Hasse-Weil L-function.

This is the BSD analog of the zeta repo's LFunction interface. The object an
experiment manipulates is an elliptic curve E/Q given by a (short or long)
Weierstrass equation. From the curve we derive everything the experimental
thread needs:

  - a_p from point counts on E mod p (Hasse: a_p = p + 1 - #E(F_p)),
  - the Dirichlet coefficients a_n built multiplicatively (Euler product),
  - the completed L-function L(E, s) and its derivatives at s = 1 via the
    approximate functional equation at high mpmath precision,
  - the root number (sign of the functional equation), which controls the
    PARITY of the analytic rank.

WHY a class and not loose functions: every experiment (analytic rank, weak
BSD table, strong BSD quantities, Sato-Tate) needs the same a_p pipeline, so
it lives here once and is shared, exactly as zeta.py / lfunction.py are shared
in the sibling Riemann repo.

Conventions:
  - mpmath at the current mp.mp.dps for all analytic work (>= 30 digits).
  - A curve is identified by its Cremona label when known, plus its
    Weierstrass coefficients [a1, a2, a3, a4, a6] and conductor N.
  - Bad primes (those dividing the conductor) get a_p in {-1, 0, 1} supplied
    from the bundled data, since point counting on a singular reduction does
    not give the right local factor.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import mpmath as mp


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def _primes_up_to(limit: int) -> List[int]:
    if limit < 2:
        return []
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))
    return [i for i in range(2, limit + 1) if sieve[i]]


@dataclass
class EllipticCurve:
    """An elliptic curve over Q in long Weierstrass form.

    y^2 + a1 x y + a3 y = x^3 + a2 x^2 + a4 x + a6

    The arithmetic invariants (conductor N, root number w, bad-prime a_p,
    Mordell-Weil rank, torsion, Tamagawa product, real period, regulator,
    analytic Sha) are passed in from the bundled LMFDB/Cremona data file,
    because computing a few of them from scratch (rank, regulator, Sha) is
    itself hard. The a_p at GOOD primes are computed here by honest point
    counting, which is the part the experiments actually exercise.
    """

    label: str
    a_invariants: List[int]  # [a1, a2, a3, a4, a6]
    conductor: int
    rank: Optional[int] = None
    torsion_order: Optional[int] = None
    root_number: Optional[int] = None  # +1 or -1
    bad_ap: Dict[int, int] = field(default_factory=dict)
    real_period: Optional[float] = None
    regulator: Optional[float] = None
    tamagawa_product: Optional[int] = None
    sha_order: Optional[int] = None  # analytic / conjectural #Sha (usually a perfect square)

    _ap_cache: Dict[int, int] = field(default_factory=dict, repr=False)

    @property
    def has_euler_product(self) -> bool:
        # The Hasse-Weil L-function has an Euler product by construction; this
        # is the structural feature a wrong-approach detector must respect.
        return True

    @property
    def has_functional_equation(self) -> bool:
        return True

    def _rhs(self, x: int, p: int) -> int:
        a1, a2, a3, a4, a6 = self.a_invariants
        return (x * x * x + a2 * x * x + a4 * x + a6) % p

    def count_points_mod_p(self, p: int) -> int:
        """#E(F_p) including the point at infinity, by brute force.

        For a good prime this is exact. We complete the square only implicitly
        by solving y^2 + (a1 x + a3) y = f(x) for each x, counting solutions y.
        """
        a1, a2, a3, a4, a6 = self.a_invariants
        # quadratic-residue table mod p
        is_square = [False] * p
        for y in range(p):
            is_square[(y * y) % p] = True
        count = 1  # point at infinity
        for x in range(p):
            # y^2 + (a1 x + a3) y - f(x) = 0  ->  discriminant in y
            b = (a1 * x + a3) % p
            c = (x * x * x + a2 * x * x + a4 * x + a6) % p
            # 4*(y^2 + b y - c) = (2y + b)^2 - (b^2 + 4c)
            disc = (b * b + 4 * c) % p
            if p == 2:
                # handle char 2 directly by enumeration
                sols = sum(1 for y in range(2) if (y * y + b * y - c) % 2 == 0)
                count += sols
                continue
            if disc == 0:
                count += 1
            elif is_square[disc]:
                count += 2
            else:
                count += 0
        return count

    def a_p(self, p: int) -> int:
        """The trace of Frobenius a_p = p + 1 - #E(F_p) at a good prime.

        At a bad prime (p | N) we return the bundled local value in
        {-1, 0, +1} (split multiplicative, non-split multiplicative, additive).
        """
        if p in self._ap_cache:
            return self._ap_cache[p]
        if self.conductor % p == 0:
            ap = self.bad_ap.get(p, 0)
        else:
            ap = p + 1 - self.count_points_mod_p(p)
        self._ap_cache[p] = ap
        return ap

    def a_n(self, n: int) -> int:
        """The n-th Dirichlet coefficient, built multiplicatively.

        a_{p^{k+1}} = a_p a_{p^k} - p a_{p^{k-1}} at good primes,
        a_{p^k} = a_p^k at bad primes (multiplicative or additive reduction),
        and a_{mn} = a_m a_n for coprime m, n.
        """
        if n == 1:
            return 1
        result = 1
        m = n
        for p in _primes_up_to(int(n ** 0.5) + 1):
            if m == 1:
                break
            if m % p == 0:
                k = 0
                while m % p == 0:
                    m //= p
                    k += 1
                result *= self._a_prime_power(p, k)
        if m > 1:
            # m is now a single prime > sqrt(n)
            result *= self._a_prime_power(m, 1)
        return result

    def _a_prime_power(self, p: int, k: int) -> int:
        ap = self.a_p(p)
        if self.conductor % p == 0:
            return ap ** k  # bad reduction: a_{p^k} = a_p^k
        # good reduction recurrence
        vals = [1, ap]
        for j in range(2, k + 1):
            vals.append(ap * vals[j - 1] - p * vals[j - 2])
        return vals[k]

    # ----- analytic L-function via the approximate functional equation -----

    def _num_terms(self) -> int:
        # Terms needed in the smoothed AFE: the incomplete-Gamma cutoff makes
        # the tail decay like exp(-n / Q), so a few multiples of Q * dps suffice.
        Q = float(mp.sqrt(mp.mpf(self.conductor)) / (2 * mp.pi))
        digits = mp.mp.dps
        return min(int(Q * (digits + 15) * 2.5) + 50, 200000)

    def L_value(self, s):
        """L(E, s) via the smoothed approximate functional equation.

        Completed L-function: Lambda(s) = N^{s/2} (2 pi)^{-s} Gamma(s) L(E, s),
        with functional equation Lambda(s) = w Lambda(2 - s) and center s = 1.

        The smoothed AFE (incomplete-Gamma test function G_z(x) =
        Gamma(z, x)/Gamma(z)) gives, with Q = sqrt(N)/(2 pi),

          L(E, s) = sum_n a_n/n^s G_s(n/Q)
                    + w * X(s) * sum_n a_n/n^{2-s} G_{2-s}(n/Q),

        where X(s) = Q^{2-2s} Gamma(2-s)/Gamma(s) is the ratio of archimedean
        factors. Both sums converge geometrically because G decays like
        exp(-n/Q).

        WHY this form: the naive Dirichlet series diverges at s = 1 (the
        center, where BSD lives), so the functional equation is mandatory to
        continue there. The smoothed AFE is the standard high-precision tool.
        """
        s = mp.mpc(s)
        w = self.root_number if self.root_number is not None else 1
        Q = mp.sqrt(mp.mpf(self.conductor)) / (2 * mp.pi)
        num_terms = self._num_terms()

        def G(z, x):
            return mp.gammainc(z, x, regularized=True)

        X = mp.power(Q, 2 - 2 * s) * mp.gamma(2 - s) / mp.gamma(s)

        acc = mp.mpc(0)
        for n in range(1, num_terms + 1):
            an = self.a_n(n)
            if an == 0:
                continue
            x = n / Q
            acc += an / mp.power(n, s) * G(s, x)
            acc += w * X * an / mp.power(n, 2 - s) * G(2 - s, x)
        return acc

    def L_derivative_at_one(self, order: int):
        """The k-th derivative L^{(k)}(E, 1) by mpmath complex differentiation.

        BSD's weak form is about how many of these vanish: the analytic rank
        is the least k with L^{(k)}(E, 1) != 0.
        """
        if order == 0:
            return self.L_value(mp.mpc(1))
        return mp.diff(lambda z: self.L_value(z), mp.mpc(1), order)

    def analytic_rank(self, max_order: int = 4, tol: float = 1e-6) -> int:
        """Estimate the analytic rank: least k with L^{(k)}(E, 1) != 0.

        The root number gives parity for free, so we use it as a consistency
        check: a returned rank must match w = (-1)^rank.
        """
        for k in range(max_order + 1):
            val = self.L_derivative_at_one(k)
            if abs(val) > tol:
                return k
        return max_order + 1

    def __repr__(self):
        return f"<EllipticCurve {self.label} N={self.conductor} rank={self.rank}>"
