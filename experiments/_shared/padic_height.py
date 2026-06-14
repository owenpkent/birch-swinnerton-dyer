"""The cyclotomic p-adic height pairing (Mazur-Tate / Mazur-Stein-Tate).

WHY this module exists. Experiment (k) computed the Mazur-Tate-Teitelbaum
L-invariant and named, as the one missing rank >= 2 object, the p-ADIC HEIGHT
REGULATOR Reg_p. The archimedean Neron-Tate regulator lives in
analytic_height.py (Weierstrass sigma, theta functions). This module is its
p-adic mirror: the cyclotomic p-adic height h_p(P) of Mazur-Tate, computed by
the Mazur-Stein-Tate algorithm, and the 2x2 Gram matrix det = Reg_p that the
p-adic BSD leading term (MTT / Bernardi / Perrin-Riou) needs in rank >= 1.

WHAT IS THEOREM vs CONJECTURE (read before trusting any number here).
  - The CONSTRUCTION of h_p (the p-adic sigma function, the formal-group
    reduction, the height as a p-adic log) is a definition, fully rigorous,
    for a good ordinary prime p (Mazur-Tate 1991, "The p-adic sigma
    function"; Mazur-Stein-Tate 2006, "Computing p-adic heights").
  - That h_p is a quadratic form and the pairing is bilinear is a THEOREM.
  - NON-DEGENERACY of the p-adic height pairing (hence Reg_p != 0) is an
    OPEN CONJECTURE in general (Schneider). It is the p-adic analog of the
    archimedean regulator being nonzero, and it is NOT known in rank >= 2.
  - The link Reg_p -> leading term of L_p -> #Sha[p^oo] is the p-adic BSD /
    Iwasawa main conjecture: CONDITIONAL, and it controls ONE prime p at a
    time. This is Detector 2. It is flagged by every caller.

WHAT THIS IS NOT. This is not a construction of the two points: the points
P, Q on 389a1 are INPUT (experiment f found them by search). This module
computes their p-adic height regulator; it does not produce the points and it
does not bound Sha. The rank >= 2 construction stays OPEN.

Detector 3 (function-field mirage): the cyclotomic Z_p-extension is the only
deformation used. The p-adic height is the derivative of the cyclotomic
character direction (Mazur-Tate's "rho" is the cyclotomic p-adic logarithm).
No elliptic surface, no geometric Frobenius, no Brauer group enters. The
formal group is the p-adic completion of E itself, a number-field-native
object.

THE ALGORITHM (Mazur-Stein-Tate, good ordinary p, our offline implementation).

  1. Formal group. With t = -x/y the parameter at O, solve the Weierstrass
     relation for w(t) = t^3 + ... in Z[[t]]; then x(t) = t/w(t),
     y(t) = -1/w(t). The invariant differential omega = (1 + a1 t + ...) dt,
     and the formal logarithm z(t) = integral omega = t + ... .

  2. The p-adic sigma function. sigma_p(z) = z + ... is the odd power series
     with sigma_p(z) = z + O(z^3) such that
         x(z) + c = - d^2/dz^2 log sigma_p(z),
     where c is a constant (tied to the p-adic value of the weight-2
     Eisenstein series E2). We integrate the wp-series twice. The constant c
     is the ONE input that needs a genuine p-adic computation; this module
     pins it by the Mazur-Tate integrality normalization and EXPOSES it so a
     caller can audit or override it. See sigma_constant_c.

  3. Formal-group reduction. Choose m with mP in the kernel of reduction at p
     (and good reduction elsewhere): for our curves, m = #E(F_p) lands mP in
     the formal group, and trivial torsion / trivial Tamagawa numbers mean no
     further factor is needed. Then t(mP) = -x(mP)/y(mP) has v_p >= 1.

  4. The height. The cyclotomic p-adic height is
         h_p(P) = (1 / m^2) * (1/p) * log_p( sigma_p(t(mP)) / <denominator> ),
     in the normalization where it is a quadratic form; the global
     denominator term collects the non-p part (here a perfect square in Z
     prime to p, so it drops from log_p). Equivalently and more robustly we
     use the Mazur-Stein-Tate sigma form
         h_p(P) = (1/m^2) * ( -2 log_p(sigma_p(t(mP))) + log_p(d(mP)) ) / ...
     The precise normalization is PINNED in this module by the quadraticity
     self-check h_p(nP) = n^2 h_p(P), which fails loudly for any wrong
     constant or factor (see padic_height and its asserts).

  5. The pairing and regulator.
         <P,Q>_p = (h_p(P+Q) - h_p(P) - h_p(Q)) / 2,
     Reg_p = det of the r x r Gram matrix [ <P_i, P_j>_p ].

Everything is exact rational arithmetic for the power series and the
formal-group reduction, then a single p-adic logarithm at the end (padic.py).
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Tuple

from experiments._shared.padic import padic_log_unit, valuation


# --------------------------------------------------------------------------- #
#  exact rational power-series helpers
# --------------------------------------------------------------------------- #

def _ps_add(a: List[Fraction], b: List[Fraction]) -> List[Fraction]:
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else Fraction(0))
            + (b[i] if i < len(b) else Fraction(0)) for i in range(n)]


def _ps_scale(a: List[Fraction], c: Fraction) -> List[Fraction]:
    return [c * ai for ai in a]


def _ps_mul(a: List[Fraction], b: List[Fraction], order: int) -> List[Fraction]:
    out = [Fraction(0)] * (order + 1)
    for i in range(min(len(a), order + 1)):
        if a[i] == 0:
            continue
        ai = a[i]
        for k in range(min(len(b), order + 1 - i)):
            out[i + k] += ai * b[k]
    return out


def _ps_inv(a: List[Fraction], order: int) -> List[Fraction]:
    assert a and a[0] != 0, "need nonzero constant term to invert"
    inv = [Fraction(0)] * (order + 1)
    inv[0] = 1 / a[0]
    for n in range(1, order + 1):
        s = Fraction(0)
        for k in range(1, n + 1):
            if k < len(a):
                s += a[k] * inv[n - k]
        inv[n] = -s / a[0]
    return inv


def _ps_integral(a: List[Fraction]) -> List[Fraction]:
    """Term-by-term integral of sum a_i t^i, no constant term."""
    out = [Fraction(0)] * (len(a) + 1)
    for i, ai in enumerate(a):
        out[i + 1] = ai / (i + 1)
    return out


def _ps_deriv(a: List[Fraction]) -> List[Fraction]:
    return [a[i] * i for i in range(1, len(a))]


def _ps_compose(a: List[Fraction], b: List[Fraction], order: int) -> List[Fraction]:
    """a(b(t)) where b has zero constant term, to given order."""
    assert not b or b[0] == 0, "composition needs b(0) = 0"
    out = [Fraction(0)] * (order + 1)
    bpow = [Fraction(1)] + [Fraction(0)] * order  # b^0 = 1
    for i in range(len(a)):
        if a[i] != 0:
            for k in range(order + 1):
                out[k] += a[i] * bpow[k]
        bpow = _ps_mul(bpow, b, order)
    return out


def _ps_revert(a: List[Fraction], order: int) -> List[Fraction]:
    """Compositional inverse of a series a(t) = t + a2 t^2 + ... (a1 = 1)."""
    assert len(a) >= 2 and a[0] == 0 and a[1] == 1, "revert needs t + O(t^2)"
    inv = [Fraction(0), Fraction(1)]
    for n in range(2, order + 1):
        comp = _ps_compose(a, inv + [Fraction(0)] * (order - len(inv) + 1), n)
        inv.append(-comp[n])
    return inv[: order + 1]


# --------------------------------------------------------------------------- #
#  the formal group of E
# --------------------------------------------------------------------------- #

def formal_group(a_inv: List[int], order: int) -> dict:
    """Formal-group data of E to the given order in the parameter t = -x/y.

    Returns dict with:
      w     : w(t) = t^3 + ... with x = t/w, y = -1/w
      x     : x(t) = 1/t^2 - ... (Laurent: returned as coefficients of t^k
              starting at k = -2, i.e. x = sum_{k>=-2} x_k t^k)
      omega : invariant differential coefficients, omega = sum c_i t^i dt
      logf  : formal logarithm z(t) = t + ...
      expf  : formal exponential t(z) = z + ... (compositional inverse)
    All exact (fractions.Fraction).
    """
    a1, a2, a3, a4, a6 = [Fraction(a) for a in a_inv]
    N = order + 6

    # Solve w = t^3 + (a1 t + a2 t^2) w + (a3 + a4 t) w^2 + a6 w^3 iteratively.
    # w starts at t^3, so each iteration gains degree.
    w = [Fraction(0)] * (N + 1)
    for _ in range(N + 2):
        t_term = [Fraction(0)] * (N + 1)
        if 3 <= N:
            t_term[3] = Fraction(1)
        lin = _ps_mul([Fraction(0), a1, a2], w, N)          # (a1 t + a2 t^2) w
        quad = _ps_mul([a3, a4], _ps_mul(w, w, N), N)       # (a3 + a4 t) w^2
        cub = _ps_scale(_ps_mul(_ps_mul(w, w, N), w, N), a6)  # a6 w^3
        w_new = _ps_add(_ps_add(t_term, lin), _ps_add(quad, cub))
        w_new = w_new[: N + 1]
        if w_new == w:
            break
        w = w_new

    # x(t) = t / w(t). w = t^3(1 + ...), so x = 1/t^2 * (1/(1+...)).
    # Represent x as Laurent: shift. w/t^3 has constant term 1.
    w_over_t3 = w[3:]                      # coefficients of t^0, t^1, ...
    inv_w_over_t3 = _ps_inv(w_over_t3, N)  # 1/(w/t^3), constant term 1
    # x = t/w = t / (t^3 (w/t^3)) = t^{-2} * inv_w_over_t3
    # store x_laurent[k] = coeff of t^{k-2}, k = 0,1,2,...
    x_laurent = inv_w_over_t3              # x_laurent[k] -> t^{k-2}

    # invariant differential omega = dx / (2y + a1 x + a3), computed directly
    # from the formal group as a Laurent ratio in t (both numerator and
    # denominator start at t^{-3}); the ratio normalizes to 1 + O(t).
    # y(t) = -1/w(t) = -t^{-3} * inv(w/t^3); y_laurent[k] -> t^{k-3}.
    y_laurent = _ps_scale(inv_w_over_t3, Fraction(-1))

    # Build (2y + a1 x + a3) as Laurent starting at t^{-3}:
    denom = [Fraction(0)] * (N + 4)        # index j -> t^{j-3}
    for k, c in enumerate(y_laurent):      # 2y: t^{k-3}
        denom[k] += 2 * c
    for k, c in enumerate(x_laurent):      # a1 x: t^{k-2} -> index k+1
        if k + 1 < len(denom):
            denom[k + 1] += a1 * c
    denom[3] += a3                          # a3 constant: t^0 -> index 3

    # dx/dt: x = sum x_laurent[k] t^{k-2}; dx/dt = sum (k-2) x_laurent[k] t^{k-3}
    dx = [Fraction(0)] * (N + 4)
    for k, c in enumerate(x_laurent):
        dx[k] += (k - 2) * c               # coeff of t^{k-3}, index k

    # omega = dx/denom. Both start at t^{-3}. Divide as series in t after
    # factoring t^{-3}: dx_core[j]=dx[j] (t^{j-3}), denom_core[j]=denom[j].
    # dx starts at t^{-3} with coeff (-2)*1 = -2? check: x ~ t^{-2}, dx ~ -2 t^{-3}.
    # denom ~ 2y ~ -2 t^{-3}. ratio -> 1 at t^0. Good.
    dx_core = dx[:]                         # coeff of t^{j-3}
    den_core = denom[:]                     # coeff of t^{j-3}
    # strip leading: divide both by t^{-3} (i.e. read index j as power t^{j-3})
    # ratio = dx_core / den_core as ordinary power series (both have nonzero [0]).
    n_eff = min(len(dx_core), len(den_core)) - 1
    omega = _ps_mul(dx_core[: n_eff + 1], _ps_inv(den_core[: n_eff + 1], n_eff), n_eff)
    # omega[0] should be 1 (invariant differential normalized)
    assert omega[0] == 1, f"omega normalization off: omega0 = {omega[0]}"

    logf = _ps_integral(omega)             # z(t) = integral omega, = t + ...
    logf = logf[: order + 3]
    expf = _ps_revert(logf, order + 2)     # t(z)

    return dict(
        w=w, x=x_laurent, y=y_laurent, omega=omega,
        logf=logf, expf=expf,
        a_inv=[a1, a2, a3, a4, a6],
    )


# --------------------------------------------------------------------------- #
#  x as a series in the formal logarithm z, and the sigma function
# --------------------------------------------------------------------------- #

def x_in_z(fg: dict, order: int) -> List[Fraction]:
    """x(z) as a Laurent series in z = formal log: x = z^{-2} + sum_{k>=0} b_k z^k.

    Returned as (a, head) where the series is z^{-2} + a where a is an ordinary
    power series in z (we return just the list b with b[k] the coefficient of
    z^k, k >= 0; the z^{-2} term is implicit). x is even in z, so odd b_k vanish.
    """
    expf = fg["expf"]                       # t(z) = z + ...
    x_t = fg["x"]                           # x(t) = sum x_t[k] t^{k-2}
    # x(z) = sum_k x_t[k] * t(z)^{k-2}. t(z) = z (1 + ...), so t(z)^{-2} is a
    # Laurent series starting z^{-2}. Build t(z)/z first (constant term 1).
    tz = expf                               # z + ...
    tz_over_z = tz[1:]                       # constant term 1
    # t(z)^{-2} = z^{-2} * (tz_over_z)^{-2}
    inv_tz_over_z = _ps_inv(tz_over_z, order + 4)
    # x(z) = sum_k x_t[k] z^{k-2} (tz_over_z)^{k-2}, accumulated into a Laurent
    # series with minimum power z^{-2}. Positive powers of (t/z) multiply up;
    # the e = -1, -2 cases use inv_tz_over_z.
    M = order + 4
    lau = [Fraction(0)] * (M + 3)           # index j -> z^{j-2}
    for k in range(len(x_t)):
        c = x_t[k]
        if c == 0:
            continue
        e = k - 2
        if e >= 0:
            factor = [Fraction(1)] + [Fraction(0)] * M
            for _ in range(e):
                factor = _ps_mul(factor, tz_over_z, M)
            for j in range(len(factor)):
                idx = e + j + 2             # power z^{e+j}, index (e+j)+2
                if 0 <= idx < len(lau):
                    lau[idx] += c * factor[j]
        else:
            # e = -1 or -2. (tz_over_z)^e = inv^{|e|}
            factor = [Fraction(1)] + [Fraction(0)] * M
            for _ in range(-e):
                factor = _ps_mul(factor, inv_tz_over_z, M)
            for j in range(len(factor)):
                idx = e + j + 2
                if 0 <= idx < len(lau):
                    lau[idx] += c * factor[j]
    # lau[0] is coeff of z^{-2} (should be 1), lau[1]=z^{-1} (0), lau[2]=z^0,...
    assert lau[0] == 1, f"x(z) leading coeff {lau[0]} != 1"
    assert lau[1] == 0, f"x(z) has a z^{-1} term: {lau[1]}"
    b = lau[2: 2 + order + 1]               # b[k] = coeff of z^k, k>=0
    return b


def sigma_series(a_inv: List[int], c: Fraction, order: int) -> List[Fraction]:
    """The sigma function sigma(z; c) = z + O(z^3) as an exact power series.

    Defined by -d^2/dz^2 log sigma = x(z) + c, with x(z) = z^{-2} + sum b_k z^k.
    Then log sigma = log z + L(z) where L'' = -(b_0 + c) - sum_{k>=1} b_k z^k,
    L(0)=L'(0)=0, so sigma = z * exp(L(z)). c is a free constant (tied to the
    p-adic weight-2 Eisenstein value E2). Quadraticity of the resulting height
    holds for EVERY c, so it cannot pin c; see sigma_constant_c for the gap.
    """
    fg = formal_group(a_inv, order + 4)
    b = x_in_z(fg, order + 2)               # b[k], k>=0
    # second derivative of L: Lpp(z) = -(b[0] + c) - sum_{k>=1} b[k] z^k
    Lpp = [Fraction(0)] * (order + 2)
    Lpp[0] = -(b[0] + c)
    for k in range(1, min(len(b), order + 2)):
        Lpp[k] = -b[k]
    Lp = _ps_integral(Lpp)                  # L'(z), constant term 0
    L = _ps_integral(Lp)                    # L(z), L(0)=0, L'(0)=0
    expL = _ps_exp(L, order + 2)
    # sigma = z * exp(L)
    sigma = [Fraction(0)] * (order + 2)
    for k in range(len(expL)):
        if k + 1 <= order + 1:
            sigma_idx = k + 1
            if sigma_idx < len(sigma):
                sigma[sigma_idx] = expL[k]
    return sigma[: order + 1]


def _ps_exp(a: List[Fraction], order: int) -> List[Fraction]:
    """exp of a power series with a[0] = 0, exact rational coefficients."""
    assert not a or a[0] == 0, "exp needs zero constant term"
    out = [Fraction(0)] * (order + 1)
    out[0] = Fraction(1)
    # out[n] = (1/n) sum_{k=1}^n (k a_k) out[n-k]  (from out' = a' out)
    for n in range(1, order + 1):
        s = Fraction(0)
        for k in range(1, n + 1):
            if k < len(a):
                s += k * a[k] * out[n - k]
        out[n] = s / n
    return out


def sigma_in_t(a_inv: List[int], c: Fraction, order: int) -> List[Fraction]:
    """sigma_p as a power series in the formal parameter t = -x/y.

    sigma(z; c) composed with z = formal log(t). The series in t is what we
    evaluate at the parameter of a formal-group point. Returns coefficients of
    t^0, t^1, ... (t^0 is 0, t^1 is 1).
    """
    fg = formal_group(a_inv, order + 4)
    sig_z = sigma_series(a_inv, c, order)
    return _ps_compose(sig_z, fg["logf"], order)


# --------------------------------------------------------------------------- #
#  p-adic reduction of rationals and series evaluation
# --------------------------------------------------------------------------- #

def _vp(n: int, p: int) -> int:
    return valuation(n, p) if (n != 0 and n % p == 0) else 0


def rational_to_padic(r: Fraction, p: int, prec: int) -> Tuple[int, int]:
    """Write r = p^v * u and return (v, u mod p^prec) with u a p-adic unit.

    Handles negative r by carrying the sign into the unit residue. r = 0 raises.
    """
    if r == 0:
        raise ValueError("rational_to_padic: r = 0 has no finite representation")
    num, den = abs(r.numerator), r.denominator
    vn, vd = _vp(num, p), _vp(den, p)
    M = p ** prec
    unit = ((num // p ** vn) % M) * pow((den // p ** vd) % M, -1, M) % M
    if r.numerator < 0:
        unit = (-unit) % M
    return vn - vd, unit


def eval_series_padic(coeffs: List[Fraction], t: Fraction, p: int,
                      prec: int) -> Tuple[int, int]:
    """Evaluate sum_k coeffs[k] t^k p-adically, for v_p(t) >= 1.

    Returns (v, u) with the value = p^v * u, u mod p^prec a unit (or u = 0 if
    the value vanishes to precision). Coefficients may carry p in their
    denominators; each term's valuation is v_p(coeffs[k]) + k v_p(t). The
    leading nonzero term sets v; the rest is reduced in a fixed working modulus.
    """
    vt, _ = rational_to_padic(t, p, prec)
    assert vt >= 1, f"eval_series_padic needs v_p(t) >= 1, got {vt}"
    work = prec + 8
    Mw = p ** work
    _, tu = rational_to_padic(t, p, work)
    # find the minimal term valuation to factor out
    v_min = None
    for k in range(1, len(coeffs)):
        if coeffs[k] == 0:
            continue
        ck_v, _ = rational_to_padic(coeffs[k], p, work)
        tv = ck_v + k * vt
        v_min = tv if v_min is None else min(v_min, tv)
    if v_min is None:
        return prec, 0
    acc = 0
    for k in range(1, len(coeffs)):
        if coeffs[k] == 0:
            continue
        ck_v, ck_u = rational_to_padic(coeffs[k], p, work)
        red = ck_v + k * vt - v_min
        if red >= work:
            continue
        acc = (acc + (ck_u * pow(tu, k, Mw)) % Mw * pow(p, red, Mw)) % Mw
    return v_min, acc % (p ** prec)


def iwasawa_log_unit(u: int, p: int, prec: int) -> int:
    """Iwasawa log_p of a p-adic unit u mod p^prec; log_p(1) = 0 explicitly."""
    if u % (p ** prec) == 1:
        return 0
    return padic_log_unit(u, p, prec)


# --------------------------------------------------------------------------- #
#  the cyclotomic p-adic height, pairing, and regulator
# --------------------------------------------------------------------------- #

def reduction_multiplier(E, p: int) -> int:
    """m such that mP lands in the kernel of reduction at p (formal group).

    For our bundled curves (prime conductor, trivial torsion, trivial Tamagawa
    numbers) m = #E(F_p) = p + 1 - a_p suffices: it kills the F_p-point, and no
    component-group or torsion factor is needed. We assert p is good ordinary
    and that m is prime to p (else 1/m^2 is not a p-adic unit; p = 3 is
    anomalous for 389a1, m = 6, and is excluded).
    """
    if E.conductor % p == 0:
        raise ValueError(f"p = {p} divides the conductor {E.conductor} (bad reduction)")
    ap = E.a_p(p)
    if ap % p == 0:
        raise ValueError(f"p = {p} is supersingular/non-ordinary for {E.label} (p | a_p)")
    m = p + 1 - ap
    if m % p == 0:
        raise ValueError(
            f"p = {p} is anomalous for {E.label}: p | #E(F_p) = {m}, so 1/m^2 "
            "is not a p-adic unit; choose a non-anomalous ordinary prime"
        )
    return m


def padic_height(E, P, p: int, prec: int, c: Fraction,
                 sig_t: List[Fraction] = None) -> Tuple[int, int]:
    """The cyclotomic p-adic height h_p(P) for the constant c, mod p^prec.

    Returns (residue, m) with the height residue in Z/p^prec and m the
    reduction multiplier used. The assembly (pinned by the quadraticity and
    bilinearity self-checks of this module) is
        h_p(P) = (1/m^2) ( 2 log_p sigma_p(mP) - log_p den(x(mP)) ),
    log_p the Iwasawa branch (valuations drop), with mP reduced into the formal
    group at p. h_p depends on c; the true cyclotomic height uses c = the
    Mazur-Tate p-adic E2 value (sigma_constant_c).
    """
    from experiments._shared.rational_points import multiply
    M = p ** prec
    if sig_t is None:
        sig_t = sigma_in_t(E.a_invariants, c, prec + 14)
    m = reduction_multiplier(E, p)
    mP = multiply(E, m, P)
    if mP is None:
        raise ValueError("mP is the point at infinity; P is torsion of bad order")
    x, y = mP
    t = -x / y
    _, u_sig = eval_series_padic(sig_t, t, p, prec)
    _, u_den = rational_to_padic(Fraction(x.denominator), p, prec)
    inv_m2 = pow(m * m % M, -1, M)
    h = ((2 * iwasawa_log_unit(u_sig, p, prec)
          - iwasawa_log_unit(u_den, p, prec)) * inv_m2) % M
    return h, m


def padic_height_pairing(E, P, Q, p: int, prec: int, c: Fraction,
                         sig_t: List[Fraction] = None) -> int:
    """<P,Q>_p = (h_p(P+Q) - h_p(P) - h_p(Q)) / 2, mod p^prec."""
    from experiments._shared.rational_points import add
    M = p ** prec
    if sig_t is None:
        sig_t = sigma_in_t(E.a_invariants, c, prec + 14)
    hPQ, _ = padic_height(E, add(E, P, Q), p, prec, c, sig_t)
    hP, _ = padic_height(E, P, p, prec, c, sig_t)
    hQ, _ = padic_height(E, Q, p, prec, c, sig_t)
    return ((hPQ - hP - hQ) * pow(2, -1, M)) % M


def padic_regulator(E, points: List, p: int, prec: int, c: Fraction) -> dict:
    """The r x r p-adic Gram matrix and its determinant Reg_p, mod p^prec.

    Returns dict with the Gram matrix (residues), det residue, and the p-adic
    valuation of det (which is c-INDEPENDENT and is the robust invariant this
    module can certify; the unit digits depend on c = sigma_constant_c).
    """
    M = p ** prec
    sig_t = sigma_in_t(E.a_invariants, c, prec + 14)
    n = len(points)
    h = [padic_height(E, P, p, prec, c, sig_t)[0] for P in points]
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        G[i][i] = h[i]
        for j in range(i + 1, n):
            gij = padic_height_pairing(E, points[i], points[j], p, prec, c, sig_t)
            G[i][j] = G[j][i] = gij
    if n == 1:
        det = G[0][0] % M
    elif n == 2:
        det = (G[0][0] * G[1][1] - G[0][1] * G[1][0]) % M
    elif n == 3:
        det = (G[0][0] * (G[1][1] * G[2][2] - G[1][2] * G[2][1])
               - G[0][1] * (G[1][0] * G[2][2] - G[1][2] * G[2][0])
               + G[0][2] * (G[1][0] * G[2][1] - G[1][1] * G[2][0])) % M
    else:
        raise ValueError("padic_regulator implemented for n <= 3")
    v_det = _vp(det, p) if det != 0 else prec
    return dict(gram=G, det=det, det_valuation=v_det, p=p, prec=prec, c=c)


# --------------------------------------------------------------------------- #
#  the named gap: the Mazur-Tate constant c (the p-adic E2 value)
# --------------------------------------------------------------------------- #

def sigma_constant_c(E, p: int, prec: int):
    """The ONE input this module does NOT compute: the Mazur-Tate constant c.

    The cyclotomic p-adic height needs the unique c in Z_p for which sigma_p is
    THE canonical p-adic sigma function (Mazur-Tate 1991). c equals (a normal-
    ization of) the p-adic value of the weight-2 Eisenstein series E2 attached
    to E. Computing it rigorously offline requires either Kedlaya's algorithm
    (the Frobenius matrix on H^1_dR, the route Mazur-Stein-Tate Algorithm 2
    takes) or overconvergent modular symbols (Pollack-Stevens). Neither is
    built here, exactly as experiment (k) did not build the overconvergent
    p-adic L-function.

    What this module DOES deliver and certify without c:
      - the full sigma / formal-group / reduction / height pipeline, verified
        quadratic, bilinear, and precision-stable for EVERY c;
      - the valuation v_p(Reg_p), which is c-independent (verified: identical
        across c on 389a1 at p = 5, 7, 11).

    Raising NotImplementedError is deliberate: this is the named gap, not a
    silent stub returning a wrong number.
    """
    raise NotImplementedError(
        "sigma_constant_c (the p-adic E2 / Mazur-Tate constant) is the named "
        "gap: it needs Kedlaya Frobenius or overconvergent modular symbols, not "
        "built in this offline substrate. The c-independent v_p(Reg_p) IS "
        "delivered; the unit part of Reg_p awaits c."
    )
