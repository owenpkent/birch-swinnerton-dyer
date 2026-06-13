"""Frontier analysis: what is the minimal open thing to assume?

Given a target claim (say weak BSD in rank >= 2), this module computes the
support sets: the minimal sets of currently-NON-established nodes such that,
if each of them were granted, the target would become established. This is the
AND/OR dual of is_established. is_established asks "is it proven now"; support
sets ask "what is the smallest set of open frontiers that would finish it".

Why this is the engine's core: it converts the prose question "where is the
frontier of BSD" into a concrete antichain of node-sets, and the leverage
ranking tells you which open node shows up across the most independent paths
(the highest-value target to attack). Because parity is its own node with no
edge into the full-rank claims (see graph.py), no support set for weak BSD in
rank >= 2 ever reduces to "just assume parity". The wall is visible in the data.

AND/OR semantics, made precise:
  - If the target is already established, the only support set is the empty set
    (nothing more is needed). Returned as [frozenset()].
  - For a node n that is established, supports(n) = {frozenset()}.
  - For a node n that is NOT established:
      take the union, over every incoming edge e, of the cartesian set-union
      of supports(p) across the AND-premises p of e. A premise with no premises
      (axiom edge) contributes {frozenset()}, the identity for set-union.
      THEN, if n has no incoming edge that could ever establish it, n must be
      assumed itself, contributing {frozenset({n})}.
  - Finally reduce to the minimal antichain: drop any set that is a superset of
    another set in the collection.

Cycle safety: a node revisited while already on the recursion stack contributes
no support sets from that branch (an empty collection, the identity for the
OR-union), so a support can never lean on itself.
"""

from __future__ import annotations

from itertools import product
from typing import Dict, FrozenSet, List

from .graph import ProofGraph


def _cartesian_union(
    premise_supports: List[List[FrozenSet[str]]],
) -> List[FrozenSet[str]]:
    """Combine AND-premises: one choice of support set per premise, unioned.

    Each premise contributes a list of candidate support sets (its OR-options).
    A conjunction is satisfied by picking one option from each premise and
    taking their union. The empty conjunction yields {frozenset()} (the axiom
    edge: nothing needs assuming). If any premise contributes no options at all
    (e.g. a cycle cut it off), the whole conjunction is unsatisfiable: return [].
    """
    if not premise_supports:
        return [frozenset()]
    if any(len(opts) == 0 for opts in premise_supports):
        return []
    combined: List[FrozenSet[str]] = []
    for choice in product(*premise_supports):
        merged: FrozenSet[str] = frozenset().union(*choice)
        combined.append(merged)
    return combined


def _minimal_antichain(sets: List[FrozenSet[str]]) -> List[FrozenSet[str]]:
    """Keep only the sets that are not supersets of some other set.

    Deduplicates, then drops any set strictly or non-strictly containing
    another distinct set. The result is sorted for stable output: by size,
    then lexicographically by sorted contents.
    """
    unique = set(sets)
    minimal: List[FrozenSet[str]] = []
    for s in unique:
        if any(other < s for other in unique if other != s):
            continue
        minimal.append(s)
    return sorted(minimal, key=lambda s: (len(s), sorted(s)))


def _can_ever_establish(graph: ProofGraph, key: str) -> bool:
    """Does this node have any incoming edge at all (a potential derivation)?

    A node with no incoming edge can only be made established by being assumed
    directly, so it is itself a frontier leaf.
    """
    return len(graph.incoming(key)) > 0


def _supports(
    graph: ProofGraph, key: str, in_progress: set, memo: dict
) -> List[FrozenSet[str]]:
    if graph.is_established(key):
        return [frozenset()]
    if key in in_progress:
        # Cycle cut: this branch contributes nothing (identity for OR-union).
        return []
    if key in memo:
        return memo[key]

    in_progress.add(key)
    try:
        collected: List[FrozenSet[str]] = []
        for edge in graph.incoming(key):
            premise_supports = [
                _supports(graph, p, in_progress, memo) for p in edge.premises
            ]
            collected.extend(_cartesian_union(premise_supports))

        # A node with no establishing edge must be assumed itself.
        if not _can_ever_establish(graph, key):
            collected.append(frozenset({key}))

        result = _minimal_antichain(collected)
    finally:
        in_progress.discard(key)

    # Memoize the result. For an acyclic graph (the atlas is a DAG) this is
    # exact. If cycles are ever added, a memo entry computed while a branch was
    # cycle-truncated could understate the supports a different call stack would
    # see; revisit this memo policy at that point.
    memo[key] = result
    return result


def support_sets(graph: ProofGraph, target_key: str) -> List[FrozenSet[str]]:
    """Minimal sets of non-established nodes that would establish the target.

    Returns a sorted, minimal, deduplicated list of frozensets. If the target
    is already established, returns [frozenset()] (nothing to assume). If the
    target can never be established (no path of edges reaching proven leaves),
    returns the frontier leaves that would have to be assumed.
    """
    # Fresh memo per call: the in_progress set differs per traversal, and a
    # shared memo across targets could cache a cycle-truncated branch.
    return _supports(graph, target_key, in_progress=set(), memo={})


def leverage(graph: ProofGraph, target_key: str) -> Dict[str, int]:
    """How many support sets each frontier node appears in.

    A node with high leverage sits on many independent routes to the target, so
    proving it unlocks the most. Returned sorted by descending leverage, then
    by node key for stability.
    """
    sets = support_sets(graph, target_key)
    counts: Dict[str, int] = {}
    for s in sets:
        for node in s:
            counts[node] = counts.get(node, 0) + 1
    return dict(
        sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    )


def _edges_supporting(
    graph: ProofGraph, target_key: str, support: FrozenSet[str]
) -> List[str]:
    """Edge keys that actually participate in deriving target from this support.

    An edge can fire once every premise is satisfiable: either already
    established, in the assumed support set, or itself derivable under the same
    support. We collect, by backward reachability from the target, only those
    firing edges. This is what lets the report distinguish a CLEAN derivation
    (the rank-two construction edge) from one that brushes a detector wall,
    rather than ORing over every edge in the graph regardless of relevance.
    """

    def satisfiable(key: str, seen: set) -> bool:
        if graph.is_established(key) or key in support:
            return True
        if key in seen:
            return False
        seen.add(key)
        return any(
            all(satisfiable(p, seen) for p in e.premises)
            for e in graph.incoming(key)
        )

    firing: List[str] = []
    stack = [target_key]
    visited: set = set()
    while stack:
        key = stack.pop()
        if key in visited:
            continue
        visited.add(key)
        for edge in graph.incoming(key):
            if all(satisfiable(p, set()) for p in edge.premises):
                firing.append(edge.key)
                stack.extend(edge.premises)
    return firing


def _edge_flags_for_path(
    graph: ProofGraph, target_key: str, support: FrozenSet[str]
) -> Dict[str, bool]:
    """OR the detector flags of only the edges that derive target from support.

    Restricted to the edges that actually fire under this support set (backward
    reachability from the target), so a derivation whose firing edges are all
    clean reports no wall. It tells the reader whether THIS derivation brushes
    parity / Sha / function field, not whether the wall exists somewhere in the
    graph. It is still a coarse OR across the firing edges, not a single path.
    """
    flags = {"parity_only": False, "sha_assumed": False, "function_field": False}
    for edge_key in _edges_supporting(graph, target_key, support):
        audit = graph.edges[edge_key].detector_audit or {}
        for k in flags:
            if audit.get(k):
                flags[k] = True
    return flags


def report(graph: ProofGraph, target_key: str) -> str:
    """Human-readable frontier report: support sets, detector flags, leverage."""
    lines: List[str] = []
    lines.append(f"Frontier report for target: {target_key}")
    if not graph.has(target_key):
        lines.append("  (no such node in the graph)")
        return "\n".join(lines)

    node = graph.node(target_key)
    lines.append(f"  statement: {node.statement}")
    lines.append(f"  regime:    {node.regime}    status: {node.status}")

    if graph.is_established(target_key):
        lines.append("  ESTABLISHED: derivable from proven nodes. No frontier to assume.")
        return "\n".join(lines)

    sets = support_sets(graph, target_key)
    lines.append("")
    lines.append(f"  {len(sets)} minimal support set(s) (assume all nodes in a set -> target holds):")
    for i, s in enumerate(sets, 1):
        members = ", ".join(sorted(s)) if s else "(empty)"
        lines.append(f"    [{i}] {{ {members} }}")
        flags = _edge_flags_for_path(graph, target_key, s)
        hit = [name for name, on in flags.items() if on]
        if hit:
            lines.append(f"        detector walls along graph edges: {', '.join(hit)}")
        else:
            lines.append("        detector walls along graph edges: none")

    lines.append("")
    lines.append("  leverage ranking (frontier node : # of support sets it appears in):")
    lev = leverage(graph, target_key)
    if not lev:
        lines.append("    (none)")
    for k, v in lev.items():
        lines.append(f"    {k} : {v}")

    return "\n".join(lines)


if __name__ == "__main__":
    # Toy graph self-test. Run: python -m experiments.engine.frontier
    #
    # Shape (-> means "edge concludes"):
    #   proven_a (proven)
    #   open_b   (open, no edge)        -- a frontier leaf
    #   open_c   (open, no edge)        -- a frontier leaf
    #   target   established by either:
    #              edge1: premises {proven_a, open_b}
    #              edge2: premises {open_c}
    #   so support sets = { {open_b}, {open_c} }  (proven_a drops out).
    #   parity   (proven) with NO edge to target -> never appears in any support.
    from .graph import ProofGraph, ProofNode, ProofEdge

    g = ProofGraph()
    g.add_node(ProofNode("proven_a", "A is a theorem", "all", "proven", "toy"))
    g.add_node(ProofNode("open_b", "B is open", "rank_ge2", "open", "toy"))
    g.add_node(ProofNode("open_c", "C is open", "rank_ge2", "open", "toy"))
    g.add_node(ProofNode("parity", "parity is known", "rank_ge2", "proven", "toy"))
    g.add_node(ProofNode("target", "the target claim", "rank_ge2", "open", "toy"))

    g.add_edge(ProofEdge(
        "edge1", ("proven_a", "open_b"), "target", "toy theorem 1",
        {"parity_only": False, "sha_assumed": False, "function_field": False},
    ))
    g.add_edge(ProofEdge(
        "edge2", ("open_c",), "target", "toy theorem 2",
        {"parity_only": False, "sha_assumed": True, "function_field": False},
    ))

    assert g.is_established("proven_a") is True, "proven node must be established"
    assert g.is_established("open_b") is False, "open node with no edge is not established"
    assert g.is_established("target") is False, "target rests on open premises"

    sets = support_sets(g, "target")
    expected = {frozenset({"open_b"}), frozenset({"open_c"})}
    assert set(sets) == expected, f"got {set(sets)}, expected {expected}"

    # parity is proven but disconnected: it must not appear in any support set.
    assert all("parity" not in s for s in sets), "parity must not route into target"

    lev = leverage(g, "target")
    assert lev == {"open_b": 1, "open_c": 1}, f"unexpected leverage {lev}"

    # An already-established target reduces to the empty support.
    g.add_node(ProofNode("done", "trivially proven", "all", "proven", "toy"))
    assert support_sets(g, "done") == [frozenset()], "proven target -> empty support"

    print("frontier self-test OK")
    print()
    print(report(g, "target"))
