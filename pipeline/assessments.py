"""PHQ-9 + GAD-7 scoring — clinical validated thresholds.

Sources (registry'de zaten var):
  - PHQ-9: Kroenke et al. 2001 (kroenke_2001_phq9_001)
  - GAD-7: Spitzer et al. 2006 (spitzer_2006_gad7_001)

Both are self-report, likert 0-3 per item.
"""
from dataclasses import dataclass
from typing import Literal

Kind = Literal["phq9", "gad7"]


@dataclass
class ScoredAssessment:
    kind: Kind
    total_score: int
    severity: str          # "minimal" | "mild" | "moderate" | "moderately_severe" | "severe"
    suicide_flag: bool     # PHQ-9 item 9 > 0 (self-harm ideation) — clinical urgent


# PHQ-9 thresholds — Kroenke 2001 official
# 0-4:   minimal
# 5-9:   mild
# 10-14: moderate
# 15-19: moderately severe
# 20-27: severe
_PHQ9_THRESHOLDS = [
    (4, "minimal"),
    (9, "mild"),
    (14, "moderate"),
    (19, "moderately_severe"),
    (27, "severe"),
]

# GAD-7 thresholds — Spitzer 2006 official
# 0-4:   minimal
# 5-9:   mild
# 10-14: moderate
# 15-21: severe
_GAD7_THRESHOLDS = [
    (4, "minimal"),
    (9, "mild"),
    (14, "moderate"),
    (21, "severe"),
]


def _severity_from_score(score: int, thresholds) -> str:
    for max_score, label in thresholds:
        if score <= max_score:
            return label
    return thresholds[-1][1]


def score_phq9(answers: list[int]) -> ScoredAssessment:
    """PHQ-9 skorla — 9 madde x 0-3.

    Args:
        answers: 9 elemanlı list, her biri 0-3

    Raises:
        ValueError: length != 9 or any value not in [0,3]
    """

    if len(answers) != 9 or any(a < 0 or a > 3 for a in answers):
        raise ValueError("PHQ-9 requires 9 answers, each 0-3")

    total_score = sum(answers)

    severity = _severity_from_score(total_score, _PHQ9_THRESHOLDS)
    suicide_flag = answers[8]>0
    return ScoredAssessment(kind="phq9",total_score=total_score,severity=severity,suicide_flag=suicide_flag)

   
 

def score_gad7(answers: list[int]) -> ScoredAssessment:
    """GAD-7 skorla — 7 madde x 0-3.

    Args:
        answers: 7 elemanlı list, her biri 0-3
    """

    if len(answers) != 7 or any(a < 0 or a > 3 for a in answers):
        raise ValueError("PHQ-9 requires 9 answers, each 0-3")
    total_score = sum(answers)

    severity = _severity_from_score(total_score, _GAD7_THRESHOLDS)
    return ScoredAssessment(kind="gad7",total_score=total_score,severity=severity,suicide_flag=False)


   


def score(kind: Kind, answers: list[int]) -> ScoredAssessment:
    """Kind'e göre uygun scorer'ı çağır — router."""
    if kind == "phq9":
        return score_phq9(answers)
    elif kind == "gad7":
        return score_gad7(answers)
    else:
        raise ValueError(f"Unknown kind: {kind}")


if __name__ == "__main__":
    # Smoke test — expected verdicts
    test_cases = [
        ("phq9", [0]*9,               0, "minimal", False),
        ("phq9", [1]*9,               9, "mild", True),   # her madde 1 → total 9 mild, suicide 1>0
        ("phq9", [0,0,0,0,0,0,0,0,2], 2, "minimal", True),   # sadece 9. madde 2 → suicide_flag
        ("phq9", [3]*9,              27, "severe", True),
        ("gad7", [0]*7,               0, "minimal", False),
        ("gad7", [2]*7,              14, "moderate", False),
        ("gad7", [3]*7,              21, "severe", False),
    ]
    for kind, ans, exp_total, exp_sev, exp_suicide in test_cases:
        r = score(kind, ans)
        ok = (r.total_score == exp_total and r.severity == exp_sev
              and r.suicide_flag == exp_suicide)
        marker = "✓" if ok else "✗"
        print(f"{marker} {kind} {ans}: total={r.total_score} sev={r.severity} "
              f"suicide={r.suicide_flag} (expected {exp_total}/{exp_sev}/{exp_suicide})")