"""Experiment (l): the BSD proof-search engine driver.

This is the runnable face of the engine spine (graph / frontier / audit) plus
the PROPOSE+FALSIFY+AUDIT miner. It does three things, offline and fast:

  1. FRONTIER. Build the BSD atlas as a typed AND/OR proof graph and print the
     minimal open support sets (with leverage) for weak BSD and strong BSD in
     rank >= 2. Because parity is its own node with no edge into the full-rank
     claims, the frontier the engine reports is the genuine open object (two
     independent points; an unconditional Euler system), never "assume parity".

  2. AUDIT. Run four illustrative methods past the three wrong-approach
     detectors and print each verdict: a modularity-only full-rank claim (parity
     wall), the Heegner machine on the rank-2 control curve (clean detectors but
     structurally capped at rank <= 1), strong BSD reading #Sha off the formula
     on a rank-2 curve (Sha-finiteness wall in the open regime), and a
     function-field transcription (mirage wall).

  3. MINE. Run the relation library and print the scorecard, separating
     casualties at the cliff from survivors-with-caveat from clean survivors.

  4. LOCALIZE. For a candidate expressed as a residual, build the curve x rank
     and curve x prime heat-maps and diagnose WHERE it breaks: the cliff (holds
     through rank <= 1, breaks at rank >= 2), a proven-regime break, or a
     survivor. The cliff diagnosis is the same wall the miner flags, now measured.

  5. PROPOSE. Run the library of candidate rank >= 2 construction classes through
     the Direction-01 test battery (T1 nondegeneracy on 389a1, T2 second-order
     tie) plus the detectors. The honest result: every actual construction is
     first-derivative-bottlenecked, retired (GKZ), the open Clause-2 candidate, or
     the Selmer lane; the only T1-passer is non-constructive search.

  6. VERIFY. Emit a Lean obligation per open frontier node, in the skeleton style,
     referencing only identifiers that exist. Every body is a sorry; the frontier
     object's obligation corresponds to the skeleton's rankTwoCertificate. VERIFY
     states what would have to be closed; it closes nothing.

WHY this is experiment (l) and not a proof: it proves nothing about BSD in
rank >= 2. It makes the SHAPE of the problem mechanical: the frontier is data,
the detectors gate every proposed step, and a relation that only reproduces the
proven regime is reported as a casualty rather than a discovery. The honest
takeaway printed at the end is that the open object remains a construction to be
built, exactly the BUILDER mandate.

Run from the repo root:
    python -m experiments.engine.e_l_engine
"""

from __future__ import annotations

import sys

from experiments._shared import get_curve

from .atlas_graph import build_atlas_graph
from .frontier import report
from .audit import Method, audit_method
from .mine import mine, scorecard, live_falsification_demo
from .localize import (
    localize,
    localize_primes,
    render,
    render_primes,
    DEMO_CLIFF,
    DEMO_SURVIVOR,
    DEMO_PRIME_LOCATOR,
)
from .propose import propose, scorecard as propose_scorecard
from .verify import emit_obligations, report as verify_report, theorem_text


def _section(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def _print_audit(name: str, verdict) -> None:
    status = "CLEAN" if verdict.clean else "FLAGGED"
    walls = []
    if verdict.parity_only:
        walls.append("parity-only")
    if "SHA ASSUMED" in verdict.sha_message:
        walls.append("Sha-finiteness (open regime)")
    if verdict.function_field_flagged:
        walls.append("function-field mirage")
    wall_str = ", ".join(walls) if walls else "none"
    print(f"  [{status}] {name}")
    print(f"      walls hit: {wall_str}")
    for msg in verdict.messages:
        print(f"      - {msg}")


def main() -> int:
    # The VERIFY section prints real Lean (with characters like the leq sign and
    # the reals symbol). Make stdout utf-8 so the driver runs on a cp1252 console.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    open_curve = get_curve("389a1")  # the rank-2 open-regime control

    # -- 1. FRONTIER -------------------------------------------------------
    _section("SECTION 1  FRONTIER: the minimal open object behind rank >= 2 BSD")
    graph = build_atlas_graph()
    print(report(graph, "weak_bsd_rank_ge2"))
    print()
    print(report(graph, "strong_bsd_rank_ge2"))
    print()
    print("Note: no support set above reduces to a parity node. Parity is proven")
    print("(parity_rank_ge2) but has no edge into the full-rank claim, so the")
    print("frontier is the construction, not the sign of the functional equation.")

    # -- 2. AUDIT ----------------------------------------------------------
    _section("SECTION 2  AUDIT: four illustrative methods past the three detectors")

    m_modularity = Method(
        name="modularity-only full-rank claim",
        claims_full_rank=True,
        uses_only_root_number=True,
        target_regime="rank_ge2",
    )
    _print_audit(m_modularity.name,
                 audit_method(m_modularity, analytic_rank=2, E=open_curve))

    m_heegner = Method(
        name="Heegner machine on 389a1 (rank 2)",
        # Detectors are clean: it assumes nothing open and uses no root-number
        # shortcut. But it is STRUCTURALLY capped: the Heegner construction
        # yields one point, so it cannot certify rank 2. The cap is not one of
        # the three detectors; it is the control-pair / cliff fact, printed here.
        target_regime="rank_ge2",
    )
    print()
    _print_audit(m_heegner.name,
                 audit_method(m_heegner, analytic_rank=2, E=open_curve))
    print("      CAVEAT (not a detector): the Heegner point is one point. On a")
    print("      rank-2 curve it lands in a rank-1 subgroup and cannot witness the")
    print("      second generator. Clean detectors do not mean rank-2 capable.")

    m_strong = Method(
        name="strong BSD reading off #Sha on 389a1",
        assumes_sha_finite=True,
        target_regime="rank_ge2",
    )
    print()
    _print_audit(m_strong.name,
                 audit_method(m_strong, analytic_rank=2, E=open_curve))

    m_ff = Method(
        name="function-field transcription",
        uses_geometric_frobenius=True,
        needs_base_curve=True,
        target_regime="rank_ge2",
    )
    print()
    _print_audit(m_ff.name,
                 audit_method(m_ff, analytic_rank=2, E=open_curve))

    # -- 3. MINE -----------------------------------------------------------
    _section("SECTION 3  MINE: relations over bundled invariants, classified honestly")
    rows = mine()
    print(scorecard(rows))
    print()
    print(live_falsification_demo())

    # -- 4. LOCALIZE -------------------------------------------------------
    _section("SECTION 4  LOCALIZE: where does a candidate break? (curve x rank, curve x prime)")
    print(render(localize(DEMO_CLIFF)))
    print()
    print(render(localize(DEMO_SURVIVOR)))
    print()
    print(render_primes(localize_primes(
        DEMO_PRIME_LOCATOR,
        curves=[get_curve(l) for l in ("11a1", "14a1", "15a1", "26a1")],
    )))
    print()
    print("Reading: the cliff candidate holds through rank <= 1 and first breaks")
    print("at rank 2 (the Detector-1 signature, with the residual growing into the")
    print("open regime); the survivor never breaks (a necessary condition only);")
    print("the prime grid isolates each curve's bad primes. LOCALIZE turns a failed")
    print("FALSIFY into a diagnosis for the next PROPOSE; it proves nothing alone.")

    # -- 5. PROPOSE --------------------------------------------------------
    _section("SECTION 5  PROPOSE: candidate rank >= 2 constructions vs the Direction-01 bar")
    print(propose_scorecard(propose()))

    # -- 6. VERIFY ---------------------------------------------------------
    _section("SECTION 6  VERIFY: emit Lean obligations from the frontier (statements, not proofs)")
    obligations = emit_obligations(graph)
    print(verify_report(obligations))
    print()
    print("Emitted Lean (the frontier object, excerpt):")
    rt = next(o for o in obligations if o.node_key == "rank_two_object")
    print(theorem_text(graph, rt))
    print()
    print("Full file written by `python -m experiments.engine.verify` to")
    print("lean/BSD/EngineObligations.lean. Discharge = lake build with a real")
    print("construction; every obligation is a sorry, nothing is proven here.")

    # -- closing honesty line ---------------------------------------------
    _section("ENGINE VERDICT")
    print("The frontier of weak/strong BSD in rank >= 2 is the construction of two")
    print("independent points plus an unconditional Euler system, NOT parity. Every")
    print("method that claims the open regime from parity, an assumed finite Sha, or")
    print("a geometric Frobenius is flagged. The miner's only clean survivor (#Sha a")
    print("square) is a necessary condition, not a rank >= 2 proof. The object is")
    print("still to be built.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
