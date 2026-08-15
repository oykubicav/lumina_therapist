"""Eval runner — runs retrieval_test_set.jsonl through the pipeline.

Reports per-test:
  - test_id, category
  - expected_route vs produced_route        (route_ok)
  - expected_allow_cbt vs produced_allow_cbt
  - matched_rules (Layer 1)
  - matched_concepts + per-concept method (hard_rule / concept_rule /
    embedding_fallback) + confidence
  - retrieved_ids + hit_ok
  - forbidden_seen + no_forbidden
  - overall passed

Aggregate metrics:
  - safety_recall            : % of risky tests routed correctly
  - route_accuracy           : % overall
  - retrieval_hit_rate       : % with >=1 expected card
  - forbidden_violations     : raw count
  - overall_pass             : %
  - safety hits by layer     : count of tests where rule / concept /
                                embedding fired
Comparative report:
  - if a previous baseline summary file exists, prints delta per metric.
"""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

from . import config
from .retriever import retrieve, backend_name
from .safety_classifier import classify, classify_verbose



# Test runner
def load_tests():
    tests = []
    with open(config.TEST_SET_PATH, encoding="utf-8") as f:
        for ln in f:
            tests.append(json.loads(ln))
    return tests


def evaluate_one(test, top_k=8):
    user = test["user_message_tr"]
    v = classify_verbose(user, enable_layer3=True)

    retrieved = retrieve(
        user,
        top_k=top_k,
        safety_card_ids=v["safety_card_ids"] or None,
        allow_cbt=v["allow_cbt"],
    )
    retrieved_ids = [r.card_id for r in retrieved]

    produced_route = v["final_route"]
    expected_route = test["expected_route"]
    route_ok = produced_route == expected_route

    allow_cbt_ok = v["allow_cbt"] == test["expected_allow_cbt"]

    expected_cards = set(test.get("expected_cards", []))
    hit = expected_cards & set(retrieved_ids)
    hit_ok = len(hit) > 0 if expected_cards else True

    forbidden = set(test.get("must_not_return_cards", []))
    forbidden_seen = forbidden & set(retrieved_ids)
    no_forbidden = len(forbidden_seen) == 0

    overall = route_ok and allow_cbt_ok and hit_ok and no_forbidden

    # Compute primary match_method for reporting (highest-priority method
    # used to determine the produced route)
    primary_method = "none"
    method_counts = Counter(v["matched_concepts_method"].values())
    if method_counts.get("hard_rule"):
        primary_method = "hard_rule"
    elif method_counts.get("concept_rule"):
        primary_method = "concept_rule"
    elif method_counts.get("embedding_fallback"):
        primary_method = "embedding_fallback"

    return {
        "test_id": test["test_id"],
        "category": test["category"],
        "expected_route": expected_route,
        "produced_route": produced_route,
        "route_ok": route_ok,
        "expected_allow_cbt": test["expected_allow_cbt"],
        "produced_allow_cbt": v["allow_cbt"],
        "allow_cbt_ok": allow_cbt_ok,
        "expected_cards": sorted(expected_cards),
        "expected_hit": sorted(hit),
        "hit_ok": hit_ok,
        "retrieved_ids": retrieved_ids,
        "forbidden_seen": sorted(forbidden_seen),
        "no_forbidden": no_forbidden,
        "passed": overall,
        # rich debug
        "matched_rules": v["matched_rules"],
        "matched_concepts": v["matched_concepts"],
        "matched_concepts_method": v["matched_concepts_method"],
        "matched_concepts_confidence": v["matched_concepts_confidence"],
        "primary_match_method": primary_method,
        "layer3_top": v.get("layer3_top", []),
        "highest_risk": v["highest_risk"],
    }



# Aggregation
def aggregate(results: List[dict]) -> Dict:
    n = len(results)
    by_cat = defaultdict(list)
    for r in results:
        by_cat[r["category"]].append(r)

    def pct(num, den):
        return (100.0 * num / den) if den else 0.0

    safety_critical = [r for r in results if r["expected_route"] != "cbt_support"]
    safety_recall_num = sum(1 for r in safety_critical if r["route_ok"])
    safety_recall = pct(safety_recall_num, len(safety_critical))

    route_acc = pct(sum(1 for r in results if r["route_ok"]), n)
    hit_rate = pct(sum(1 for r in results if r["hit_ok"]), n)
    forbidden = sum(len(r["forbidden_seen"]) for r in results)
    overall = pct(sum(1 for r in results if r["passed"]), n)

    layer_hits = Counter(r["primary_match_method"] for r in results if r["primary_match_method"] != "none")

    return {
        "n": n,
        "safety_recall_pct": safety_recall,
        "safety_recall_num": safety_recall_num,
        "safety_critical_total": len(safety_critical),
        "route_accuracy_pct": route_acc,
        "retrieval_hit_rate_pct": hit_rate,
        "forbidden_violations": forbidden,
        "overall_pass_pct": overall,
        "overall_pass_num": sum(1 for r in results if r["passed"]),
        "layer_hits": dict(layer_hits),
        "per_category": {
            cat: {
                "n": len(rs),
                "pass": sum(1 for r in rs if r["passed"]),
                "pass_pct": pct(sum(1 for r in rs if r["passed"]), len(rs)),
                "route_ok": sum(1 for r in rs if r["route_ok"]),
                "hit_ok": sum(1 for r in rs if r["hit_ok"]),
            }
            for cat, rs in by_cat.items()
        },
    }


def print_summary(agg: Dict, baseline: Optional[Dict] = None):
    n = agg["n"]
    def fmt(v_now, v_base, unit=""):
        if v_base is None:
            return f"{v_now:6.1f}{unit}"
        delta = v_now - v_base
        sign = "+" if delta >= 0 else ""
        return f"{v_now:6.1f}{unit}  (was {v_base:.1f}{unit}, {sign}{delta:.1f})"

    print(f"\n{'='*78}")
    print(f"EVAL — {n} tests   (Layer3 backend: {backend_name()})")
    print(f"{'='*78}")
    base = baseline or {}
    print(f"  safety_recall:        {fmt(agg['safety_recall_pct'], base.get('safety_recall_pct'), '%')}  ({agg['safety_recall_num']}/{agg['safety_critical_total']})")
    print(f"  route_accuracy:       {fmt(agg['route_accuracy_pct'], base.get('route_accuracy_pct'), '%')}")
    print(f"  retrieval_hit_rate:   {fmt(agg['retrieval_hit_rate_pct'], base.get('retrieval_hit_rate_pct'), '%')}")
    print(f"  forbidden_violations: {agg['forbidden_violations']:>3}        " +
          (f"(was {base.get('forbidden_violations', '?')})" if baseline else ""))
    print(f"  overall_pass:         {fmt(agg['overall_pass_pct'], base.get('overall_pass_pct'), '%')}  ({agg['overall_pass_num']}/{n})")

    print(f"\n  Safety routing by layer (where layer fired):")
    for k in ("hard_rule", "concept_rule", "embedding_fallback"):
        c = agg["layer_hits"].get(k, 0)
        print(f"    {k:24s} x{c}")

    print(f"\n  Per-category overall pass:")
    base_cat = base.get("per_category", {})
    for cat in sorted(agg["per_category"]):
        cur = agg["per_category"][cat]
        bsl = base_cat.get(cat, {})
        delta = ""
        if "pass_pct" in bsl:
            d = cur["pass_pct"] - bsl["pass_pct"]
            sign = "+" if d >= 0 else ""
            delta = f"  (was {bsl['pass_pct']:.1f}%, {sign}{d:.1f})"
        print(f"    {cat:24s} {cur['pass']:>2}/{cur['n']:<2}  ({cur['pass_pct']:5.1f}%)" + delta)



# Baseline lookup
def find_latest_baseline(exclude_prefix: Optional[str] = None) -> Optional[Dict]:
    """Find the most recent baseline summary JSON. If exclude_prefix is set,
    skip files starting with that prefix (useful to exclude current run)."""
    out_dir = config.EVAL_RESULTS_DIR
    summaries = sorted(out_dir.glob("baseline_*_summary.json"))
    if exclude_prefix:
        summaries = [s for s in summaries if exclude_prefix not in s.name]
    if not summaries:
        return None
    with open(summaries[-1], encoding="utf-8") as f:
        return json.load(f)



# Main
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--detail", action="store_true")
    parser.add_argument("--no-baseline-compare", action="store_true")
    parser.add_argument("--label", default="baseline", help="Result-file prefix")
    args = parser.parse_args()

    tests = load_tests()
    baseline = None if args.no_baseline_compare else find_latest_baseline()

    start = time.time()
    results = [evaluate_one(t, top_k=args.top_k) for t in tests]
    dur = time.time() - start

    if args.detail:
        for r in results:
            mark = "✓" if r["passed"] else "✗"
            method = r["primary_match_method"][:6]
            print(f"{mark} [{r['category']:20s}] {r['test_id']}: "
                  f"route={r['produced_route']:38s} "
                  f"method={method:6s} hit={r['hit_ok']} fbd={len(r['forbidden_seen'])}")

    agg = aggregate(results)
    print_summary(agg, baseline)
    print(f"\n  Wall time: {dur*1000:.0f} ms")

    out_dir = config.EVAL_RESULTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{args.label}_{datetime.utcnow():%Y%m%d_%H%M%S}.jsonl"
    out = out_dir / fname
    with open(out, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\n  Per-test results: {out.relative_to(config.ROOT)}")
    summary = out_dir / fname.replace(".jsonl", "_summary.json")
    with open(summary, "w", encoding="utf-8") as f:
        json.dump({**agg, "top_k": args.top_k, "duration_ms": dur * 1000, "backend": backend_name()}, f, ensure_ascii=False, indent=2)
    print(f"  Summary:          {summary.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
