"""Shared infrastructure for the BSD proof-architecture experiments.

Provides a uniform EllipticCurve / Hasse-Weil L-function interface plus the
three wrong-approach detectors (parity-only, Sha-finiteness assumed,
function-field mirage) and the proven-vs-open control pair, so every
experiment runs against the same curves and the same discipline checks.
"""

from .elliptic_curve import EllipticCurve
from .curve_data import (
    get_curve,
    all_curves,
    CURVE_RANK0,
    CURVE_RANK1,
    CURVE_RANK2,
    CURVE_RANK3,
)
from .controls import (
    root_number_parity,
    parity_detector,
    ParityVerdict,
    sha_finiteness_flag,
    ShaFlag,
    function_field_template,
    function_field_mirage,
    FunctionFieldTemplate,
    control_pair,
    ControlPair,
)

__all__ = [
    "EllipticCurve",
    "get_curve",
    "all_curves",
    "CURVE_RANK0",
    "CURVE_RANK1",
    "CURVE_RANK2",
    "CURVE_RANK3",
    "root_number_parity",
    "parity_detector",
    "ParityVerdict",
    "sha_finiteness_flag",
    "ShaFlag",
    "function_field_template",
    "function_field_mirage",
    "FunctionFieldTemplate",
    "control_pair",
    "ControlPair",
]
