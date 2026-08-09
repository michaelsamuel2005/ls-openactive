"""FastAPI public discovery slice — server-side rendered, no-JS core.

AI-ASSISTED SCAFFOLD (WP Phase D, ADR-0001). NOT authorship evidence. Every core route returns
complete HTML with no JavaScript required; React/TS only enhances. Maturity: research_demonstration
(C-BLOCK-12) — not a public deployment.
"""
from __future__ import annotations
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

try:  # imported as `server.main` (uvicorn server.main:app --app-dir apps/public-discovery)
    from . import render
except ImportError:  # imported as top-level `main` (server dir on sys.path: tests / --app-dir .../server)
    import render

HERE = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(HERE, "templates"))

app = FastAPI(title="LS OpenActive — public discovery (research demonstration)")
app.mount("/static", StaticFiles(directory=os.path.join(HERE, "static")), name="static")

TEMPLATE_FOR_TERMINAL = {
    "supported_match": "results.html",
    "bounded_non_match": "no_match.html",
    "evidence_indeterminate": "cannot_answer.html",
}


def _pick(scenario: str) -> str:
    return scenario if scenario in render.SCENARIOS else "supported"


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


@app.get("/discover", response_class=HTMLResponse)
def discover(request: Request, scenario: str = "supported", activity: str = "", access: str = ""):
    sc = _pick(scenario)
    view = render.build_view(render.load_public(sc))
    if view["action_kind"] == "service_failure":
        tmpl = "service_failure.html"
    else:
        tmpl = TEMPLATE_FOR_TERMINAL.get(view.get("terminal"), "results.html")
    return templates.TemplateResponse(request, tmpl, {"v": view, "scenario": sc,
                                                      "query": {"activity": activity, "access": access}})


@app.get("/result/{cid}", response_class=HTMLResponse)
def result(request: Request, cid: str, scenario: str = "supported"):
    view = render.build_view(render.load_public(_pick(scenario)))
    cand = next((c for c in view.get("candidates", []) if c["id"] == cid), None)
    if not cand:
        return HTMLResponse(
            "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<title>Not found</title></head><body><main id=\"main\"><h1>Result not found</h1>"
            "<p><a href=\"/\">Back to search</a></p></main></body></html>", status_code=404)
    return templates.TemplateResponse(request, "detail.html", {"v": view, "c": cand})


@app.get("/help", response_class=HTMLResponse)
def help_page(request: Request):
    return templates.TemplateResponse(request, "help.html", {})


@app.get("/api/envelope")
def api_envelope(scenario: str = "supported"):
    """The public ApplicationEnvelope projection — the contract boundary for the enhancement layer."""
    return JSONResponse(render.load_public(_pick(scenario)))
