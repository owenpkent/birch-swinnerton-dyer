"""The BSD proof-search engine: a sound search loop over a typed proof graph.

This package is the load-bearing spine of a proof-search engine for the Birch
and Swinnerton-Dyer conjecture. It runs the loop FRONTIER / PROPOSE / AUDIT /
FALSIFY / LOCALIZE / VERIFY. FRONTIER computes the minimal sets of open claims
that would establish a target (frontier.support_sets); PROPOSE supplies a
candidate construction as a Method; AUDIT runs that method and every proof edge
past the three wrong-approach detectors that serve as the soundness oracle
(audit.audit_method, audit.audit_edge, wrapping experiments._shared.controls:
parity-only, Sha-finiteness assumed in the open regime, function-field mirage);
FALSIFY and LOCALIZE then narrow where a claim breaks, and VERIFY checks what
survives. The whole thing rests on a typed AND/OR proof graph (graph.ProofGraph)
in which parity is a node distinct from any full-rank claim with no edge between
them, so the parity wall is structural rather than merely remembered. Nothing
here claims more than it proves: every node is pinned to a rank regime and a
proven / conditional / open / refuted status.
"""

from .graph import ProofNode, ProofEdge, ProofGraph
from .frontier import support_sets, leverage, report
from .audit import Method, AuditVerdict, audit_method, audit_edge

__all__ = [
    "ProofNode",
    "ProofEdge",
    "ProofGraph",
    "support_sets",
    "leverage",
    "report",
    "Method",
    "AuditVerdict",
    "audit_method",
    "audit_edge",
]
