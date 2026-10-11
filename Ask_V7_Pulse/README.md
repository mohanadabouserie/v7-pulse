# Ask V7 Pulse: hosted setup

This folder holds everything the hosted dashboard needs to run "Ask V7 Pulse" on Claude, with web search and Apify.

| File | What it is |
|---|---|
| `system_prompt.md` | The system prompt. The static part is cached; the "Right now" block is filled per request. |
| `tools.json` | The `tools` array for the Claude Messages API: web search, web fetch, eight dashboard-data tools, three Apify tools and an event-suggestion tool. |
| `apify_allowlist.json` | The only actors the assistant may run, what they collect and what they cost. `apify_list_actors` returns this. |

## How a question flows

1. The dashboard sends the question, the chat history and the current filters to your backend (for example `POST /api/ask`). The browser never sees an API key.
2. The backend calls the Claude Messages API with the system prompt, `tools.json` and the conversation, streaming the answer back to the browser.
3. **Web search and web fetch** run on Anthropic's side. Show their citations under the answer.
4. **Dashboard tools** (`get_overview`, `search_posts`, …) run in your backend against the database and return small JSON (aim for under 30 KB each).
5. **Apify tools** run in your backend with the guardrails below.
6. The loop repeats until Claude finishes (`stop_reason` is `end_turn`). If it returns `pause_turn`, send the assistant message back unchanged to continue.

## Model

- `claude-opus-5` (default) for the best analysis and recommendations, about USD 0.17 a question (see `V7_Pulse_Costs.html`).
- `claude-opus-5-5` is the newer Opus at a lower price per token (USD 4 / 20 per million). It's launching now, so test it before switching.
- `claude-sonnet-5` for faster, cheaper answers to everyday questions, about USD 0.07 a question.
- `max_tokens` 4096 is enough for most answers. Stream the response.

## Minimal backend loop (Python)

```python
import json, anthropic
client = anthropic.Anthropic()                      # ANTHROPIC_API_KEY from the environment
TOOLS = json.load(open("tools.json"))
STATIC, _ = open("system_prompt.md").read().split("## Right now")

def ask(messages, right_now_text):
    system = [
        {"type": "text", "text": STATIC, "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": "## Right now" + right_now_text},
    ]
    while True:
        resp = client.messages.create(model="claude-opus-5", max_tokens=4096,
                                      system=system, tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason == "pause_turn":
            continue                                # server tools still working: send it back as is
        if resp.stop_reason != "tool_use":
            return resp                             # done: render text blocks and citations
        results = []
        for block in resp.content:
            if block.type == "tool_use":            # only your own tools appear here
                out = run_tool(block.name, block.input)          # dashboard DB or Apify, see below
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": json.dumps(out, ensure_ascii=False)[:30000]})
        messages.append({"role": "user", "content": results})
```

Put `cache_control` on the tools too if your tool list is long, so repeat questions are cheaper.

## Apify guardrails (enforce these in `run_tool`, not only in the prompt)

- **Allowlist**: refuse any `actor_id` not in `apify_allowlist.json`.
- **Caps on every run**: call `POST https://api.apify.com/v2/acts/{actor}/runs?maxItems={max_items}&maxTotalChargeUsd={max_cost_usd}` with the token in an `Authorization: Bearer` header from the server's environment. Never put the token in the page.
- **Approval**: run at once only when `max_cost_usd` is at or under the auto-approve limit (suggested USD 0.20) and the month's budget allows it. Otherwise store a pending request, return `{"status": "needs_approval", "request_id": …}`, and show it to an admin in the dashboard with Approve and Reject buttons.
- **Budget**: track spend per day and per month (`GET /v2/users/me/limits` shows usage). Refuse runs that would pass the cap.
- **Results**: `apify_get_run` reads `GET /v2/actor-runs/{run_id}` and the dataset, keeps the requested fields and at most 50 items, and marks the data as collected on that date.
- **Log** every run: who asked, the question, the actor, the input, the cost.

Notes from our test runs:
- TikTok needs a cap of at least USD 0.50.
- Reddit needs at least 10 items.
- Carrefour takes one search string per run.
- Amazon must not get `countryCode`, which adds USD 0.06 a product.
- Talabat area pagination is unreliable in the actor. Page the area list on talabat.com, then pass `branchIds`. Free Apify accounts are capped at 100 items a run.

### Option B: Apify's own tool server

Apify runs a hosted MCP server at `https://mcp.apify.com` (Bearer token auth). Claude's MCP connector can attach it directly with `mcp_servers` plus an `mcp_toolset` that allowlists tools (`default_config: {"enabled": false}` and only the tools you want enabled). You can also restrict actors in the URL, for example `https://mcp.apify.com?tools=memo23/talabat-scraper,junglee/Amazon-crawler`. It's quicker to set up, but you lose the per-run cost caps and the approval step above, so we recommend Option A for a client dashboard. Check Anthropic's MCP connector docs for the current beta header.

## Web search

- `web_search_20260209` costs USD 10 per 1,000 searches plus tokens. `max_uses: 5` keeps a single answer from searching too much.
- `web_fetch_20260209` has no extra charge beyond tokens. It can only open URLs that appeared in the conversation or in search results.
- Results are localized to Cairo. If you add `"country": "EG"` to `user_location` and the API rejects it, leave it out.
- Display citations with every web fact. The API requires showing sources to end users.
- Web search can be switched off for the whole organization in the Claude Console. If requests fail with "web search is not enabled", turn it on there.

## Security

- Keys (`ANTHROPIC_API_KEY`, `APIFY_API_TOKEN`) live only in the server environment.
- Posts, comments, menus and web pages are untrusted text. The prompt tells Claude to treat them as data. Keep tools read-only, except Apify runs (capped, approved) and event suggestions (pending until approved).
- Don't send personal data to the web tools. Restaurant and page names are fine; private individuals are not.

## Questions to test it with

1. "Summarize the last 30 days and tell me what to do this week."
2. "Why did mentions spike on 29 Sep?"
3. "How do we compare with Coca-Cola and Pepsi online and in restaurants?"
4. "Which restaurants in Zamalek sell Pepsi but not V7? Draft a pitch for the top 3."
5. "Is there news about Coca-Cola Egypt raising prices?" (should use web search and cite sources)
6. "Collect menus for 200 more restaurants in New Cairo." (should propose a capped Apify run for approval)
7. "اكتبلي ملخص للمنافسين بالمصري" (should answer in Egyptian Arabic)

## The published demo vs the hosted version

The published dashboard already answers with Claude through claude.ai, using the same instructions and the eight dashboard-data tools, run inside the page. A published page has no internet access and must not hold an Apify key. So there, Claude shows proposed web searches and Apify runs as cards instead of running them. The hosted version runs them for real.
