"""C-08 deterministic intent parser (WP §9).

AI-ASSISTED SCAFFOLD. NOT authorship evidence. The conversational layer may interpret and communicate;
it does NOT decide what is true (WP §9.1). This parser is deterministic and closed-vocabulary: it
never guesses — an unrecognised or incomplete query routes to parse_clarification, never to a
fabricated result. An LLM parser can later replace this behind the same typed-intent contract
(constrained decoding), but the discipline demonstrated here does not depend on a model.
"""
from __future__ import annotations
import re

ACTIVITIES = {"swimming": "swimming", "swim": "swimming",
              "climbing": "climbing", "climb": "climbing",
              "yoga": "yoga"}
BOROUGHS = {"croydon": "LB Croydon", "havering": "LB Havering"}
ACCESS_TERMS = ("step-free", "step free", "stepfree", "wheelchair")

# recognised (activity, borough) -> the shared frozen scenario / DecisionEnvelope
SCENARIO_MAP = {
    ("swimming", "LB Croydon"): "supported",
    ("climbing", "LB Havering"): "no_match",
    ("yoga", "LB Croydon"): "indeterminate",
}


def parse(text: str) -> dict:
    t = (text or "").lower()
    activity = None
    for k, v in ACTIVITIES.items():
        if re.search(rf"\b{k}\b", t):
            activity = v
            break
    borough = None
    for k, v in BOROUGHS.items():
        if re.search(rf"\b{k}\b", t):
            borough = v
            break
    access = "step_free" if any(a in t for a in ACCESS_TERMS) else None

    hard = []
    if activity:
        hard.append(f"activity={activity}")
    if access:
        hard.append(f"access={access}")
    ambiguous = []
    if not activity:
        ambiguous.append("activity")
    if not borough:
        ambiguous.append("area")

    scenario = SCENARIO_MAP.get((activity, borough))
    return {
        "activity": activity, "borough": borough, "access": access,
        "hard": hard, "ambiguous": ambiguous, "scenario": scenario,
        "confident": bool(activity and borough and scenario),
        "high_consequence": access is not None,  # accessibility is a high-consequence constraint (WP §9.2)
    }
