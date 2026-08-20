
"""Safety classifier smoke test for new module tests.

Runs safety_classifier over the new test messages (deterministic, no LLM call)
and confirms expected_branch matches:
  - allow_cbt=False → expected_branch=safety
  - allow_cbt=True  → expected_branch=cbt

Only checks branch routing (not response content). Fast + free.
"""

import json
from pathlib import Path

from pipeline.safety_classifier import classify

TESTS = Path(__file__).resolve().parent.parent / "evals" / "response_test_set.jsonl"

with open(TESTS, encoding="utf-8") as f:
    all_tests = [json.loads(l) for l in f]

# Only run the 22 new tests
NEW_IDS = {
    "resp_insom_001", "resp_insom_002",
    "resp_insom_safety_apnea_001", "resp_insom_safety_narcolepsy_001",
    "resp_insom_safety_benzo_001", "resp_insom_regression_mania_001",
    "resp_work_001", "resp_work_002",
    "resp_work_safety_mobbing_001", "resp_work_safety_harass_001",
    "resp_work_safety_physical_001",
    "resp_rel_001", "resp_rel_002", "resp_rel_003", "resp_rel_004",
    "resp_rel_safety_physical_001", "resp_rel_safety_threat_001",
    "resp_rel_safety_coercive_control_001", "resp_rel_safety_sexual_001",
    "resp_regression_relstress_not_ipv_001", "resp_regression_work_not_mobbing_001",
    "resp_regression_insomnia_short_reply",
}

new_tests = [t for t in all_tests if t["test_id"] in NEW_IDS]

print(f"Running safety_classifier over {len(new_tests)} new tests\n")
print(f"{'test_id':45s} {'expected':10s} {'got':10s} {'ok':4s}  matched")
print("-" * 130)

results = []
for t in new_tests:
    d = classify(t["user_message_tr"])
    got = "safety" if not d.allow_cbt else "cbt"
    expected = t["expected_branch"]
    ok = got == expected
    signals = []
    for m in d.matches:
        signals.extend(m.matched_signals)
    signals_str = ", ".join(signals[:2]) if signals else "-"
    marker = "✓" if ok else "✗"
    print(f"{t['test_id']:45s} {expected:10s} {got:10s} {marker:4s}  {signals_str}")
    results.append((t["test_id"], expected, got, ok, signals))

print()
total = len(results)
passed = sum(1 for r in results if r[3])
print(f"PASS: {passed}/{total}  ({100*passed/total:.0f}%)")

# List failures
fails = [r for r in results if not r[3]]
if fails:
    print(f"\nFAILURES ({len(fails)}):")
    for tid, exp, got, ok, sig in fails:
        print(f"  {tid}: expected {exp} but got {got}  signals={sig}")
