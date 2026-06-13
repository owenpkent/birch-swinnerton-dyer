"""Typed proof graph: the BSD research atlas rendered as data.

The atlas (docs/research_atlas) is a prose catalog of what is proven, what is
conditional, and what is open across the rank 0 / rank 1 / rank >= 2 regimes.
This module turns that catalog into a directed AND/OR graph the engine can
search. A ProofNode is a regime-pinned claim with a status; a ProofEdge is a
theorem that derives one node from an AND-set of premise nodes. The point of
making it data is mechanical honesty: "is this claim actually established?"
becomes a graph reachability question, not a paragraph of prose, and the
parity wall can be encoded structurally rather than remembered.

The load-bearing modelling rule: PARITY IS ITS OWN NODE. The root number gives
the rank mod 2 (proven via modularity), but there is deliberately no edge from
a parity node to a full-rank node. So when the engine asks what would establish
weak BSD in rank >= 2, the answer never routes through parity. The graph
structure itself encodes that parity is insufficient.

The three detector booleans on each edge (parity_only, sha_assumed,
function_field) are descriptive metadata. They say what an edge SECRETLY relies
on. They do NOT gate traversal: an edge with sha_assumed=True still establishes
its conclusion in the graph sense. The flags are surfaced separately by
audit.py and frontier.py so a reader sees which wall each derivation path hits.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


# Regime strings. The whole engine pins every claim to one of these.
REGIMES = ("rank0", "rank1", "rank_ge2", "all")

# Status strings. "proven" is self-establishing; the others need an edge.
STATUSES = ("proven", "conditional", "open", "refuted")


@dataclass(frozen=True)
class ProofNode:
    """A single regime-pinned claim in the atlas.

    status semantics:
      proven      -- established on its own (a theorem in this regime).
      conditional -- holds modulo the nodes named in depends_on.
      open         -- not known; only an edge can establish it in-graph.
      refuted     -- known false; never establishes anything.
    """

    key: str
    statement: str
    regime: str
    status: str
    provenance: str = ""
    depends_on: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.regime not in REGIMES:
            raise ValueError(
                f"node {self.key!r}: regime {self.regime!r} not in {REGIMES}"
            )
        if self.status not in STATUSES:
            raise ValueError(
                f"node {self.key!r}: status {self.status!r} not in {STATUSES}"
            )


@dataclass(frozen=True)
class ProofEdge:
    """A theorem deriving `conclusion` from the AND-set `premises`.

    premises is the conjunction of node keys the theorem needs. An empty tuple
    marks an axiom or an externally-known input (the edge fires unconditionally).
    detector_audit is descriptive only; see the module docstring.
    """

    key: str
    premises: Tuple[str, ...]
    conclusion: str
    justification: str
    detector_audit: Dict[str, bool] = field(default_factory=dict)


class ProofGraph:
    """A mutable collection of nodes and edges with established-ness queries.

    The single nontrivial query is is_established: a node counts as established
    if it is itself proven, or if some incoming edge has all of its premises
    established. The recursion is made cycle-safe by tracking the set of nodes
    currently mid-evaluation and treating any such node as not-yet-established.
    """

    def __init__(self) -> None:
        self.nodes: Dict[str, ProofNode] = {}
        self.edges: Dict[str, ProofEdge] = {}

    # -- construction ------------------------------------------------------

    def add_node(self, node: ProofNode) -> None:
        if node.key in self.nodes:
            raise ValueError(f"duplicate node key {node.key!r}")
        self.nodes[node.key] = node

    def add_edge(self, edge: ProofEdge) -> None:
        if edge.key in self.edges:
            raise ValueError(f"duplicate edge key {edge.key!r}")
        self.edges[edge.key] = edge

    # -- lookups -----------------------------------------------------------

    def node(self, key: str) -> ProofNode:
        return self.nodes[key]

    def has(self, key: str) -> bool:
        return key in self.nodes

    def incoming(self, key: str) -> List[ProofEdge]:
        """All edges whose conclusion is `key`, in insertion order."""
        return [e for e in self.edges.values() if e.conclusion == key]

    # -- the one real query ------------------------------------------------

    def is_established(self, key: str) -> bool:
        """True iff `key` is a proven node or is derivable from proven nodes.

        Cycle-safe: a node reached again while already on the recursion stack
        is treated as not-yet-established for that branch, so a derivation may
        not lean on itself. Only status=="proven" is self-establishing; a
        conditional / open / refuted node needs a sound incoming edge whose
        premises are all (recursively) established.
        """
        return self._established(key, in_progress=set())

    def _established(self, key: str, in_progress: set) -> bool:
        if key not in self.nodes:
            return False
        if self.nodes[key].status == "proven":
            return True
        if key in in_progress:
            # Mid-recursion: refuse to let the node justify itself.
            return False
        in_progress.add(key)
        try:
            for edge in self.incoming(key):
                if all(
                    self._established(p, in_progress) for p in edge.premises
                ):
                    return True
            return False
        finally:
            in_progress.discard(key)
