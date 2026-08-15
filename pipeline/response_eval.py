"""response_eval.py — End-to-end response evaluation.

Runs response_test_set.jsonl through the full orchestrator (safety +
retrieve + compose + critic + optional rewrite + optional safety
template fallback) and scores each response against per-test constraints.

Per-test constraint schema (see evals/response_test_set.jsonl):
    response_must_contain          : list[str]      each must appear (case-insensitive)
    response_must_contain_any_of   : list[list[str]] each group: at least one appears
    response_must_not_contain      : list[str]      none may appear
    response_max_sentences         : int            soft length cap
    expected_branch                : "cbt" | "safety"
    critic_must_pass               : bool           final critic verdict must PASS

Metrics reported:
    branch_accuracy
    must_contain_hit_rate
    must_not_contain_violations
    length_violations
    critic_pass_rate
    overall_pass       (all constraints satisfied)

Comparative report vs latest previous response_eval summary.
"""

from __future__ import annotations

import argparse
import json
import re
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from . import config
from . import orchestrator


TEST_SET_PATH = config.ROOT / "evals" / "response_test_set.jsonl"


def load_tests():
    tests = []
    with open(TEST_SET_PATH, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                tests.append(json.loads(ln))
    return tests


def _rough_sentence_count(text: str) -> int:
    enders = re.findall(r"[.!?…]+", text)
    return max(1, len(enders))


def _check_response(response_text: str, test: dict) -> dict:
    txt_low = response_text.lower()

    # must_contain (case-insensitive substring; ekli halleri de yakalasın)
    missing = []
    for needle in test.get("response_must_contain", []):
        if needle.lower() not in txt_low:
            missing.append(needle)

    # must_contain_any_of (OR groups)
    missing_any_groups = []
    for group in test.get("response_must_contain_any_of", []):
        if not any(n.lower() in txt_low for n in group):
            missing_any_groups.append(group)

    # must_not_contain — WORD BOUNDARY match, not raw substring.
    # Türkçede "yalnız kal" ≠ "yalnız kalma"; substring FP olmasın diye
    # \b sınırlarıyla eşleşiyoruz. Python 3 re modülü \b'yi Unicode-aware
    # değerlendiriyor, Türkçe harfler word char sayılıyor.
    forbidden_seen = []
    for needle in test.get("response_must_not_contain", []):
        pattern = r"\b" + re.escape(needle.lower()) + r"\b"
        if re.search(pattern, txt_low, re.UNICODE):
            forbidden_seen.append(needle)

    # Length
    max_s = test.get("response_max_sentences")
    n_sent = _rough_sentence_count(response_text)
    length_violation = (max_s is not None and n_sent > max_s)

    return {
        "must_contain_missing": missing,
        "must_contain_any_missing_groups": missing_any_groups,
        "forbidden_seen": forbidden_seen,
        "sentences": n_sent,
        "max_sentences": max_s,
        "length_violation": length_violation,
    }


def evaluate_one(test: dict, *, top_k: int, enable_llm_critic: bool, max_rewrites: int) -> dict:
    """Send the test through the orchestrator and score."""
    t0 = time.time()
    try:
        turn = orchestrator.respond(
            test["user_message_tr"],
            top_k=top_k,
            enable_llm_critic=enable_llm_critic,
            max_rewrites=max_rewrites,
        )
    except Exception as e:
        return {
            "test_id": test["test_id"],
            "category": test["category"],
            "error": f"{type(e).__name__}: {e}",
            "passed": False,
        }
    wall_ms = (time.time() - t0) * 1000

    checks = _check_response(turn.response_text, test)

    # Branch check
    expected_branch = test.get("expected_branch")
    branch_ok = (expected_branch is None) or (turn.branch == expected_branch)

    # Critic check
    critic_pass = turn.critic.get("passed", False)
    critic_ok = (not test.get("critic_must_pass", True)) or critic_pass

    all_content_ok = (
        len(checks["must_contain_missing"]) == 0
        and len(checks["must_contain_any_missing_groups"]) == 0
        and len(checks["forbidden_seen"]) == 0
    )
    passed = branch_ok and critic_ok and all_content_ok and not checks["length_violation"]

    return {
        "test_id": test["test_id"],
        "category": test["category"],
        "expected_branch": expected_branch,
        "produced_branch": turn.branch,
        "branch_ok": branch_ok,
        "critic_pass": critic_pass,
        "critic_ok": critic_ok,
        "critic_findings": turn.critic.get("findings", []),
        "content_checks": checks,
        "sentences": checks["sentences"],
        "length_ok": not checks["length_violation"],
        "used_fallback": turn.used_fallback,
        "rewrite_count": turn.rewrite_count,
        "passed": passed,
        "response_text": turn.response_text,
        "safety_route": turn.safety.final_route,
        "safety_allow_cbt": turn.safety.allow_cbt,
        "safety_card_ids": turn.safety.safety_card_ids,
        "wall_ms": wall_ms,
    }


def aggregate(results: List[dict]) -> Dict:
    n = len(results)
    valid = [r for r in results if "error" not in r]

    def pct(num, den):
        return (100.0 * num / den) if den else 0.0

    branch_acc = pct(sum(1 for r in valid if r["branch_ok"]), len(valid))
    critic_pass = pct(sum(1 for r in valid if r["critic_pass"]), len(valid))
    critic_ok = pct(sum(1 for r in valid if r["critic_ok"]), len(valid))
    length_ok = pct(sum(1 for r in valid if r["length_ok"]), len(valid))
    forbidden_viol = sum(len(r["content_checks"]["forbidden_seen"]) for r in valid)
    missing_viol = sum(
        len(r["content_checks"]["must_contain_missing"]) + len(r["content_checks"]["must_contain_any_missing_groups"])
        for r in valid
    )
    overall = pct(sum(1 for r in valid if r["passed"]), len(valid))

    by_cat = defaultdict(list)
    for r in valid:
        by_cat[r["category"]].append(r)

    per_cat = {}
    for cat, rs in by_cat.items():
        per_cat[cat] = {
            "n": len(rs),
            "pass": sum(1 for r in rs if r["passed"]),
            "pass_pct": pct(sum(1 for r in rs if r["passed"]), len(rs)),
        }

    return {
        "n": n,
        "n_valid": len(valid),
        "branch_accuracy_pct": branch_acc,
        "critic_pass_rate_pct": critic_pass,
        "critic_ok_pct": critic_ok,
        "length_ok_pct": length_ok,
        "forbidden_violations": forbidden_viol,
        "missing_content_violations": missing_viol,
        "overall_pass_pct": overall,
        "fallback_count": sum(1 for r in valid if r.get("used_fallback")),
        "rewrite_count": sum(r.get("rewrite_count", 0) for r in valid),
        "errors": [r for r in results if "error" in r],
        "per_category": per_cat,
    }


def print_summary(agg: Dict, baseline: Optional[Dict] = None, *, wall_ms: float = 0.0):
    n = agg["n"]

    def fmt(v_now, v_base, unit=""):
        if v_base is None:
            return f"{v_now:6.1f}{unit}"
        delta = v_now - v_base
        sign = "+" if delta >= 0 else ""
        return f"{v_now:6.1f}{unit}  (was {v_base:.1f}{unit}, {sign}{delta:.1f})"

    print()
    print("=" * 78)
    print(f"RESPONSE EVAL — {n} tests   (composer={config.LLM_MODEL_COMPOSER}, critic={config.LLM_MODEL_CRITIC})")
    print("=" * 78)
    b = baseline or {}
    print(f"  branch_accuracy      : {fmt(agg['branch_accuracy_pct'], b.get('branch_accuracy_pct'), '%')}")
    print(f"  critic_pass_rate     : {fmt(agg['critic_pass_rate_pct'], b.get('critic_pass_rate_pct'), '%')}")
    print(f"  length_ok            : {fmt(agg['length_ok_pct'], b.get('length_ok_pct'), '%')}")
    print(f"  forbidden_violations : {agg['forbidden_violations']:>3}       " + (f"(was {b.get('forbidden_violations','?')})" if baseline else ""))
    print(f"  missing_content_viol : {agg['missing_content_violations']:>3}       " + (f"(was {b.get('missing_content_violations','?')})" if baseline else ""))
    print(f"  overall_pass         : {fmt(agg['overall_pass_pct'], b.get('overall_pass_pct'), '%')}")
    print(f"  rewrites             : {agg['rewrite_count']}   fallbacks: {agg['fallback_count']}")
    if agg.get("errors"):
        print(f"  errors               : {len(agg['errors'])} tests errored")

    print()
    print("  Per-category pass:")
    base_cat = b.get("per_category", {})
    for cat in sorted(agg["per_category"]):
        cur = agg["per_category"][cat]
        bsl = base_cat.get(cat, {})
        delta = ""
        if "pass_pct" in bsl:
            d = cur["pass_pct"] - bsl["pass_pct"]
            sign = "+" if d >= 0 else ""
            delta = f"  (was {bsl['pass_pct']:.1f}%, {sign}{d:.1f})"
        print(f"    {cat:32s} {cur['pass']:>2}/{cur['n']:<2}  ({cur['pass_pct']:5.1f}%)" + delta)

    if wall_ms:
        print(f"\n  Wall time: {wall_ms/1000:.1f} s  ({wall_ms/max(1,n):.0f} ms/test avg)")


def find_latest_baseline() -> Optional[Dict]:
    results_dir = config.EVAL_RESULTS_DIR
    summaries = sorted(results_dir.glob("response_*_summary.json"))
    if not summaries:
        return None
    with open(summaries[-1], encoding="utf-8") as f:
        return json.load(f)


def main():
    # Auto-register composer mock handlers if provider is mock
    import os as _os
    if _os.environ.get("CBT_LLM_PROVIDER") == "mock":
        from . import composer as _composer
        _composer.register_composer_mocks()

    parser = argparse.ArgumentParser()
    parser.add_argument("--top-k", type=int, default=6)
    parser.add_argument("--label", default="response")
    parser.add_argument("--detail", action="store_true")
    parser.add_argument("--dump-responses", action="store_true",
                        help="Print each response text (long output).")
    parser.add_argument("--no-llm-critic", action="store_true",
                        help="Skip Haiku critic pass — rule-only.")
    parser.add_argument("--no-rewrite", action="store_true",
                        help="Disable rewrite loop.")
    parser.add_argument("--limit", type=int, default=0,
                        help="Only run first N tests (dev iteration).")
    parser.add_argument("--filter", default="",
                        help="Substring filter on test_id.")
    args = parser.parse_args()

    tests = load_tests()
    if args.filter:
        tests = [t for t in tests if args.filter in t["test_id"]]
    if args.limit:
        tests = tests[: args.limit]

    baseline = find_latest_baseline()
    max_rewrites = 0 if args.no_rewrite else 1
    enable_llm_critic = not args.no_llm_critic

    start = time.time()
    results = []
    for i, test in enumerate(tests, 1):
        print(f"[{i:>3}/{len(tests)}] {test['test_id']} ...", end="", flush=True)
        r = evaluate_one(test, top_k=args.top_k, enable_llm_critic=enable_llm_critic, max_rewrites=max_rewrites)
        mark = "PASS" if r.get("passed") else "FAIL"
        if "error" in r:
            mark = f"ERR({r['error'][:40]})"
        print(f" {mark}")
        if args.detail:
            _print_test_detail(r)
        if args.dump_responses:
            print("  RESPONSE:")
            for ln in (r.get("response_text") or "").splitlines():
                print(f"    {ln}")
            print()
        results.append(r)
    wall_ms = (time.time() - start) * 1000

    agg = aggregate(results)
    print_summary(agg, baseline, wall_ms=wall_ms)

    out_dir = config.EVAL_RESULTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{args.label}_{datetime.utcnow():%Y%m%d_%H%M%S}.jsonl"
    with open(out_dir / fname, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    summary_path = out_dir / fname.replace(".jsonl", "_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({**agg, "top_k": args.top_k, "duration_ms": wall_ms,
                   "enable_llm_critic": enable_llm_critic, "max_rewrites": max_rewrites}, f, ensure_ascii=False, indent=2)
    print(f"\n  Per-test results: {(out_dir / fname).relative_to(config.ROOT)}")
    print(f"  Summary:          {summary_path.relative_to(config.ROOT)}")


def _print_test_detail(r):
    if "error" in r:
        print(f"    error: {r['error']}")
        return
    cc = r.get("content_checks", {})
    if cc.get("forbidden_seen"):
        print(f"    forbidden_seen: {cc['forbidden_seen']}")
    if cc.get("must_contain_missing"):
        print(f"    missing: {cc['must_contain_missing']}")
    if cc.get("must_contain_any_missing_groups"):
        print(f"    missing_any_of: {cc['must_contain_any_missing_groups']}")
    if cc.get("length_violation"):
        max_s = cc.get("max_sentences", "?")
        print(f"    length: {r.get('sentences', '?')} sentences (max {max_s})")
    if not r.get("branch_ok", True):
        print(f"    branch: expected {r.get('expected_branch')}, got {r.get('produced_branch')}")
    if not r.get("critic_pass", True):
        for f in r.get("critic_findings", [])[:4]:
            print(f"    critic: [{f.get('layer')}/{f.get('severity')}] {f.get('check_id')}: {f.get('message')}")
    if r.get("rewrite_count", 0):
        print(f"    rewrites: {r['rewrite_count']}  used_fallback: {r.get('used_fallback', False)}")


if __name__ == "__main__":
    main()
