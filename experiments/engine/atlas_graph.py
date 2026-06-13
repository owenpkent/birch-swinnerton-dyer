"""The BSD research atlas rendered as a typed AND/OR proof graph.

This module is the single place the engine's structural honesty lives. It turns
the prose scorecard in docs/research_atlas/README.md into ProofNodes (regime-
pinned claims with a proven / conditional / open / refuted status) and ProofEdges
(theorems deriving one node from an AND-set of premises). Once the atlas is data,
the question "is weak BSD in rank >= 2 actually established?" is a graph
reachability query, and the frontier of BSD is a concrete antichain of open
node-sets rather than a remembered paragraph.

WHY this module and not a hand-written graph in some driver: the modelling choice
that makes the parity wall STRUCTURAL has to be enforced in exactly one place so
it cannot drift. That choice is: parity is its own node (parity_rank0/1/ge2,
proven from modularity plus the parity conjecture) and there is deliberately NO
edge from any parity node into a full-rank weak/strong BSD node. So when
frontier.support_sets is asked what would finish weak_bsd_rank_ge2, no support
set ever collapses to "just assume parity". The insufficiency of parity is
encoded in the wiring, not in a comment.

The regimes split every claim into rank0 / rank1 (the PROVEN regime, Coates-Wiles
and Gross-Zagier + Kolyvagin) and rank_ge2 (the OPEN regime). The proven-regime
weak BSD and finite-Sha nodes are status "proven" and self-establish. The open-
regime nodes are status "open" and bottom out at frontier leaves with no incoming
edge (the missing rank >= 2 construction and the missing higher Euler system), so
they surface as the frontier the engine reports. The detector_audit booleans on
each edge are descriptive metadata (what the edge SECRETLY leans on); they do not
gate traversal, they are surfaced by audit.py and frontier.report.
"""

from __future__ import annotations

from .graph import ProofEdge, ProofGraph, ProofNode


# Detector-audit shorthands. Every edge declares what it secretly relies on so
# audit.py and frontier.report can show which wall a derivation path brushes.
# A fresh dict is passed per edge (dict(...)) so no two edges share one mutable.
_CLEAN = {"parity_only": False, "sha_assumed": False, "function_field": False}
_PARITY = {"parity_only": True, "sha_assumed": False, "function_field": False}
_SHA = {"parity_only": False, "sha_assumed": True, "function_field": False}
_FUNCTION_FIELD = {"parity_only": False, "sha_assumed": True, "function_field": True}


def build_atlas_graph() -> ProofGraph:
    """Construct the BSD atlas as a ProofGraph.

    Returns a graph whose proven leaves are the genuine theorems (modularity,
    the parity conjecture, the rank 0 / rank 1 Coates-Wiles and Gross-Zagier +
    Kolyvagin results) and whose open targets are weak and strong BSD in rank
    >= 2. The wiring enforces that parity does not route into any full-rank claim.
    """
    g = ProofGraph()

    # ---------------------------------------------------------------------
    # Background theorems over Q (regime "all"): modularity and the parity
    # conjecture. Both proven, both self-establishing. What they CANNOT do is
    # encoded by the edges: modularity reaches only the parity nodes.
    # ---------------------------------------------------------------------
    g.add_node(ProofNode(
        "modularity",
        "Every E/Q is modular: L(E,s) continues to C with a functional "
        "equation and a root number w (Wiles; Taylor-Wiles; BCDT 2001).",
        "all", "proven", "Wiles 1995; Taylor-Wiles 1995; BCDT 2001",
    ))
    g.add_node(ProofNode(
        "parity_conjecture",
        "Mordell-Weil rank mod 2 equals analytic rank mod 2 (the parity "
        "conjecture, now a theorem).",
        "all", "proven", "Nekovar; T. and V. Dokchitser",
    ))

    # ---------------------------------------------------------------------
    # Parity nodes, one per regime. Each says ONLY rank mod 2. Proven (the root
    # number gives analytic rank mod 2, the parity conjecture upgrades it to
    # Mordell-Weil rank mod 2), but by design NO edge runs from any of these
    # into a weak_bsd_* node.
    # ---------------------------------------------------------------------
    for regime in ("rank0", "rank1", "rank_ge2"):
        g.add_node(ProofNode(
            f"parity_{regime}",
            f"Analytic-rank parity (rank mod 2 only) in regime {regime}: "
            "w = (-1)^r determines rank mod 2, never the rank itself.",
            regime, "proven", "modularity root number + parity conjecture",
        ))

    # ---------------------------------------------------------------------
    # Weak BSD (rank equality ord_{s=1} L = rank E(Q)), per regime.
    # rank 0 and rank 1 are proven; rank >= 2 is open.
    # ---------------------------------------------------------------------
    g.add_node(ProofNode(
        "weak_bsd_rank0",
        "ord_{s=1} L(E,s) = rank E(Q) in analytic rank 0.",
        "rank0", "proven", "Coates-Wiles (CM); Kolyvagin",
    ))
    g.add_node(ProofNode(
        "weak_bsd_rank1",
        "ord_{s=1} L(E,s) = rank E(Q) in analytic rank 1.",
        "rank1", "proven", "Gross-Zagier 1986 + Kolyvagin 1990",
    ))
    g.add_node(ProofNode(
        "weak_bsd_rank_ge2",
        "ord_{s=1} L(E,s) = rank E(Q) in analytic rank >= 2. OPEN.",
        "rank_ge2", "open", "OPEN: the missing higher-rank construction",
    ))

    # ---------------------------------------------------------------------
    # Finiteness of Sha, per regime. Proven for rank <= 1, open for rank >= 2.
    # ---------------------------------------------------------------------
    g.add_node(ProofNode(
        "finite_sha_rank_le1",
        "#Sha(E/Q) is finite for analytic rank <= 1.",
        "rank1", "proven", "Gross-Zagier + Kolyvagin 1990",
    ))
    g.add_node(ProofNode(
        "finite_sha_rank_ge2",
        "#Sha(E/Q) is finite for analytic rank >= 2. OPEN.",
        "rank_ge2", "open", "OPEN: the central missing finiteness",
    ))

    # ---------------------------------------------------------------------
    # Strong BSD (the leading-coefficient formula), per regime.
    # rank 0: conditional/partial (p-part for many p via Skinner-Urban).
    # rank 1: partial. rank >= 2: open. The depends_on tuple records the bridge
    # node the conditional nodes lean on.
    # ---------------------------------------------------------------------
    g.add_node(ProofNode(
        "strong_bsd_rank0",
        "Strong BSD leading-coefficient formula in analytic rank 0; p-part "
        "known for many p, full formula partial.",
        "rank0", "conditional",
        "Skinner-Urban 2014 (p-part, many p); partial in general",
        depends_on=("iwasawa_main_conjecture",),
    ))
    g.add_node(ProofNode(
        "strong_bsd_rank1",
        "Strong BSD leading-coefficient formula in analytic rank 1; partial "
        "(p-part for many p).",
        "rank1", "conditional",
        "Kato + Skinner-Urban (p-part); partial",
        depends_on=("iwasawa_main_conjecture",),
    ))
    g.add_node(ProofNode(
        "strong_bsd_rank_ge2",
        "Strong BSD leading-coefficient formula in analytic rank >= 2. OPEN.",
        "rank_ge2", "open",
        "OPEN: needs both rank equality and finite Sha in the open regime",
    ))

    # ---------------------------------------------------------------------
    # The proven rank <= 1 engines. heegner_point outputs ONE point (a rank-1
    # object); kolyvagin_euler_system bounds the Selmer group from that single
    # non-torsion seed. Both proven, both capped at one degree of freedom.
    # ---------------------------------------------------------------------
    g.add_node(ProofNode(
        "heegner_point",
        "The Heegner point construction: outputs ONE point on E (a rank <= 1 "
        "object), non-torsion exactly when L'(E,1) != 0.",
        "rank1", "proven", "Gross-Zagier 1986",
    ))
    g.add_node(ProofNode(
        "kolyvagin_euler_system",
        "Kolyvagin's Euler system: from one non-torsion Heegner point, bounds "
        "Sel_p(E/K) and forces rank 1 with finite Sha (analytic rank <= 1 only).",
        "rank1", "proven", "Kolyvagin 1990",
    ))

    # ---------------------------------------------------------------------
    # The open objects the program is missing. These have NO incoming edge:
    # they are frontier leaves. The frontier query for weak_bsd_rank_ge2 must
    # bottom out here, which is the whole point of the cross-cutting thesis.
    # ---------------------------------------------------------------------
    g.add_node(ProofNode(
        "rank_two_object",
        "Direction-01 construction: on a rank >= 2 curve, produce two provably "
        "independent rational points with det of the height regulator > 0. OPEN.",
        "rank_ge2", "open", "OPEN: research Direction 01 (BUILDER mandate)",
    ))
    g.add_node(ProofNode(
        "higher_euler_system",
        "Direction-02 construction: a rank >= 2 Euler system bounding Sha "
        "unconditionally in the open regime (no rank-1 Heegner ceiling). OPEN.",
        "rank_ge2", "open", "OPEN: research Direction 02",
    ))

    # ---------------------------------------------------------------------
    # The conditional p-adic bridge. The cyclotomic Iwasawa main conjecture for
    # GL2 (Kato divisibility + Skinner-Urban reverse divisibility) gives the
    # p-part of strong BSD one prime at a time, mostly in rank <= 1. Conditional:
    # it is the bridge the strong_bsd_rank0/1 nodes depend on.
    # ---------------------------------------------------------------------
    g.add_node(ProofNode(
        "iwasawa_main_conjecture",
        "Cyclotomic Iwasawa main conjecture for GL2: Ch(f) = (L_f), giving the "
        "p-part of strong BSD one prime at a time, mostly analytic rank <= 1.",
        "rank1", "conditional", "Kato; Skinner-Urban 2014", depends_on=(),
    ))

    # ---------------------------------------------------------------------
    # The function-field mirage template. Full BSD is a theorem over F_q(C)
    # under finite Brauer group / finite Sha (Tate, Artin-Tate, Milne), but its
    # proof imports a geometric Frobenius on a surface that has no number-field
    # analog. Included precisely as the mirage exhibit; its edge carries
    # function_field=True and concludes NOTHING over Q.
    # ---------------------------------------------------------------------
    g.add_node(ProofNode(
        "bsd_function_field",
        "Full BSD over F_q(C) (rank equality + leading-coefficient formula), "
        "rank-uniform, PROVEN under finite Brauer group / finite Sha.",
        "all", "proven", "Tate; Artin-Tate; Milne 1975",
    ))

    # =====================================================================
    # EDGES
    # =====================================================================

    # Modularity reaches ONLY parity in the open regime. This edge concludes
    # parity_rank_ge2 and nothing else. There is no edge parity_* -> weak_bsd_*,
    # so this derivation is a dead end toward full rank. The detector flag
    # records that the edge, taken alone, delivers only rank mod 2.
    g.add_edge(ProofEdge(
        "e_modularity_to_parity_ge2",
        ("modularity",),
        "parity_rank_ge2",
        "Functional-equation sign w = (-1)^r gives rank mod 2 (parity only). "
        "This is ALL the root number knows; no edge from here to full rank.",
        dict(_PARITY),
    ))

    # The proven rank-1 regime: the Heegner point plus Kolyvagin's Euler system
    # together give weak BSD and finite Sha in rank 1. Both premises proven, so
    # both conclusions are established; both edges clean.
    g.add_edge(ProofEdge(
        "e_gzk_to_weak_bsd_rank1",
        ("heegner_point", "kolyvagin_euler_system"),
        "weak_bsd_rank1",
        "Gross-Zagier height formula + Kolyvagin Euler system => rank equality "
        "(analytic rank 1).",
        dict(_CLEAN),
    ))
    g.add_edge(ProofEdge(
        "e_gzk_to_finite_sha_le1",
        ("heegner_point", "kolyvagin_euler_system"),
        "finite_sha_rank_le1",
        "Kolyvagin's bound on Sel_p from one non-torsion seed => #Sha finite "
        "(analytic rank <= 1).",
        dict(_CLEAN),
    ))

    # The open regime, structurally honest. weak BSD in rank >= 2 follows from
    # the missing rank-two construction (two independent points). Clean detector
    # flags: the construction, IF it existed, would deliver actual points; the
    # obstruction is that the premise is OPEN, not that the method is unsound.
    g.add_edge(ProofEdge(
        "e_rank_two_to_weak_bsd_ge2",
        ("rank_two_object",),
        "weak_bsd_rank_ge2",
        "Two provably independent rational points exhibit rank >= 2 "
        "(Direction 01). Premise is OPEN, so this does not yet fire.",
        dict(_CLEAN),
    ))

    # Finite Sha in rank >= 2 needs both the rank-two object and a higher-rank
    # Euler system bounding Sha. Both premises open; edge clean.
    g.add_edge(ProofEdge(
        "e_higher_system_to_finite_sha_ge2",
        ("rank_two_object", "higher_euler_system"),
        "finite_sha_rank_ge2",
        "A rank >= 2 Euler system bounds Sha unconditionally (Direction 02). "
        "Premises are OPEN, so this does not yet fire.",
        dict(_CLEAN),
    ))

    # Strong BSD in rank >= 2 from weak BSD plus finite Sha in that regime. The
    # Sha-finiteness here is a PREMISE NODE (finite_sha_rank_ge2), not an
    # assumption smuggled into the method, so sha_assumed is False: the wall is
    # already paid for by requiring the open finiteness node explicitly. All
    # three flags False.
    g.add_edge(ProofEdge(
        "e_weak_and_sha_to_strong_ge2",
        ("weak_bsd_rank_ge2", "finite_sha_rank_ge2"),
        "strong_bsd_rank_ge2",
        "Rank equality + finite Sha => leading-coefficient formula (rank >= 2). "
        "Finiteness is a premise node, not an assumption.",
        dict(_CLEAN),
    ))

    # The Iwasawa main conjecture supplies the p-part of strong BSD in rank 0
    # and rank 1. sha_assumed=True records the conditional bridge: the route to
    # #Sha[p^infty] runs through the main conjecture one prime at a time and
    # leans on a finiteness input.
    g.add_edge(ProofEdge(
        "e_iwasawa_to_strong_bsd_rank0",
        ("iwasawa_main_conjecture",),
        "strong_bsd_rank0",
        "Skinner-Urban: Ch(f) = (L_f) gives the p-part in rank 0 (many p).",
        dict(_SHA),
    ))
    g.add_edge(ProofEdge(
        "e_iwasawa_to_strong_bsd_rank1",
        ("iwasawa_main_conjecture",),
        "strong_bsd_rank1",
        "Kato + Skinner-Urban: p-part of strong BSD in rank 1 (partial).",
        dict(_SHA),
    ))

    # The function-field mirage. Full BSD over F_q(C) is proven, but the proof
    # imports a geometric Frobenius on a surface with no number-field analog.
    # This edge concludes the function-field node and carries function_field=True
    # (and sha_assumed=True, since the theorem pivots on finite Brauer/Sha). It
    # deliberately concludes NOTHING over Q, so it cannot leak into the rank >= 2
    # frontier. It is here as the audit exhibit.
    g.add_edge(ProofEdge(
        "e_artin_tate_to_bsd_function_field",
        (),
        "bsd_function_field",
        "Tate/Artin-Tate/Milne: BSD over F_q(C) via geometric Frobenius on a "
        "surface, under finite Brauer group. No number-field analog.",
        dict(_FUNCTION_FIELD),
    ))

    return g


if __name__ == "__main__":
    # Build the atlas and report the frontier for the two OPEN targets. Run:
    #   python -m experiments.engine.atlas_graph
    # The frontier for weak_bsd_rank_ge2 must come back as the open object
    # (rank_two_object), NOT via any parity node. strong_bsd_rank_ge2 must come
    # back needing the rank-two object AND the higher Euler system (the Sha route).
    from .frontier import report, support_sets

    g = build_atlas_graph()

    print("=" * 72)
    print("ATLAS GRAPH")
    print(f"  nodes: {len(g.nodes)}   edges: {len(g.edges)}")
    print("=" * 72)

    # Sanity: the proven regime is established, the open regime is not.
    assert g.is_established("weak_bsd_rank0"), "rank 0 weak BSD must be proven"
    assert g.is_established("weak_bsd_rank1"), "rank 1 weak BSD must be proven"
    assert g.is_established("finite_sha_rank_le1"), "rank <= 1 Sha finiteness proven"
    assert not g.is_established("weak_bsd_rank_ge2"), "rank >= 2 weak BSD is OPEN"
    assert not g.is_established("strong_bsd_rank_ge2"), "rank >= 2 strong BSD is OPEN"
    assert not g.is_established("finite_sha_rank_ge2"), "rank >= 2 Sha finiteness OPEN"
    assert g.is_established("parity_rank_ge2"), "parity in rank >= 2 is proven"

    for target in ("weak_bsd_rank_ge2", "strong_bsd_rank_ge2"):
        print()
        print("-" * 72)
        print(f"support_sets({target!r}):")
        for s in support_sets(g, target):
            print("   ", "{ " + ", ".join(sorted(s)) + " }")
        print()
        print(report(g, target))

    # The load-bearing self-check, printed so the human sees the parity wall is
    # structural: no support set for weak BSD in rank >= 2 contains any parity
    # node, and the open object IS the frontier.
    print()
    print("-" * 72)
    weak_supports = support_sets(g, "weak_bsd_rank_ge2")
    routes_through_parity = any(
        any(member.startswith("parity") for member in s) for s in weak_supports
    )
    print(f"weak_bsd_rank_ge2 support sets: {[sorted(s) for s in weak_supports]}")
    print(f"any support set routes through a parity_* node? {routes_through_parity}")
    assert not routes_through_parity, (
        "PARITY WALL VIOLATED: parity routed into weak_bsd_rank_ge2"
    )
    assert frozenset({"rank_two_object"}) in weak_supports, (
        "rank_two_object must be the frontier of weak BSD rank >= 2"
    )

    strong_supports = support_sets(g, "strong_bsd_rank_ge2")
    print(f"strong_bsd_rank_ge2 support sets: {[sorted(s) for s in strong_supports]}")
    assert frozenset({"rank_two_object", "higher_euler_system"}) in strong_supports, (
        "strong BSD rank >= 2 must need the rank-two object AND a higher Euler system"
    )

    print("OK: the frontier is the open object, not parity. Parity is a dead end.")
