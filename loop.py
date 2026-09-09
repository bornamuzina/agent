import json
import browser
from mediator import ask_model

#prompt options --------------------------------

ACTIONS = """
Reply with ONE json object, nothing else:
{"action": "goto", "url": "https://..."}
{"action": "click", "index": 3}
{"action": "done", "answer": "..."}
{"action": "record", "company": "...", "url": "...", "note": "..."}

Record a company only once, and only if it is hiring for the goal's role.
Do not record job titles or duplicates.
Say done when you have enough.
"""

def build_prompt(goal, page, links, history, results):
    return f"""Goal: {goal}

{ACTIONS}

History so far:
{history}

Collected so far ({len(results)}):
{results}

Current page text:
{page[:1500]}

Links on page:
{links}

Your next action:"""

#---------------------------------------------------------decode answer


def parse_action(reply):
    start = reply.find("{")
    end = reply.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(reply[start:end + 1])
    except json.JSONDecodeError:
        return None

#-------------------------loop------------------------------

def run(goal, start_url, max_steps=10):
    tab = browser.connect()
    browser.goto(tab, start_url)
    history = []
    results = []

    seen = set()

    for step in range(max_steps):
        page = browser.read_text(tab)
        url = browser.current_url(tab)
        links = browser.list_links(tab)
        prompt = build_prompt(goal, page, links, history, results)
        action = parse_action(ask_model(prompt))

        if action is None:
            history.append("invalid reply, retrying")
            continue

        print(step, action)

        key = f"{action} from {url}"
        if key in seen:
            history.append(f"{action} -> already tried from this page, choose differently")
            continue
        seen.add(key)

        if action["action"] == "done":
            return results
        elif action["action"] == "record":
            results.append(action)
        elif action["action"] == "goto":
            browser.goto(tab, action["url"])
        elif action["action"] == "click":
            browser.click_link(tab, action["index"])

        url = browser.current_url(tab)
        history.append(f"{action} -> now at {url}")
        print("  history:", history[-1])

    return results