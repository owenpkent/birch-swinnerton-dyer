"""Wrong-approach detectors for the BSD experimental thread.

The Riemann sibling repo uses the Davenport-Heilbronn L-function as a single
structural wrong-approach detector. BSD's discipline is different in flavor
(there is no single counterexample L-function), so the detectors here encode
the three ways a candidate BSD argument silently cheats. Any experiment or
proposed method is run through these and must come back clean.

Detector 1: PARITY-ONLY.
  From modularity the root number w gives the analytic rank only mod 2, and the
  parity conjecture (Nekovar; T. and V. Dokchitser) gives the Mordell-Weil rank
  only mod 2. A method whose entire output is a parity statement cannot prove
  the FULL rank equality. parity_detector flags a claimed conclusion that uses
  only w.

Detector 2: SHA-FINITENESS ASSUMED.
  #Sha(E) is finite only KNOWN for analytic rank <= 1 (Gross-Zagier +
  Kolyvagin). It is a necessary input to strong BSD. A method that uses
  #Sha < infinity must say so out loud. sha_finiteness_flag records whether a
  computation assumed it and whether the curve is in the proven regime.

Detector 3: FUNCTION-FIELD MIRAGE.
  Over a function field F_q(C), BSD for an elliptic curve is a THEOREM under
  finiteness of the Brauer/Tate-Shafarevich group (Tate; Artin-Tate; Milne).
  That is the structural template: it shows what a complete proof looks like in
  the geometric case. A method that "proves BSD" by an argument that would work
  verbatim over a function field has probably imported the geometric Frobenius
  that the number-field case lacks. function_field_template documents the
  template and the gap.

CONTROL PAIR.
  rank <= 1 curve (BSD proven) vs an explicit rank >= 2 curve (BSD open). A
  method must do something genuinely new in the rank >= 2 case, not just
  reproduce the proven regime. control_pair returns the pair.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .curve_data import get_curve
from .elliptic_curve import EllipticCurve


# --------------------------------------------------------------------------
# Detector 1: parity-only
# --------------------------------------------------------------------------

def root_number_parity(E: EllipticCurve) -> int:
    """Parity of the analytic rank predicted by the root number: w = (-1)^r.

    Returns 0 (even rank) or 1 (odd rank). This is ALL the root number knows.
    """
    w = E.root_number
    if w is None:
        raise ValueError(f"{E.label} has no recorded root number")
    return 0 if w == 1 else 1


@dataclass
class ParityVerdict:
    is_parity_only: bool
    message: str


def parity_detector(claims_full_rank: bool, uses_only_root_number: bool) -> ParityVerdict:
    """Flag a conclusion that claims the full rank from parity data alone.

    claims_full_rank: does the method assert the exact rank (not just parity)?
    uses_only_root_number: is the only structural input the sign w?

    A method that claims the full rank using only w is INCOMPLETE: w fixes the
    rank mod 2 but cannot separate rank 0 from rank 2, or rank 1 from rank 3.
    """
    if claims_full_rank and uses_only_root_number:
        return ParityVerdict(
            True,
            "PARITY-ONLY: the root number gives rank mod 2 only. "
            "It cannot distinguish rank 0 from 2 or rank 1 from 3. "
            "A full-rank claim from w alone is incomplete.",
        )
    return ParityVerdict(False, "OK: conclusion is not parity-only.")


# --------------------------------------------------------------------------
# Detector 2: Sha-finiteness assumed
# --------------------------------------------------------------------------

@dataclass
class ShaFlag:
    assumed: bool
    in_proven_regime: bool
    message: str


def sha_finiteness_flag(E: EllipticCurve, analytic_rank: int, method_assumes_finite: bool) -> ShaFlag:
    """Record whether finiteness of Sha was assumed and whether it is proven.

    Finiteness of Sha(E) is a theorem only for analytic rank <= 1. For a
    rank >= 2 curve, any strong-BSD computation that solves for #Sha is
    assuming a conjecture. This is not wrong, but it must be flagged.
    """
    proven = analytic_rank <= 1
    if method_assumes_finite and not proven:
        msg = (
            f"SHA ASSUMED (analytic rank {analytic_rank} >= 2): finiteness of "
            "Sha is OPEN here. Any #Sha read off the BSD formula is conjectural."
        )
    elif method_assumes_finite and proven:
        msg = (
            f"Sha finiteness used and PROVEN (analytic rank {analytic_rank} <= 1, "
            "Gross-Zagier + Kolyvagin)."
        )
    else:
        msg = "Sha finiteness not used."
    return ShaFlag(method_assumes_finite, proven, msg)


# --------------------------------------------------------------------------
# Detector 3: function-field template / mirage
# --------------------------------------------------------------------------

@dataclass
class FunctionFieldTemplate:
    statement: str
    what_it_proves: str
    the_gap: str


def function_field_template() -> FunctionFieldTemplate:
    """The geometric template: BSD over F_q(C) is a theorem under finite Sha.

    Use this as the 'this is what a complete proof looks like' control, exactly
    as the Riemann sibling repo uses function-field RH (Weil/Deligne) as its
    template for what Spec(Z) is missing.
    """
    return FunctionFieldTemplate(
        statement=(
            "For an elliptic curve E over a global function field K = F_q(C), the "
            "BSD rank equality and the leading-coefficient formula hold provided the "
            "Tate-Shafarevich (equivalently Brauer) group is finite (Tate; Artin-Tate; "
            "Milne 1975). The L-function is a rational function of q^{-s} (Grothendieck), "
            "so analytic continuation and the functional equation are automatic."
        ),
        what_it_proves=(
            "In the geometric case the analytic rank equals the rank of the "
            "Mordell-Weil group, and #Sha appears as the order of a finite group "
            "computed from etale cohomology of a surface (the elliptic surface E -> C)."
        ),
        the_gap=(
            "Over Q there is no base curve C and no geometric Frobenius. The "
            "missing object is the arithmetic surface and its cohomology. A method "
            "that 'works' verbatim over a function field has imported the very "
            "Frobenius structure the number-field case lacks."
        ),
    )


def function_field_mirage(method_uses_geometric_frobenius: bool,
                          method_needs_base_curve: bool) -> str:
    """Flag a method that secretly relies on the geometric (function-field) input."""
    if method_uses_geometric_frobenius or method_needs_base_curve:
        return (
            "FUNCTION-FIELD MIRAGE: this method relies on a geometric Frobenius / "
            "base curve that exists over F_q(C) but not over Q. The crossing of that "
            "gap is exactly the open part of BSD, so the argument is incomplete over Q."
        )
    return "OK: method does not silently import the function-field geometry."


# --------------------------------------------------------------------------
# Control pair: proven (rank <= 1) vs open (rank >= 2)
# --------------------------------------------------------------------------

@dataclass
class ControlPair:
    proven: EllipticCurve
    open_: EllipticCurve

    def describe(self) -> str:
        return (
            f"PROVEN regime: {self.proven.label} (rank {self.proven.rank}); "
            f"BSD rank equality + finite Sha are theorems (Gross-Zagier + Kolyvagin). "
            f"OPEN regime: {self.open_.label} (rank {self.open_.rank}); "
            f"BSD is conjectural, Sha-finiteness is unproven. "
            f"A method must do something genuinely NEW on {self.open_.label}."
        )


def control_pair(proven_label: str = "37a1", open_label: str = "389a1") -> ControlPair:
    """The default rank-1 (proven) vs rank-2 (open) control pair."""
    return ControlPair(get_curve(proven_label), get_curve(open_label))
