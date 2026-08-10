"""C-08 conversation verification (WP §9).

AI-ASSISTED SCAFFOLD. NOT authorship evidence. Proves: chat and guided routes CONVERGE on the same
DecisionEnvelope; an unclear query CLARIFIES rather than fabricating; a high-consequence constraint is
CONFIRMED first; the chat surface leaks nothing and passes the C-11 wording linter; and the route
degrades safely when the model is off (§9.5).

Run:  python test_conversation.py
"""
from __future__ import annotations
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SERVER = os.path.join(HERE, "server")
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
CONTENT = os.path.join(REPO, "packages", "accessible-design-system", "content")
for p in (SERVER, CONTENT, HERE):
    sys.path.insert(0, p)

from fastapi.testclient import TestClient  # noqa: E402
import main, render                        # noqa: E402
import a11y_check, render_lint             # noqa: E402

client = TestClient(main.app)
LEAK = ["internal_score", "recmodel-0.3", "ep-7731", "trace-aa19", "r-a1", "lineage", "0.82"]
CONFIRMED_SWIM = {"q": "swimming in Croydon with step-free access", "confirm": "1"}


def order(html):
    return re.findall(r"Option \d+: (sess-\d+)", html)


def run():
    fails = 0

    # 1. convergence: chat (confirmed) resolves to the SAME decision/order as guided
    chat_html = client.get("/chat", params=CONFIRMED_SWIM).text
    guided_html = client.get("/discover", params={"scenario": "supported"}).text
    conv = order(chat_html) == order(guided_html) == ["sess-101", "sess-102"] \
        and "Matches your confirmed needs" in chat_html
    print(f"[{'OK ' if conv else 'BAD'}] chat<->guided convergence (same certified slate/order)")
    fails += 0 if conv else 1

    # 2. high-consequence confirmation gate (no results before confirm)
    pre = client.get("/chat", params={"q": "swimming in Croydon with step-free access"}).text
    gate = ("confirm" in pre.lower()) and ("sess-101" not in pre)
    print(f"[{'OK ' if gate else 'BAD'}] high-consequence confirmation gate (results withheld until confirmed)")
    fails += 0 if gate else 1

    # 3. unclear query clarifies, never fabricates
    unclear = client.get("/chat", params={"q": "find me something fun"}).text
    clar = ("understand" in unclear.lower()) and ("sess-101" not in unclear)
    print(f"[{'OK ' if clar else 'BAD'}] unclear query -> parse clarification (no fabricated result)")
    fails += 0 if clar else 1

    # 4. safe degradation (model off): guided still works, nothing guessed
    off = client.get("/chat", params={"q": "swimming in Croydon", "model": "off"}).text
    still = client.get("/discover", params={"scenario": "supported"}).text
    degr = ("unavailable" in off.lower()) and ("sess-101" not in off) and ("sess-101" in still)
    print(f"[{'OK ' if degr else 'BAD'}] safe degradation when model off; guided route unaffected")
    fails += 0 if degr else 1

    # 5. no leak on the chat results surface
    leaks = [v for v in LEAK if v in chat_html]
    print(f"[{'OK ' if not leaks else 'BAD'}] chat results leak no staff/research values")
    for l in leaks:
        print("      LEAK:", l)
    fails += len(leaks)

    # 6. C-11 render lint over the chat-resolved decision wording
    pub = render.load_public("supported")
    view = render.build_view(pub)
    violations = render_lint.lint_render(render_lint.load_lexicon(), pub["payload"]["decision"], render.visible_strings(view))
    print(f"[{'OK ' if not violations else 'BAD'}] C-11 render-lint on chat wording")
    for rid, d in violations:
        print(f"      {rid}: {d}")
    fails += len(violations)

    # 7. a11y across the conversational pages
    pages = {
        "/chat": client.get("/chat").text,
        "/chat (clarify)": unclear,
        "/chat (confirm)": pre,
        "/chat (unavailable)": off,
        "/chat (results)": chat_html,
    }
    for label, html in pages.items():
        problems = a11y_check.check_html(html)
        print(f"[{'OK ' if not problems else 'BAD'}] a11y {label}")
        for pr in problems:
            print("      a11y:", pr)
        fails += len(problems)

    print("\nRESULT:", "ALL CONVERSATION CHECKS PASS" if fails == 0 else f"{fails} FAILURE(S)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(run())
