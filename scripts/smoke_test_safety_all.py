
"""Full safety_classifier smoke test — all 62 test rows.

Confirms branch routing (safety vs cbt) for every test in the response set.
Deterministic, no LLM call — fast + free.
"""

import json
from pathlib import Path
from pipeline.safety_classifier import classify

TESTS = Path(__file__).resolve().parent.parent / "evals" / "response_test_set.jsonl"

with open(TESTS, encoding="utf-8") as f:
    all_tests = [json.loads(l) for l in f]

print(f"Running safety_classifier over {len(all_tests)} tests\n")

results = []
for t in all_tests:
    try:
        d = classify(t["user_message_tr"])
        got = "safety" if not d.allow_cbt else "cbt"
    except Exception as e:
        got = f"ERROR:{type(e).__name__}"
    expected = t.get("expected_branch", "?")
    ok = got == expected
    results.append((t["test_id"], expected, got, ok))

# Group by category prefix
from collections import defaultdict
by_module = defaultdict(list)
for tid, exp, got, ok in results:
    if tid.startswith("resp_ha"):
        mod = "health_anxiety"
    elif tid.startswith("resp_panic"):
        mod = "panic"
    elif tid.startswith("resp_gad"):
        mod = "gad"
    elif tid.startswith("resp_dep"):
        mod = "depression"
    elif tid.startswith("resp_lse"):
        mod = "low_self_esteem"
    elif tid.startswith("resp_insom"):
        mod = "insomnia"
    elif tid.startswith("resp_work"):
        mod = "work_stress"
    elif tid.startswith("resp_rel_"):
        mod = "relationship_stress"
    elif tid.startswith("resp_grief"):
        mod = "grief_loss"
    elif tid.startswith("resp_trans"):
        mod = "life_transitions"
    elif tid.startswith("resp_trauma"):
        mod = "trauma_awareness"
    elif tid.startswith("resp_fin"):
        mod = "financial_stress"
    elif tid.startswith("resp_pain"):
        mod = "chronic_pain"
    elif tid.startswith("resp_body"):
        mod = "body_image"
    elif tid.startswith("resp_exam"):
        mod = "exam_anxiety"
    elif tid.startswith("resp_regression"):
        mod = "regression"
    elif tid.startswith("resp_safety"):
        mod = "safety_general"
    elif tid.startswith("resp_boundary"):
        mod = "boundary"
    elif tid.startswith("resp_nuance"):
        mod = "nuance"
    else:
        mod = "misc"
    by_module[mod].append((tid, exp, got, ok))

# Print per-module pass rate
print("Per-module pass rate:")
for mod, rows in sorted(by_module.items()):
    p = sum(1 for r in rows if r[3])
    n = len(rows)
    print(f"  {mod:25s} {p:2d}/{n:2d}  ({100*p/n:.0f}%)")

total = len(results)
passed = sum(1 for r in results if r[3])
print(f"\n=== OVERALL: {passed}/{total} ({100*passed/total:.0f}%) ===")

# Failures detail
fails = [(tid, exp, got) for tid, exp, got, ok in results if not ok]
if fails:
    print(f"\nFAILURES ({len(fails)}):")
    for tid, exp, got in fails:
        print(f"  {tid}: expected {exp} → got {got}")
