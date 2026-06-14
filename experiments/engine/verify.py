"""VERIFY: turn a frontier node into a typed Lean obligation, not a proof.

The last operator of the loop. Its honest job, exactly as the design doc states,
is to emit a Lean STATEMENT for an open frontier node against Mathlib's elliptic
-curve API, in the style of the existing lean/BSD skeleton, so the open object
becomes a concrete `sorry` target a human (or a future automated tactic) can
attack. Only a discharged Lean obligation, checked by `lake build` with a real
construction in hand, moves a node from open to proven. VERIFY closes nothing; it
states precisely what would have to be closed.

What it produces:

  - one LeanObligation per open rank >= 2 frontier node, carrying the node's
    regime and status, the frontier support set the engine computed for it (the
    provenance: what would discharge it), and a Lean theorem signature that
    references ONLY identifiers that exist in the skeleton (analyticRank,
    mordellWeilRank, leadingCoefficient, realPeriod, regulator, tamagawaProduct,
    shaOrder, torsionOrder, RationalEC);
  - a complete Lean file (write_lean_file) of those obligations as `sorry`
    theorems in `namespace BSD`, each with a doc comment giving its engine
    provenance. engine_rankTwoObject_obligation corresponds to the existing
    `BSD.rankTwoCertificate`, closing the round trip: the engine's computed
    frontier object IS the sorry the skeleton already declares.

Honesty guardrails, load-bearing:
  - every emitted theorem body is `sorry`; VERIFY never writes a closed proof;
  - a node whose statement cannot yet be expressed against the skeleton API (a
    finiteness claim with no Tate-Shafarevich type in the skeleton) is reported
    as PENDING, not faked into a theorem that references a nonexistent name;
  - the emitted file is NOT compiler-verified by this module. Discharge, and even
    typechecking, require `lake build` with Mathlib, which is the explicit next
    step, never claimed done here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .frontier import support_sets
from .graph import ProofGraph


# Goal templates for the open nodes that CAN be stated against the skeleton API.
# Each value is (lean_name, goal_text). The goal references only identifiers that
# exist in lean/BSD (see EllipticCurveDefs / LFunction / MordellWeil / StrongBSD).
_LEAN_GOALS: Dict[str, "tuple[str, str]"] = {
    "rank_two_object": (
        "engine_rankTwoObject_obligation",
        "2 ≤ mordellWeilRank E",
    ),
    "weak_bsd_rank_ge2": (
        "engine_weakBSD_rankGe2_obligation",
        "analyticRank E = mordellWeilRank E",
    ),
    "strong_bsd_rank_ge2": (
        "engine_strongBSD_rankGe2_obligation",
        "leadingCoefficient E\n"
        "      = (realPeriod E * regulator E * (tamagawaProduct E : ℝ) "
        "* (shaOrder E : ℝ))\n"
        "        / ((torsionOrder E : ℝ) ^ 2)",
    ),
}

# Open nodes the engine knows but the skeleton API cannot yet express. Honest:
# we do NOT emit a theorem referencing a type that does not exist.
_PENDING: Dict[str, str] = {
    "finite_sha_rank_ge2": (
        "no Tate-Shafarevich TYPE in the skeleton (only shaOrder : Nat presupposing "
        "finiteness), so finiteness is not yet expressible. Pending a `Sha` type."
    ),
}

# Cross-references to existing named targets in the skeleton, for the doc comment.
_CORRESPONDS: Dict[str, str] = {
    "rank_two_object": "BSD.rankTwoCertificate",
    "weak_bsd_rank_ge2": "BSD.weakBSD (open regime)",
    "strong_bsd_rank_ge2": "BSD.strongBSD (open regime)",
}

_DEFAULT_NODES = [
    "rank_two_object",
    "weak_bsd_rank_ge2",
    "finite_sha_rank_ge2",
    "strong_bsd_rank_ge2",
]


@dataclass
class LeanObligation:
    node_key: str
    regime: str
    status: str
    support: List[List[str]]          # the frontier support sets (provenance)
    lean_name: Optional[str]          # None when pending
    goal: Optional[str]               # the Lean goal text, None when pending
    corresponds_to: str = ""
    pending: bool = False
    pending_reason: str = ""
    body: str = "sorry"               # always sorry in v0; never a closed proof


def emit_obligations(graph: ProofGraph,
                     node_keys: Optional[List[str]] = None) -> List[LeanObligation]:
    """Emit a Lean obligation per open frontier node.

    For each node: read its regime/status from the graph, compute its frontier
    support set for provenance, and either build a Lean goal (if the skeleton API
    can express it) or mark it pending. Never emits a theorem for a node it cannot
    state honestly, and never emits a non-sorry body.
    """
    keys = node_keys if node_keys is not None else _DEFAULT_NODES
    obligations: List[LeanObligation] = []
    for key in keys:
        if not graph.has(key):
            continue
        node = graph.node(key)
        support = [sorted(s) for s in support_sets(graph, key)]
        if key in _PENDING:
            obligations.append(LeanObligation(
                node_key=key, regime=node.regime, status=node.status,
                support=support, lean_name=None, goal=None,
                pending=True, pending_reason=_PENDING[key],
            ))
            continue
        lean_name, goal = _LEAN_GOALS[key]
        obligations.append(LeanObligation(
            node_key=key, regime=node.regime, status=node.status,
            support=support, lean_name=lean_name, goal=goal,
            corresponds_to=_CORRESPONDS.get(key, ""),
        ))
    return obligations


def _theorem_block(graph: ProofGraph, obl: LeanObligation) -> str:
    """One Lean theorem with a doc comment carrying the engine provenance."""
    node = graph.node(obl.node_key)
    support_str = "; ".join("{ " + ", ".join(s) + " }" for s in obl.support)
    corresponds = (f"\n    Corresponds to `{obl.corresponds_to}`."
                   if obl.corresponds_to else "")
    doc = (
        f"/-- Engine node `{obl.node_key}` (regime {obl.regime}, status "
        f"{obl.status}).\n"
        f"    {node.statement}\n"
        f"    Frontier support set (what would discharge it): {support_str}.\n"
        f"    Discharge: a construction or proof, checked by `lake build`; only "
        f"then does the node become proven.{corresponds} -/"
    )
    return (
        f"{doc}\n"
        f"theorem {obl.lean_name} (E : RationalEC) (_h : 2 ≤ analyticRank E) :\n"
        f"    {obl.goal} := by\n"
        f"  sorry"
    )


def theorem_text(graph: ProofGraph, obligation: LeanObligation) -> str:
    """Public accessor for one obligation's Lean theorem block (driver excerpts)."""
    return _theorem_block(graph, obligation)


_HEADER = """/-
  Engine-emitted BSD obligations (generated by experiments/engine/verify.py).

  These are STATEMENTS, not proofs. Each theorem below is a `sorry` whose
  discharge (a real construction, checked by `lake build` against Mathlib) would
  move the corresponding engine proof-graph node from `open` to `proven`. No
  theorem here is claimed proven; this mirrors the skeleton's stance.

  Each obligation cites its engine node key, regime, and the frontier support set
  the engine computed. `engine_rankTwoObject_obligation` restates the open
  frontier object and corresponds to `BSD.rankTwoCertificate`.
-/

import BSD.StrongBSD

namespace BSD
"""


def lean_file_text(graph: ProofGraph, obligations: List[LeanObligation]) -> str:
    """Assemble the full Lean file from the emittable (non-pending) obligations."""
    blocks = [_theorem_block(graph, o) for o in obligations if not o.pending]
    pending = [o for o in obligations if o.pending]
    body = "\n\n".join(blocks)
    pend_note = ""
    if pending:
        lines = [f"-- PENDING (not emitted as theorems, no skeleton API yet):"]
        for o in pending:
            lines.append(f"--   {o.node_key}: {o.pending_reason}")
        pend_note = "\n\n" + "\n".join(lines)
    return f"{_HEADER}\n{body}{pend_note}\n\nend BSD\n"


def write_lean_file(graph: ProofGraph, path: str,
                    node_keys: Optional[List[str]] = None) -> List[LeanObligation]:
    """Emit obligations and write the Lean file. Returns the obligations."""
    obligations = emit_obligations(graph, node_keys)
    text = lean_file_text(graph, obligations)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return obligations


def report(obligations: List[LeanObligation]) -> str:
    """Per-obligation status and the honest, nothing-proven summary."""
    lines: List[str] = []
    lines.append("VERIFY: Lean obligations emitted from the frontier")
    lines.append("=" * 78)
    emitted = [o for o in obligations if not o.pending]
    pending = [o for o in obligations if o.pending]
    for o in emitted:
        support_str = "; ".join("{ " + ", ".join(s) + " }" for s in o.support)
        lines.append(f"  [SORRY] {o.lean_name}")
        lines.append(f"          node {o.node_key} (regime {o.regime}, status {o.status})")
        lines.append(f"          support: {support_str}")
        if o.corresponds_to:
            lines.append(f"          corresponds to {o.corresponds_to}")
    for o in pending:
        lines.append(f"  [PENDING] {o.node_key}: {o.pending_reason}")
    lines.append("-" * 78)
    lines.append(f"  emitted as sorry: {len(emitted)}   pending API: {len(pending)}"
                 f"   proven: 0")
    lines.append("  Every obligation is a sorry. Discharge requires `lake build`")
    lines.append("  with a real construction; nothing here is proven.")
    return "\n".join(lines)


if __name__ == "__main__":
    # Run: python -m experiments.engine.verify
    # Builds the atlas graph, emits obligations, writes the Lean file, self-checks.
    import os
    from .atlas_graph import build_atlas_graph

    graph = build_atlas_graph()
    obligations = emit_obligations(graph)
    by_node = {o.node_key: o for o in obligations}

    # The frontier object must be emitted and must be a sorry, never proven.
    rt = by_node["rank_two_object"]
    assert not rt.pending and rt.body == "sorry", "rank_two_object must be an open sorry"
    assert "mordellWeilRank" in rt.goal, "the obligation must reference the MW rank"
    # finite Sha must be pending (honest: no Sha type in the skeleton).
    assert by_node["finite_sha_rank_ge2"].pending, "finite Sha has no skeleton API yet"
    # The whole file must be sorry-only and reference real identifiers.
    text = lean_file_text(graph, obligations)
    assert "sorry" in text and "namespace BSD" in text and "analyticRank" in text
    assert "theorem engine_rankTwoObject_obligation" in text

    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    lean_path = os.path.join(here, "lean", "BSD", "EngineObligations.lean")
    write_lean_file(graph, lean_path)

    print("verify self-test OK")
    print(f"wrote {lean_path}")
    print()
    print(report(obligations))
