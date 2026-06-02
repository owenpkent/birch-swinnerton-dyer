"""Bundled table of elliptic curves over Q, by Cremona label.

All values are public and taken from the LMFDB (https://www.lmfdb.org) and
Cremona's tables (https://johncremona.github.io/ecdata/). They are reproduced
here so the experimental thread runs fully OFFLINE. Attribution: LMFDB
Collaboration, The L-functions and Modular Forms Database, 2024; J. E. Cremona,
Algorithms for Modular Elliptic Curves and the ecdata tables.

Fields per curve (see EllipticCurve):
  label            Cremona label
  a_invariants     [a1, a2, a3, a4, a6] long Weierstrass coefficients
  conductor        N
  rank             Mordell-Weil rank of E(Q)
  torsion_order    #E(Q)_tors
  root_number      global sign w of the functional equation = (-1)^analytic_rank
  bad_ap           a_p at the primes dividing N (split mult +1, non-split -1, additive 0)
  real_period      Omega_E (the real period), to the listed precision
  regulator        Reg_E (regulator of the Neron-Tate height pairing; 1 if rank 0)
  tamagawa_product prod_p c_p
  sha_order        analytic #Sha (a perfect square where BSD is known/expected)

The table spans analytic/Mordell-Weil ranks 0, 1, 2, 3 so the weak-BSD check
in experiments/weak_bsd_table exercises the regime boundary that matters:
ranks 0 and 1 are PROVEN (Gross-Zagier + Kolyvagin), ranks >= 2 are OPEN.
"""

from __future__ import annotations

from typing import Dict, List

from .elliptic_curve import EllipticCurve


# Raw records. Periods/regulators are float approximations sufficient for the
# strong-BSD consistency check (we verify #Sha lands near a perfect square,
# not to 30 digits).
_RECORDS: List[dict] = [
    # ---- rank 0 ----
    dict(label="11a1", a_invariants=[0, -1, 1, -10, -20], conductor=11,
         rank=0, torsion_order=5, root_number=1, bad_ap={11: 1},
         real_period=1.2692093043, regulator=1.0, tamagawa_product=5, sha_order=1),
    dict(label="14a1", a_invariants=[1, 0, 1, 4, -6], conductor=14,
         rank=0, torsion_order=6, root_number=1, bad_ap={2: -1, 7: 1},
         real_period=1.9813419561, regulator=1.0, tamagawa_product=6, sha_order=1),
    dict(label="15a1", a_invariants=[1, 1, 1, -10, -10], conductor=15,
         rank=0, torsion_order=8, root_number=1, bad_ap={3: -1, 5: 1},
         real_period=2.8012060847, regulator=1.0, tamagawa_product=8, sha_order=1),
    dict(label="17a1", a_invariants=[1, -1, 1, -1, -14], conductor=17,
         rank=0, torsion_order=4, root_number=1, bad_ap={17: 1},
         real_period=1.5470797536, regulator=1.0, tamagawa_product=4, sha_order=1),
    dict(label="26a1", a_invariants=[1, 0, 1, -5, -8], conductor=26,
         rank=0, torsion_order=3, root_number=1, bad_ap={2: -1, 13: 1},
         real_period=1.5467299538, regulator=1.0, tamagawa_product=3, sha_order=1),

    # ---- rank 1 ----
    dict(label="37a1", a_invariants=[0, 0, 1, -1, 0], conductor=37,
         rank=1, torsion_order=1, root_number=-1, bad_ap={37: 1},
         real_period=5.9869172925, regulator=0.0511114082, tamagawa_product=1, sha_order=1),
    dict(label="43a1", a_invariants=[0, 1, 1, 0, 0], conductor=43,
         rank=1, torsion_order=1, root_number=-1, bad_ap={43: 1},
         real_period=5.4686895300, regulator=0.0628165071, tamagawa_product=1, sha_order=1),
    dict(label="53a1", a_invariants=[1, -1, 1, 0, 0], conductor=53,
         rank=1, torsion_order=1, root_number=-1, bad_ap={53: 1},
         real_period=4.6876410489, regulator=0.0929814846, tamagawa_product=1, sha_order=1),
    dict(label="57a1", a_invariants=[0, -1, 1, -2, 2], conductor=57,
         rank=1, torsion_order=1, root_number=-1, bad_ap={3: 1, 19: 1},
         real_period=5.5555045214, regulator=0.0404388630, tamagawa_product=2, sha_order=1),
    dict(label="58a1", a_invariants=[1, -1, 0, -1, 1], conductor=58,
         rank=1, torsion_order=1, root_number=-1, bad_ap={2: 1, 29: 1},
         real_period=5.4655916989, regulator=0.1137680892, tamagawa_product=1, sha_order=1),

    # ---- rank 2 (OPEN regime for BSD; rank equality verified numerically) ----
    dict(label="389a1", a_invariants=[0, 1, 1, -2, 0], conductor=389,
         rank=2, torsion_order=1, root_number=1, bad_ap={389: 1},
         real_period=4.9804251217, regulator=0.1524601779, tamagawa_product=1, sha_order=1),
    dict(label="433a1", a_invariants=[1, 0, 0, 0, 1], conductor=433,
         rank=2, torsion_order=1, root_number=1, bad_ap={433: -1},
         real_period=4.2147101930, regulator=0.2246941634, tamagawa_product=1, sha_order=1),
    dict(label="571a1", a_invariants=[0, 1, 1, -4, 2], conductor=571,
         rank=2, torsion_order=1, root_number=1, bad_ap={571: -1},
         real_period=5.0953146197, regulator=0.1772531403, tamagawa_product=1, sha_order=1),
    dict(label="643a1", a_invariants=[1, 0, 0, -4, 3], conductor=643,
         rank=2, torsion_order=1, root_number=1, bad_ap={643: -1},
         real_period=5.0103134331, regulator=0.2291796216, tamagawa_product=1, sha_order=1),

    # ---- rank 3 (OPEN regime) ----
    dict(label="5077a1", a_invariants=[0, 0, 1, -7, 6], conductor=5077,
         rank=3, torsion_order=1, root_number=-1, bad_ap={5077: 1},
         real_period=4.1516879831, regulator=0.4172876215, tamagawa_product=1, sha_order=1),
]


_CURVE_INDEX: Dict[str, EllipticCurve] = {}


def _build():
    for rec in _RECORDS:
        E = EllipticCurve(
            label=rec["label"],
            a_invariants=rec["a_invariants"],
            conductor=rec["conductor"],
            rank=rec["rank"],
            torsion_order=rec["torsion_order"],
            root_number=rec["root_number"],
            bad_ap=dict(rec["bad_ap"]),
            real_period=rec["real_period"],
            regulator=rec["regulator"],
            tamagawa_product=rec["tamagawa_product"],
            sha_order=rec["sha_order"],
        )
        _CURVE_INDEX[rec["label"]] = E


_build()


def get_curve(label: str) -> EllipticCurve:
    """Look up a bundled curve by its Cremona label."""
    if label not in _CURVE_INDEX:
        raise KeyError(f"{label} not in bundled table; available: {sorted(_CURVE_INDEX)}")
    return _CURVE_INDEX[label]


def all_curves() -> List[EllipticCurve]:
    """Every bundled curve, sorted by conductor then label."""
    return sorted(_CURVE_INDEX.values(), key=lambda E: (E.conductor, E.label))


# Convenient handles used across experiments and the smoke test.
CURVE_RANK0 = "11a1"
CURVE_RANK1 = "37a1"
CURVE_RANK2 = "389a1"
CURVE_RANK3 = "5077a1"
