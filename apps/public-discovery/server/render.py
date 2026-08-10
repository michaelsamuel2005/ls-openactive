"""View-model builder for the public discovery slice.

AI-ASSISTED SCAFFOLD (WP Phase D). NOT authorship evidence; Clarence corrects it in his own words
and obtains non-author review. It reuses the C-BLOCK-05 projector and the C-11 wording lexicon so
the UI can only ever show the PUBLIC projection, worded from the approved lexicon — never a staff
field, never an over-claim.
"""
from __future__ import annotations
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
REPO = os.path.normpath(os.path.join(APP, "..", ".."))
CB05 = os.path.join(REPO, "packages", "application-contracts", "c-block-05")
CONTENT = os.path.join(REPO, "packages", "accessible-design-system", "content")
SCEN = os.path.join(HERE, "scenarios")

sys.path.insert(0, CB05)
import projection_and_invariants as proj  # noqa: E402

_FIELDS, _PLANES = proj.load_classes()
_LEX = json.load(open(os.path.join(CONTENT, "evidence-language.json")))

SCENARIOS = ("supported", "no_match", "indeterminate", "service_failure")

# Evaluation conditions (C-17): P0/P1/P2 change only PRESENTATION over the same decision (C-BLOCK-06).
EVAL_MANIFEST = os.path.join(REPO, "packages", "evaluation", "condition-manifest.json")
try:
    _COND_CAPS = {c["id"]: c["capabilities"] for c in json.load(open(EVAL_MANIFEST)).get("public_conditions", [])}
except Exception:
    _COND_CAPS = {}


def condition_caps(cid):
    return _COND_CAPS.get(cid, {"evidence_communication": True, "conversation": False})


def phrase(cat, val, default=""):
    e = _LEX.get(cat, {}).get(val or "")
    if e and e.get("approved"):
        return e["approved"][0]
    return default or (val or "")


def load_public(scenario):
    """Load the staff-complete scenario envelope and return ONLY its public projection."""
    env = json.load(open(os.path.join(SCEN, scenario + ".json")))
    pub = proj.project(env, _FIELDS, set(_PLANES["public"]))
    return {} if pub is proj.DROP else pub


def build_view(pub):
    v = {
        "action_kind": pub.get("action_kind"),
        "maturity": (pub.get("header") or {}).get("release_maturity_class"),
    }
    if v["action_kind"] == "service_failure":
        p = pub.get("payload", {})
        v["failed_stage"] = p.get("failed_stage")
        v["safe_next"] = p.get("safe_next")
        return v
    d = (pub.get("payload") or {}).get("decision", {})
    v["terminal"] = d.get("terminal_decision")
    v["terminal_text"] = phrase("terminal_decision", d.get("terminal_decision"))
    v["recommendation"] = d.get("recommendation_action")
    v["recommendation_text"] = phrase("recommendation_action", d.get("recommendation_action"))
    v["scope"] = d.get("scope_qualifier")
    v["scope_notice"] = phrase("scope_qualifier", "scope_indeterminate") if d.get("scope_qualifier") == "scope_indeterminate" else ""
    v["coverage"] = (d.get("coverage_qualifier") or {}).get("statement", "")
    v["vintage"] = (d.get("versions") or {}).get("vintage", "")
    cands = []
    for c in d.get("candidates", []):
        attrs = []
        for a in c.get("attributes", []):
            attrs.append({
                "id": a["predicate_id"],
                "state": a["evidence_state"],
                "state_text": phrase("evidence_state", a["evidence_state"]),
                "grade_text": phrase("grade", a.get("grade")) if a.get("grade") else "",
            })
        cands.append({
            "id": c["candidate_id"], "rank": c["rank"], "pool": c["pool"],
            "provider_link": c.get("provider_link", ""), "attributes": attrs,
        })
    v["candidates"] = cands
    return v


def visible_strings(view):
    """Flatten the human-facing strings a page shows, for the C-11 render linter."""
    out = [view.get("terminal_text", ""), view.get("recommendation_text", ""),
           view.get("scope_notice", ""), view.get("coverage", "")]
    for c in view.get("candidates", []):
        for a in c["attributes"]:
            out.append(f"{a['id']}: {a['state_text']} {a['grade_text']}")
    return [s for s in out if s]
