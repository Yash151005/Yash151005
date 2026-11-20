#!/usr/bin/env python3
"""
YASH.PAKALE // NEURAL.OS: self-hosted telemetry renderer.

Renders three data-driven SVGs into assets/ from GitHub data:
  telemetry.svg   stats tiles, top languages, 30-day contribution pulse
  snake.svg       a snake that eats the real contribution graph
  trophies.svg    trophy shelf computed from the same numbers

Why: third-party widgets (streak-stats, readme-stats, trophy, Platane snake
output branch) fail intermittently, e.g. "Something went wrong! Could not
fetch total commits". Here every image is a file in this repo, served by
GitHub itself, so the README cannot show a broken widget.

Fail-safe: on a fatal error nothing in assets/ is touched (exit 1), so the
profile keeps the last good render. Writes are atomic and XML-validated.

Data sources (stdlib only):
  * GraphQL contribution calendar when GH_TOKEN/GITHUB_TOKEN is set
  * otherwise (or if GraphQL fails) the public page
    https://github.com/users/<user>/contributions, so this also runs locally
    with no token:   python tools/render_telemetry.py
  * REST for repos / followers, search API for PR / issue counts
"""
import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (BG, BLUE, BLUE2, DEFS, DIM, DIM2, GOLD, LEVELS, LINE,  # noqa: E402
                   PANEL2, SANS, TEAL, TXT, esc, head, panel, write_atomic)

USER = os.environ.get("PROFILE_USER", "Yash151005")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
UA = "yash151005-telemetry-renderer"


# ================================================================== fetching
def _req(url, payload=None, accept="application/vnd.github+json", auth=True):
    headers = {"User-Agent": UA, "Accept": accept}
    if TOKEN and auth:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=data, headers=headers,
                                         method="POST" if data else "GET")
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8")
        except Exception as e:  # noqa: BLE001
            last = e
            print(f"  retry {attempt + 1}/3 {url[:70]}: {e}", file=sys.stderr)
            time.sleep(2 + attempt * 3)
    raise last


def calendar_graphql():
    q = """query($u:String!){ user(login:$u){ contributionsCollection{
      totalCommitContributions
      contributionCalendar{ totalContributions
        weeks{ contributionDays{ date contributionCount } } } } } }"""
    res = json.loads(_req("https://api.github.com/graphql", {"query": q, "variables": {"u": USER}}))
    cc = res["data"]["user"]["contributionsCollection"]
    days = [(d["date"], d["contributionCount"])
            for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    return days, cc["totalCommitContributions"]


def calendar_public():
    page = _req(f"https://github.com/users/{USER}/contributions", accept="text/html", auth=False)
    cells = dict(re.findall(r'data-date="(\d{4}-\d\d-\d\d)"\s+id="(contribution-day-component-[\d-]+)"', page))
    if not cells:
        raise RuntimeError("public contribution page: no calendar cells found")
    tips = {}
    for cid, text in re.findall(r'<tool-tip[^>]*\bfor="([^"]+)"[^>]*>([^<]*)</tool-tip>', page):
        text = html.unescape(text)
        m = re.match(r"\s*([\d,]+) contributions?", text)
        tips[cid] = int(m.group(1).replace(",", "")) if m else 0
    days = sorted((date, tips.get(cid, 0)) for date, cid in cells.items())
    return days, None


def fetch():
    days, commits = None, None
    if TOKEN:
        try:
            days, commits = calendar_graphql()
            print("calendar: graphql")
        except Exception as e:  # noqa: BLE001
            print(f"graphql failed, using public page: {e}", file=sys.stderr)
    if days is None:
        days, commits = calendar_public()
        print("calendar: public contributions page")

    user = json.loads(_req(f"https://api.github.com/users/{USER}"))
    repos, page = [], 1
    while page <= 5:
        batch = json.loads(_req(
            f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&page={page}"))
        repos += batch
        if len(batch) < 100:
            break
        page += 1
    own = [r for r in repos if not r.get("fork")]

    def search_count(q):
        try:
            return json.loads(_req(f"https://api.github.com/search/issues?q={q}&per_page=1"))["total_count"]
        except Exception as e:  # noqa: BLE001 — non-critical
            print(f"search '{q}' failed (non-fatal): {e}", file=sys.stderr)
            return 0

    langs = {}
    for r in own:
        if r.get("language"):
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    created = dt.date.fromisoformat(user["created_at"][:10])
    return {
        "days": days,
        "total": sum(c for _, c in days),
        "commits": commits,
        "repos": user.get("public_repos", len(repos)),
        "followers": user.get("followers", 0),
        "stars": sum(r.get("stargazers_count", 0) for r in own),
        "langs": sorted(langs.items(), key=lambda kv: (-kv[1], kv[0]))[:6],
        "prs": search_count(f"author:{USER}+type:pr"),
        "issues": search_count(f"author:{USER}+type:issue"),
        "years": (dt.date.today() - created).days / 365.25,
    }


def streaks(days):
    longest = run = 0
    for _, c in days:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur, i = 0, len(days) - 1
    today = dt.date.today().isoformat()
    while i >= 0:
        date, c = days[i]
        if c:
            cur += 1
        elif not (date >= today and cur == 0):  # today with 0 doesn't break it yet
            break
        i -= 1
    return cur, longest


def stamp():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


# ================================================================ telemetry
def render_telemetry(d):
    w, h = 940, 480
    cur, lng = streaks(d["days"])
    tiles = [
        ("CONTRIBUTIONS · 1Y", f"{d['total']:,}"),
        ("CURRENT STREAK", f"{cur} d"),
        ("LONGEST STREAK", f"{lng} d"),
        ("PUBLIC REPOS", f"{d['repos']}"),
        ("STARS EARNED", f"{d['stars']}"),
        ("FOLLOWERS", f"{d['followers']}"),
    ]
    cells = []
    for i, (label, val) in enumerate(tiles):
        x, y = 30 + (i % 2) * 212, 74 + (i // 2) * 88
        cells.append(f"""
<rect x="{x}" y="{y}" width="200" height="76" rx="10" fill="{PANEL2}" stroke="{LINE}"/>
<rect x="{x + 12}" y="{y}" width="48" height="2.5" rx="1.2" fill="url(#edgeG)"/>
<text x="{x + 14}" y="{y + 25}" font-size="10" letter-spacing="1.6" fill="{DIM}">{label}</text>
<text x="{x + 14}" y="{y + 60}" font-family="{SANS}" font-size="28" font-weight="700" fill="{TXT}"
      class="num" style="animation-delay:-{i * 0.5:.1f}s">{esc(val)}</text>""")

    langs = d["langs"] or [("n/a", 1)]
    top = max(v for _, v in langs)
    tot = sum(v for _, v in langs)
    lx, ly, bw_max = 500, 100, 400
    bars = [f'<text x="{lx}" y="84" font-size="10.5" letter-spacing="2" fill="{DIM}">TOP LANGUAGES · BY REPOSITORY</text>']
    for i, (name, n) in enumerate(langs):
        y = ly + i * 38
        bw = max(6, bw_max * n / top)
        bars.append(f"""
<text x="{lx}" y="{y + 12}" font-size="12" fill="{TXT}">{esc(name)}</text>
<text x="{lx + bw_max}" y="{y + 12}" text-anchor="end" font-size="11.5" fill="{DIM}">{n} repo{"s" if n != 1 else ""} · {100 * n / tot:.0f}%</text>
<rect x="{lx}" y="{y + 19}" width="{bw_max}" height="6" rx="3" fill="{LINE}" opacity="0.6"/>
<g style="transform-box:fill-box;transform-origin:left center"><rect class="bar" style="animation-delay:{i * 0.12:.2f}s"
   x="{lx}" y="{y + 19}" width="{bw:.1f}" height="6" rx="3" fill="{TEAL}"/></g>""")

    # 30-day pulse: single series area chart, no legend needed
    last = d["days"][-30:]
    cx0, cx1, cy0, cy1 = 40, w - 40, 374, 440
    vmax = max([c for _, c in last] + [1])
    pts = [(cx0 + i * (cx1 - cx0) / (len(last) - 1), cy1 - (cy1 - cy0) * c / vmax)
           for i, (_, c) in enumerate(last)]
    line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    area = line + f" L{pts[-1][0]:.1f} {cy1} L{pts[0][0]:.1f} {cy1} Z"
    pk = max(range(len(last)), key=lambda i: last[i][1])
    px, py = pts[pk]
    peak = ""
    if last[pk][1]:
        anchor = "end" if px > w - 120 else "start"
        dx = -8 if anchor == "end" else 8
        peak = (f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{TEAL}" stroke="{BG}" stroke-width="2"/>'
                f'<text x="{px + dx:.1f}" y="{py - 6:.1f}" text-anchor="{anchor}" font-size="10.5" fill="{TXT}">'
                f'peak {last[pk][1]} on {last[pk][0][5:]}</text>')
    f30 = sum(c for _, c in last)

    svg = f"""{head(w, h)}
{DEFS}
<defs>
  <linearGradient id="areaG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{TEAL}" stop-opacity="0.35"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="reveal"><rect x="0" y="0" height="{h}" width="0">
    <animate attributeName="width" values="0;{w};{w}" keyTimes="0;0.35;1" dur="9s" repeatCount="indefinite"/>
  </rect></clipPath>
</defs>
<style>
  .num{{animation:np 3s ease-in-out infinite}}
  @keyframes np{{0%,100%{{opacity:.85}}50%{{opacity:1}}}}
  .bar{{animation:fill 1.4s cubic-bezier(.2,.7,.2,1) both}}
  @keyframes fill{{from{{transform:scaleX(.02)}}to{{transform:scaleX(1)}}}}
</style>
{panel(w, h, "LIVE_TELEMETRY", "SELF-HOSTED · NO THIRD-PARTY WIDGETS")}
{''.join(cells)}
{''.join(bars)}
<text x="{cx0}" y="352" font-size="10.5" letter-spacing="2" fill="{DIM}">CONTRIBUTION PULSE · LAST 30 DAYS · {f30} TOTAL</text>
<line x1="{cx0}" y1="{cy0}" x2="{cx1}" y2="{cy0}" stroke="{LINE}" stroke-dasharray="2 5"/>
<text x="{cx1}" y="{cy0 - 4}" text-anchor="end" font-size="9.5" fill="{DIM2}">{vmax}</text>
<line x1="{cx0}" y1="{cy1}" x2="{cx1}" y2="{cy1}" stroke="{LINE}"/>
<g clip-path="url(#reveal)">
  <path d="{area}" fill="url(#areaG)"/>
  <path d="{line}" fill="none" stroke="{TEAL}" stroke-width="2" stroke-linejoin="round"/>
</g>
{peak}
<text x="{cx0}" y="{cy1 + 16}" font-size="9.5" fill="{DIM}">{last[0][0]}</text>
<text x="{cx1}" y="{cy1 + 16}" text-anchor="end" font-size="9.5" fill="{DIM}">{last[-1][0]}</text>
<text x="{w / 2}" y="{h - 8}" text-anchor="middle" font-size="9" letter-spacing="1.5" fill="{DIM2}">AUTO-RENDERED {stamp()} · GITHUB ACTIONS</text>
</svg>"""
    write_atomic("telemetry.svg", svg)


# ==================================================================== snake
def render_snake(d):
    w, h = 940, 270
    first = dt.date.fromisoformat(d["days"][0][0])
    start = first - dt.timedelta(days=(first.weekday() + 1) % 7)  # Sunday on/before
    counts = {date: c for date, c in d["days"]}
    ncols = (dt.date.fromisoformat(d["days"][-1][0]) - start).days // 7 + 1
    step, cell = 15, 11
    x0, y0 = (w - ncols * step) // 2, 102

    def pos(col, row):
        return x0 + col * step, y0 + row * step

    # serpentine path through every grid slot: adjacent moves of equal length,
    # so time-at-slot = index / (n - 1) of the loop
    order = []
    for col in range(ncols):
        rows = range(7) if col % 2 == 0 else range(6, -1, -1)
        order += [(col, r) for r in rows]
    n = len(order)
    dur = round(n * 0.085, 2)
    idx = {cr: i for i, cr in enumerate(order)}

    base, food = [], []
    for date, c in d["days"]:
        dd = dt.date.fromisoformat(date)
        col, row = (dd - start).days // 7, (dd.weekday() + 1) % 7
        x, y = pos(col, row)
        base.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{LEVELS[0]}"/>')
        if c:
            lvl = 1 if c <= 2 else 2 if c <= 5 else 3 if c <= 9 else 4
            f = idx[(col, row)] / (n - 1)
            food.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{LEVELS[lvl]}">'
                f'<title>{c} on {date}</title>'
                f'<animate attributeName="opacity" values="1;0" keyTimes="0;{f:.4f}" calcMode="discrete" '
                f'dur="{dur}s" repeatCount="indefinite"/></rect>')

    path = "M" + " L".join(f"{pos(c, r)[0] + cell / 2} {pos(c, r)[1] + cell / 2}" for c, r in order)
    seg_t = dur / (n - 1)
    body = []
    nseg = 8
    for i in range(nseg, -1, -1):  # draw tail first so the head is on top
        s = cell + 1 if i == 0 else cell - i * 0.45
        col = GOLD if i == 0 else TEAL
        op = 1 if i == 0 else 0.95 - i * 0.07
        begin = f' begin="-{dur - i * seg_t:.3f}s"' if i else ""
        glow = ' filter="url(#glow)"' if i == 0 else ""
        body.append(
            f'<rect x="{-s / 2:.2f}" y="{-s / 2:.2f}" width="{s:.2f}" height="{s:.2f}" rx="3.5" fill="{col}" '
            f'opacity="{op:.2f}"{glow}>'
            f'<animateMotion dur="{dur}s"{begin} repeatCount="indefinite"><mpath xlink:href="#snk" href="#snk"/></animateMotion></rect>')

    lg = "".join(
        f'<rect x="{x0 + i * 52}" y="{h - 34}" width="{cell}" height="{cell}" rx="2.5" fill="{LEVELS[i]}"/>'
        f'<text x="{x0 + i * 52 + 16}" y="{h - 24.5}" font-size="9.5" fill="{DIM}">{lbl}</text>'
        for i, lbl in enumerate(["0", "1-2", "3-5", "6-9", "10+"]))
    months = []
    seen = set()
    for col in range(ncols):
        dd = start + dt.timedelta(days=col * 7)
        key = (dd.year, dd.month)
        if dd.day <= 7 and key not in seen and col < ncols - 2:
            seen.add(key)
            months.append(f'<text x="{pos(col, 0)[0]}" y="{y0 - 8}" font-size="9.5" fill="{DIM}">{dd.strftime("%b")}</text>')

    svg = f"""{head(w, h)}
{DEFS}
{panel(w, h, "CONTRIBUTION.STREAM", "SNAKE.EXE · RENDERED DAILY")}
<text x="{x0}" y="{y0 - 28}" font-size="10.5" letter-spacing="1.5" fill="{TXT}">{d['total']:,} contributions in the last year · the snake eats them in order</text>
{''.join(months)}
{''.join(base)}
{''.join(food)}
<path id="snk" d="{path}" fill="none" stroke="none"/>
{''.join(body)}
{lg}
<text x="{w - x0}" y="{h - 24.5}" text-anchor="end" font-size="9" letter-spacing="1.5" fill="{DIM2}">AUTO-RENDERED {stamp()}</text>
</svg>"""
    write_atomic("snake.svg", svg)


# ================================================================= trophies
TIERS = [("S", GOLD, "#fde68a"), ("A", GOLD, "#fcd34d"), ("B", "#cbd5e1", "#f1f5f9"), ("C", "#d97706", "#fbbf24")]


def tier(v, th):  # th = thresholds for C, B, A, S
    for name, t in zip(["S", "A", "B", "C"], reversed(th)):
        if v >= t:
            return name
    return None


def render_trophies(d):
    _, lng = streaks(d["days"])
    commits = d["commits"] if d["commits"] is not None else d["total"]
    items = [
        ("COMMITS" if d["commits"] is not None else "CONTRIBS", commits, [50, 200, 500, 1000]),
        ("REPOS", d["repos"], [10, 30, 60, 100]),
        ("STARS", d["stars"], [1, 10, 30, 100]),
        ("FOLLOWERS", d["followers"], [5, 20, 50, 100]),
        ("PULL REQS", d["prs"], [1, 10, 50, 100]),
        ("ISSUES", d["issues"], [1, 10, 30, 100]),
        ("STREAK", lng, [3, 7, 30, 100]),
        ("EXPERIENCE", round(d["years"], 1), [1, 2, 3, 5]),
    ]
    w, h = 940, 250
    cw = (w - 40) / len(items)
    cards = []
    for i, (label, val, th) in enumerate(items):
        x = 20 + i * cw
        cx = x + cw / 2
        t = tier(val, th)
        meta = {k: (a, b) for k, a, b in TIERS}
        if t:
            c1, c2 = meta[t]
            gid = f"tg{i}"
            grad = (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
                    f'<stop offset="0" stop-color="{c2}"/><stop offset="1" stop-color="{c1}"/></linearGradient>')
            fill, stroke, op = f"url(#{gid})", c1, 1
        else:
            grad, fill, stroke, op = "", PANEL2, DIM2, 0.6
        nxt = next((n for n in th if val < n), None)
        sub = "MAX TIER" if nxt is None else f"next: {nxt}"
        shown = f"{val:g}y" if label == "EXPERIENCE" else f"{val:,}"
        glow = ' filter="url(#glow)"' if t == "S" else ""
        cards.append(f"""
<defs>{grad}</defs>
<rect x="{x + 5:.1f}" y="70" width="{cw - 10:.1f}" height="160" rx="12" fill="{PANEL2}" stroke="{LINE}"/>
<g transform="translate({cx:.1f} 90)" opacity="{op}"{glow}><g class="cup" style="animation-delay:-{i * 0.4:.1f}s">
  <path d="M-12 4 C-26 4 -26 22 -9 24 M12 4 C26 4 26 22 9 24" fill="none" stroke="{stroke}" stroke-width="3"/>
  <path d="M-18 0 H18 V8 C18 26 8 34 0 34 C-8 34 -18 26 -18 8 Z" fill="{fill}" stroke="{stroke}" stroke-width="1"/>
  <rect x="-3" y="34" width="6" height="9" fill="{stroke}"/>
  <rect x="-14" y="43" width="28" height="6" rx="2" fill="{fill}" stroke="{stroke}" stroke-width="1"/>
  <text x="0" y="22" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="800" fill="{BG if t else DIM}">{t or '?'}</text>
</g></g>
<text x="{cx:.1f}" y="166" text-anchor="middle" font-size="10" letter-spacing="1.2" fill="{DIM}">{label}</text>
<text x="{cx:.1f}" y="190" text-anchor="middle" font-family="{SANS}" font-size="18" font-weight="700" fill="{TXT}">{shown}</text>
<text x="{cx:.1f}" y="212" text-anchor="middle" font-size="9" fill="{DIM2}">{sub}</text>""")

    svg = f"""{head(w, h)}
{DEFS}
<style>
  .cup{{animation:bob 3.6s ease-in-out infinite}}
  @keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}
</style>
{panel(w, h, "TROPHY_SHELF", "TIERS  S · A · B · C  ·  SELF-COMPUTED")}
{''.join(cards)}
</svg>"""
    write_atomic("trophies.svg", svg)


# ===================================================================== main
def main():
    d = fetch()
    if len(d["days"]) < 30:
        raise RuntimeError(f"calendar too short ({len(d['days'])} days)")
    render_telemetry(d)
    render_snake(d)
    render_trophies(d)
    print("telemetry render complete; last-good assets replaced.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001 — never leave a half-broken asset
        print(f"FATAL: keeping last-good assets ({e})", file=sys.stderr)
        sys.exit(1)
