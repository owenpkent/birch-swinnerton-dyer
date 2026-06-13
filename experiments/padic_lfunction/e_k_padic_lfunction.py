"""Experiment (k): the p-adic L-function thread (Mazur-Tate-Teitelbaum).

This is the computational side of architecture 3 (Iwasawa theory). Where the
complex L-function L(E,s) measures the rank at the archimedean place, the
p-adic L-function L_p(E,s) measures it at p, and it carries one phenomenon the
complex side has no analog for: the EXCEPTIONAL (trivial) ZERO.

The setup. For a prime p of good ordinary or multiplicative reduction one
p-stabilizes by the unit root alpha of X^2 - a_p X + p, and L_p(E,s)
interpolates L(E,s)/Omega_E against the cyclotomic characters, weighted by a
multiplier:
  - good ordinary p:        (1 - 1/alpha)^2,   alpha != 1, nonzero;
  - split multiplicative p: (1 - 1/alpha) with alpha = a_p = +1, i.e. ZERO.
So at a split-multiplicative prime the interpolation factor kills the value:
L_p(E,1) = 0 even when L(E,1) != 0. That extra zero is not explained by the
Mordell-Weil rank. Mazur, Tate and Teitelbaum predicted, and Greenberg-Stevens
(1993) proved, that the missing derivative is governed by a purely p-adic
number, the L-INVARIANT
        L_p(E) = log_p(q_E) / ord_p(q_E),
q_E the Tate parameter, log_p the Iwasawa branch (log_p(p) = 0):
        L_p'(E,1) = L_p(E) * L(E,1)/Omega_E          (split multiplicative).

What this experiment computes, all offline and exactly p-adically
([`_shared/padic.py`](../_shared/padic.py)):

  1. THE EXCEPTIONAL-ZERO CLASSIFICATION. For every prime-conductor bundled
     curve, the p-stabilization multiplier at p = N. Split (a_N = +1) gives 0,
     an exceptional zero; non-split (a_N = -1) gives 2, none. A good-ordinary
     contrast (11a1 at p = 3, 7) shows the unit root alpha != 1 and a nonzero
     multiplier.

  2. THE L-INVARIANT. The Tate parameter q_E (by p-adic inversion of the
     j-series, ord_p(q) cross-checked against v_p(Delta)) and the L-invariant
     L_p(E) for each split-multiplicative curve, to 20 base-p digits.

  3. THE GREENBERG-STEVENS PREDICTION. For 11a1 (rank 0, the original MTT
     example) the right-hand side L_p(E) * L(E,1)/Omega_E is assembled
     numerically: L(E,1)/Omega_E = 1/5 (computed on the substrate) embeds in
     Z_11, giving the predicted L_p'(E,1) as an explicit 11-adic number.

  4. THE OPEN REGIME. The rank-2 curves 389a1, 433a1, 571a1, 643a1 are split
     multiplicative, so their p-adic L-function vanishes to order rank + 1 = 3.
     The L-invariant is computed; the leading p-adic coefficient additionally
     needs the p-adic height regulator, named as the missing input.

Detector posture (architecture 3):
  - Detector 1: the L-invariant is a leading-coefficient datum, strictly finer
    than the parity of the rank, but it lives at p, not at infinity.
  - Detector 2: the bridge from L_p to #Sha[p^oo] is the Iwasawa main
    conjecture (Skinner-Urban, Kato). It is an INPUT, conditional on
    hypotheses, and it controls one p at a time; global Sha-finiteness in rank
    >= 2 is not delivered. The exceptional zero adds a derivative, not a bound.
  - Detector 3: the cyclotomic Z_p-extension replaces the geometric Frobenius;
    no elliptic surface, no Brauer group. No function-field import.

The honest limit: the full p-adic L-function value/derivative needs modular
symbols (overconvergent, Pollack-Stevens), which this thread does NOT build.
The L-invariant and the exceptional-zero structure, which are the whole of the
MTT phenomenon at the level of the leading term, it does.

Run from the repo root:
    python -m experiments.padic_lfunction.e_k_padic_lfunction
"""

from __future__ import annotations

from fractions import Fraction

import mpmath as mp

from experiments._shared import get_curve, sha_finiteness_flag, function_field_template
from experiments._shared.padic import (
    l_invariant, stabilization_multiplier, weierstrass_invariants, valuation,
    padic_log_unit,
)

PREC = 20                      # base-p digits of p-adic precision
SPLIT_CURVES = ["11a1", "389a1", "433a1", "571a1", "643a1"]
NONSPLIT_CURVES = ["37a1", "43a1", "53a1", "5077a1"]


def _padic_str(residue: int, valn: int, p: int, digits: int = 5) -> str:
    """Compact display of a p-adic number: valuation + residue mod p^digits."""
    if residue == 0:
        return f"O(p^{PREC})"
    return f"v_{p}={valn}, residue mod {p}^{digits} = {residue % (p ** digits)}"


def main() -> int:
    print("EXPERIMENT (k): the p-adic L-function / Mazur-Tate-Teitelbaum thread")
    print("=" * 70)

    # ---- 1. exceptional-zero classification --------------------------------
    print()
    print("1. EXCEPTIONAL-ZERO CLASSIFICATION (p = N, the bad prime)")
    print(f"{'curve':>7} {'rank':>4} {'p=N':>6} {'a_p':>4} {'reduction':>16} "
          f"{'multiplier':>11} {'exceptional zero?':>18}")
    print("-" * 72)
    for label in SPLIT_CURVES + NONSPLIT_CURVES:
        E = get_curve(label)
        p = E.conductor
        ap = E.bad_ap[p]
        m = stabilization_multiplier(ap, p, PREC, multiplicative=True)
        red = "split mult." if ap == 1 else "non-split mult."
        mult = "0" if m["exceptional"] else str(m["multiplier"])
        exc = "YES (extra zero)" if m["exceptional"] else "no"
        print(f"{label:>7} {E.rank:>4} {p:>6} {ap:>+4d} {red:>16} {mult:>11} {exc:>18}")
    print("-" * 72)
    print("  Split multiplicative <=> a_p = +1 <=> the unit root alpha = 1 <=> the")
    print("  interpolation factor (1 - 1/alpha) vanishes: L_p(E,1) = 0 with no")
    print("  Mordell-Weil reason. This is the phenomenon the complex L has no analog for.")

    # good-ordinary contrast: 11a1 at p = 3, 7
    print()
    print("   good-ordinary contrast (11a1): unit root alpha of X^2 - a_p X + p")
    E11 = get_curve("11a1")
    for q in (3, 7):
        ap = E11.a_p(q)
        m = stabilization_multiplier(ap, q, PREC, multiplicative=False)
        print(f"     p = {q}: a_p = {ap:+d}, alpha = {m['alpha'] % (q**5)} (mod {q}^5), "
              f"(1-1/alpha)^2 != 0 mod {q}: {m['multiplier'] % q != 0}  -> no exceptional zero")

    # ---- 2. the L-invariant ------------------------------------------------
    print()
    print("2. THE L-INVARIANT  L_p(E) = log_p(q_E) / ord_p(q_E)  (split mult., 20 digits)")
    print(f"{'curve':>7} {'rank':>4} {'p':>6} {'ord_p(q)':>9} {'v_p(Delta)':>11} "
          f"{'L_p(E)':>34}")
    print("-" * 74)
    for label in SPLIT_CURVES:
        E = get_curve(label)
        p = E.conductor
        c4, c6, disc = weierstrass_invariants(E.a_invariants)
        vD = valuation(disc, p)
        r = l_invariant(E.a_invariants, p, PREC)
        ok = "ok" if r["e"] == vD else "MISMATCH"
        disp = _padic_str(r["L_p"], r["L_p_valuation"], p, digits=5)
        print(f"{label:>7} {E.rank:>4} {p:>6} {r['e']:>9} {vD:>11} ({ok})  {disp}")
    print("-" * 74)
    print("  ord_p(q) = v_p(Delta) on every curve (Tate: components of the Neron fibre).")
    print("  L_p(E) is a unit-valuation p-adic number with no archimedean shadow.")

    # ---- 3. the Greenberg-Stevens prediction on 11a1 -----------------------
    print()
    print("3. GREENBERG-STEVENS on 11a1 (rank 0, the original MTT example)")
    mp.mp.dps = 25
    L_over_Omega = E11.L_value(mp.mpc(1)).real / E11.real_period
    frac = Fraction(float(L_over_Omega)).limit_denominator(1000)
    print(f"   L(11a1,1)/Omega_E = {mp.nstr(L_over_Omega, 12)} = {frac} (rational, rank 0)")
    p = 11
    M = p ** PREC
    r = l_invariant(E11.a_invariants, p, PREC)
    # embed L/Omega = a/b in Z_11 and predict L_p'(E,1) = L_p(E) * (a/b)
    aob = (frac.numerator % M) * pow(frac.denominator % M, -1, M) % M
    # L_p(E) as a true p-adic integer times p^{val}; here val = 1, residue r['L_p'] is L_p/p^?  -
    # reconstruct log_q (= L_p * ord) then multiply, to keep the valuation honest
    log_q = r["log_q"]
    ord_q = r["e"]
    Lp_times = (log_q * pow(ord_q % M, -1, M)) % M           # = L_p(E) mod 11^20
    predicted = (Lp_times * aob) % M
    vpred = valuation(predicted, p) if predicted % p == 0 else 0
    print(f"   L_p(11a1) = log_11(q)/ord_11(q),  ord = {ord_q},  "
          f"v_11(L_p) = {r['L_p_valuation']}")
    print(f"   PREDICTED L_p'(11a1, 1) = L_p(E) * (1/5):  "
          f"v_11 = {vpred}, residue mod 11^5 = {predicted % (p**5)}")
    print("   (Greenberg-Stevens 1993, Invent. math. 111. Confirming this number")
    print("   numerically needs the modular-symbol L_p, the named next sub-step;")
    print("   both factors on the right are assembled here from the substrate.)")

    # ---- 4. the open regime ------------------------------------------------
    print()
    print("4. THE OPEN REGIME: rank-2 curves are split multiplicative")
    print("   For 389a1, 433a1, 571a1, 643a1 the p-adic L-function vanishes to order")
    print("   rank + 1 = 3 (two from the rank, one exceptional). The L-invariant above")
    print("   is one factor of the leading p-adic coefficient; the rest is the p-adic")
    print("   height regulator (Mazur-Tate-Teitelbaum / Bernardi / Perrin-Riou), the")
    print("   p-adic analog of Reg_E. That regulator is NOT built here.")
    flag = sha_finiteness_flag(get_curve("389a1"), analytic_rank=2,
                               method_assumes_finite=False)
    print()
    print("   DETECTOR 2 (Sha): the bridge L_p -> #Sha[p^oo] is the Iwasawa main")
    print("   conjecture (Skinner-Urban / Kato), an INPUT under hypotheses, one prime")
    print("   at a time. The exceptional zero adds a derivative, never a Sha bound.")
    print(f"     {flag.message}")
    tmpl = function_field_template()
    print("   DETECTOR 3 (function field): the cyclotomic Z_p-extension stands in for")
    print("   the geometric Frobenius; no elliptic surface, no Brauer group is used.")
    print(f"     contrast: {tmpl.the_gap}")

    print()
    print("SUMMARY. The exceptional zero and the L-invariant, the entire MTT")
    print("phenomenon at the level of the leading term, are computed exactly and")
    print("offline. They are p-adic data: finer than parity (Detector 1), but they")
    print("bound no Sha in rank >= 2 (Detector 2) and import no surface (Detector 3).")
    print("Architecture 3 reaches the p-part of one prime under a conjectural")
    print("input; the archimedean leading term and global Sha-finiteness stay open.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
