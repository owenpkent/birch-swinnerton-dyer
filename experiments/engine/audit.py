"""Soundness oracle: run a method or a proof edge past the three detectors.

The engine proposes constructions and derivations. Before any of them is
allowed to count as progress, it goes through the same three wrong-approach
detectors every experiment in this repo uses (parity-only, Sha-finiteness
assumed in the open regime, function-field mirage). This module is a thin wrap
around experiments._shared.controls. It never reimplements a detector; it only
adapts the engine's Method / ProofEdge shapes to the detector signatures and
collapses the three verdicts into one clean / not-clean flag.

WHY a wrapper and not direct calls: the proof graph stores detector_audit
metadata on each edge as three booleans, and a proposed Method carries its own
risk profile. Both need to be checked against the SAME controls so the audit is
consistent whether it comes from a stored edge or a freshly proposed method.
The control curve for the Sha check defaults to the open-regime control (389a1)
so an unspecified method is judged in the regime where the wall actually bites.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from experiments._shared import (
    parity_detector,
    sha_finiteness_flag,
    function_field_mirage,
    control_pair,
)
from experiments._shared.elliptic_curve import EllipticCurve

from .graph import ProofGraph


@dataclass
class Method:
    """A proposed construction or argument, with its self-declared risk profile.

    The booleans are the method's HONEST description of what it leans on. A
    method that claims the full rank from the root number alone sets both
    claims_full_rank and uses_only_root_number; the parity detector then fires.
    """

    name: str
    claims_full_rank: bool = False
    uses_only_root_number: bool = False
    assumes_sha_finite: bool = False
    target_regime: str = "rank_ge2"
    uses_geometric_frobenius: bool = False
    needs_base_curve: bool = False


@dataclass
class AuditVerdict:
    method: str
    parity_only: bool
    sha_message: str
    function_field_flagged: bool
    clean: bool
    messages: List[str] = field(default_factory=list)


def audit_method(
    m: Method, analytic_rank: int = 2, E: Optional[EllipticCurve] = None
) -> AuditVerdict:
    """Run a proposed method past the three detectors and return one verdict.

    parity via parity_detector, Sha via sha_finiteness_flag against E (or the
    open-regime control curve when E is None), function field via
    function_field_mirage. clean is True iff no wall is hit: not parity-only,
    not function-field-flagged, and Sha-finiteness is not assumed in the open
    regime (analytic_rank >= 2).
    """
    parity = parity_detector(m.claims_full_rank, m.uses_only_root_number)

    curve = E if E is not None else control_pair().open_
    sha = sha_finiteness_flag(curve, analytic_rank, m.assumes_sha_finite)

    ff_message = function_field_mirage(m.uses_geometric_frobenius, m.needs_base_curve)
    ff_flagged = ff_message.startswith("FUNCTION-FIELD MIRAGE")

    sha_wall = sha.assumed and not sha.in_proven_regime

    clean = (not parity.is_parity_only) and (not ff_flagged) and (not sha_wall)

    return AuditVerdict(
        method=m.name,
        parity_only=parity.is_parity_only,
        sha_message=sha.message,
        function_field_flagged=ff_flagged,
        clean=clean,
        messages=[parity.message, sha.message, ff_message],
    )


def audit_edge(graph: ProofGraph, edge_key: str) -> AuditVerdict:
    """Derive an AuditVerdict from a stored edge's detector_audit metadata.

    The edge's three booleans say what the underlying theorem secretly relies
    on. We translate them into a Method with the matching risk profile and run
    the same audit_method, judged in the regime of the edge's conclusion node
    (rank >= 2 unless the conclusion is pinned to rank 0 / rank 1).
    """
    edge = graph.edges[edge_key]
    audit = edge.detector_audit or {}

    conclusion_regime = "rank_ge2"
    if graph.has(edge.conclusion):
        conclusion_regime = graph.node(edge.conclusion).regime

    # Map the conclusion regime to a representative analytic rank for the Sha
    # check: rank0 -> 0, rank1 -> 1, anything else (rank_ge2 / all) -> 2 so the
    # open-regime wall is the default, matching the honesty discipline.
    regime_to_rank = {"rank0": 0, "rank1": 1}
    analytic_rank = regime_to_rank.get(conclusion_regime, 2)

    # A stored parity_only flag means the edge's justification, taken alone,
    # delivers only parity. Encode that as a full-rank claim resting on w.
    parity_only = bool(audit.get("parity_only"))

    m = Method(
        name=f"edge:{edge_key}",
        claims_full_rank=parity_only,
        uses_only_root_number=parity_only,
        assumes_sha_finite=bool(audit.get("sha_assumed")),
        target_regime=conclusion_regime,
        uses_geometric_frobenius=bool(audit.get("function_field")),
        needs_base_curve=bool(audit.get("function_field")),
    )
    return audit_method(m, analytic_rank=analytic_rank)
