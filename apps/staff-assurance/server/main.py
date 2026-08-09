"""FastAPI staff assurance workbench — role-gated SSR.

AI-ASSISTED SCAFFOLD (WP §8, C-06/C-07). NOT authorship evidence. Role gating here is a STUB for the
demonstration: real authentication/IAM/break-glass is Wesley's (Section 16, C-BLOCK-04). Server-side
enforcement is the point — a missing/invalid role returns 403, never partial staff content. Maturity:
research_demonstration (C-BLOCK-12).
"""
from __future__ import annotations
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

try:
    from . import render
except ImportError:
    import render

HERE = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(HERE, "templates"))

app = FastAPI(title="LS OpenActive — staff assurance (restricted, research demonstration)")
app.mount("/static", StaticFiles(directory=os.path.join(HERE, "static")), name="static")

ALLOWED_ROLES = {"analyst", "assurance"}


def _role(request: Request):
    r = request.headers.get("x-staff-role")
    return r if r in ALLOWED_ROLES else None


def _forbidden(request: Request):
    return templates.TemplateResponse(request, "forbidden.html", {}, status_code=403)


def _pick(scenario: str) -> str:
    return scenario if scenario in render.SCENARIOS else "supported"


@app.get("/", response_class=HTMLResponse)
def workbench(request: Request):
    role = _role(request)
    if not role:
        return _forbidden(request)
    return templates.TemplateResponse(request, "workbench.html",
                                      {"role": role, "scenarios": render.SCENARIOS})


@app.get("/replay", response_class=HTMLResponse)
def replay(request: Request, scenario: str = "supported"):
    role = _role(request)
    if not role:
        return _forbidden(request)
    sc = _pick(scenario)
    env = render.load_env(sc)
    return templates.TemplateResponse(request, "replay.html", {
        "role": role, "scenario": sc, "r": render.replay(env),
        "prov": render.provenance(env, "Public-state replay", "inspect only",
                                  "State whether the retained public payload replays to the same digest."),
    })


@app.get("/failure-chain", response_class=HTMLResponse)
def failure_chain(request: Request, scenario: str = "supported"):
    role = _role(request)
    if not role:
        return _forbidden(request)
    sc = _pick(scenario)
    env = render.load_env(sc)
    return templates.TemplateResponse(request, "failure_chain.html", {
        "role": role, "scenario": sc, "steps": render.failure_chain(env),
        "prov": render.provenance(env, "Failure-chain explorer", "diagnose only",
                                  "Describe where a public outcome became limited; no realised-gain wording."),
    })


@app.get("/collection-health", response_class=HTMLResponse)
def collection_health(request: Request, scenario: str = "supported"):
    role = _role(request)
    if not role:
        return _forbidden(request)
    sc = _pick(scenario)
    env = render.load_env(sc)
    return templates.TemplateResponse(request, "collection_health.html", {
        "role": role, "scenario": sc, "h": render.collection_health(env),
        "prov": render.provenance(env, "Collection / vintage health", "inspect only",
                                  "Report denominators and freshness; provision is a lower bound."),
    })


@app.get("/action-card", response_class=HTMLResponse)
def action_card(request: Request, state: str = "drafted"):
    role = _role(request)
    if not role:
        return _forbidden(request)
    return templates.TemplateResponse(request, "action_card.html",
                                      {"role": role, "card": render.action_card(state)})


@app.get("/help", response_class=HTMLResponse)
def help_page(request: Request):
    # Help/guidance carries no evidence, so it is available without a role (consistent help, 3.2.6).
    return templates.TemplateResponse(request, "help.html", {"role": _role(request)})
