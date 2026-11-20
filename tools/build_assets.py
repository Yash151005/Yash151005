#!/usr/bin/env python3
"""
Builds the STATIC profile art in assets/ (run once, or after editing text here):

    python tools/build_assets.py

  header-banner.svg   animated name banner with self-hosted typing roles
  identity.svg        identity.sys holographic ID card (avatar embedded)
  system.svg          system-overview terminal
  uplink-*.svg        contact chips (linkedin, email, portfolio, github, instagram)
  divider.svg         section divider
  footer.svg          footer wave

Data-driven art (telemetry, snake, trophies) is rendered daily by
tools/render_telemetry.py instead.
Stdlib only. Everything is self-contained: no external fonts, images or URLs.
"""
import base64
import os
import random

from theme import (BG, BLUE, BLUE2, DEFS, DIM, DIM2, GOLD, LINE, PANEL2, ROOT,
                   ROSE, SANS, TEAL, TXT, esc, head, panel, write_atomic)


def anim_track(points):
    """[(t, v)] -> (keyTimes, values) strings, dropping duplicate key times."""
    pts = []
    for t, v in points:
        t = round(min(max(t, 0.0), 1.0), 4)
        if pts and pts[-1][0] == t:
            pts[-1] = (t, v)
        else:
            pts.append((t, v))
    if pts[0][0] != 0:
        pts.insert(0, (0.0, pts[0][1]))
    if pts[-1][0] != 1:
        pts.append((1.0, pts[-1][1]))
    return ";".join(f"{t:g}" for t, _ in pts), ";".join(f"{v:g}" for _, v in pts)


# ====================================================================== banner
def banner():
    w, h = 1000, 320
    rnd = random.Random(151005)

    stars = "".join(
        f'<circle cx="{rnd.uniform(0, w):.0f}" cy="{rnd.uniform(0, h):.0f}" r="{rnd.choice([0.6, 0.9, 1.2])}" '
        f'fill="#ffffff" class="tw" style="animation-delay:-{rnd.uniform(0, 4):.2f}s"/>'
        for _ in range(70))

    # --- neural network constellation (right side)
    layers = [(740, [90, 160, 230]), (820, [70, 130, 190, 250]), (900, [110, 210]), (960, [160])]
    nodes = [(x, y) for x, ys in layers for y in ys]
    edges, pulses = [], []
    k = 0
    for (xa, ya_list), (xb, yb_list) in zip(layers, layers[1:]):
        for ya in ya_list:
            for yb in yb_list:
                pid = f"e{k}"
                edges.append(f'<path id="{pid}" d="M{xa} {ya} L{xb} {yb}" stroke="{BLUE}" stroke-opacity="0.28" stroke-width="1"/>')
                if k % 2 == 0:
                    dur = 2.2 + (k % 5) * 0.35
                    pulses.append(
                        f'<circle r="2.2" fill="{TEAL}" filter="url(#glow)">'
                        f'<animateMotion dur="{dur:.2f}s" begin="-{(k * 0.37) % dur:.2f}s" repeatCount="indefinite">'
                        f'<mpath xlink:href="#{pid}" href="#{pid}"/></animateMotion></circle>')
                k += 1
    node_svg = "".join(
        f'<circle cx="{x}" cy="{y}" r="6" fill="{BG}" stroke="{TEAL if i % 3 else GOLD}" stroke-width="1.6" '
        f'class="nd" style="animation-delay:-{i * 0.3:.1f}s"/>'
        for i, (x, y) in enumerate(nodes))

    # --- self-hosted typing roles (replaces third-party typing widget)
    roles = [
        "AI Engineer :: agentic systems, RAG, LLM apps",
        "Data Scientist :: forecasting, anomalies, FL",
        "Software Developer :: Python, TypeScript, web",
        "raw data -> trained model -> shipped product",
    ]
    n, slot = len(roles), 4.0
    total = n * slot
    cw, x0, ty = 10.8, 84, 214
    clips, texts, cur_pts = [], [], []
    for i, line in enumerate(roles):
        tw = len(line) * cw
        a, b, c, d = i / n, (i + 0.45) / n, (i + 0.82) / n, (i + 0.97) / n
        kt, vals = anim_track([(a, 0), (b, tw), (c, tw), (d, 0)])
        clips.append(
            f'<clipPath id="tc{i}"><rect x="{x0}" y="{ty - 20}" height="28" width="0">'
            f'<animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{total}s" repeatCount="indefinite"/>'
            f'</rect></clipPath>')
        texts.append(
            f'<text x="{x0}" y="{ty}" font-size="18" fill="{TXT}" textLength="{tw:.1f}" '
            f'lengthAdjust="spacingAndGlyphs" clip-path="url(#tc{i})">{esc(line)}</text>')
        cur_pts += [(a, x0), (b, x0 + tw), (c, x0 + tw), (d, x0)]
    kt, vals = anim_track(cur_pts)
    cursor = (f'<rect y="{ty - 16}" width="10" height="20" fill="{TEAL}" class="blink" x="{x0}">'
              f'<animate attributeName="x" values="{vals}" keyTimes="{kt}" dur="{total}s" repeatCount="indefinite"/></rect>')

    chips, cx = [], 60
    for label, col in [("AI ENGINEER", BLUE), ("DATA SCIENTIST", TEAL), ("SOFTWARE DEVELOPER", GOLD)]:
        cwid = len(label) * 8.4 + 30
        chips.append(
            f'<rect x="{cx}" y="236" width="{cwid:.0f}" height="28" rx="14" fill="{col}" fill-opacity="0.10" stroke="{col}" stroke-opacity="0.7"/>'
            f'<circle cx="{cx + 14}" cy="250" r="3.2" fill="{col}"/>'
            f'<text x="{cx + 24}" y="254.5" font-size="12" letter-spacing="1.5" fill="{TXT}">{label}</text>')
        cx += cwid + 12

    svg = f"""{head(w, h)}
{DEFS}
<defs>
  <linearGradient id="nameG" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#93c5fd"/>
    <stop offset=".8" stop-color="{TEAL}"/><stop offset="1" stop-color="{GOLD}"/>
  </linearGradient>
  <linearGradient id="bgG" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#050a18"/><stop offset="1" stop-color="#081430"/>
  </linearGradient>
  <clipPath id="frame"><rect width="{w}" height="{h}" rx="18"/></clipPath>
  {''.join(clips)}
</defs>
<style>
  .tw{{animation:tw 4s ease-in-out infinite}}
  @keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:.9}}}}
  .au1{{animation:d1 14s ease-in-out infinite alternate}}
  .au2{{animation:d2 18s ease-in-out infinite alternate}}
  .au3{{animation:d1 22s ease-in-out infinite alternate-reverse}}
  @keyframes d1{{from{{transform:translate(-60px,0)}}to{{transform:translate(80px,30px)}}}}
  @keyframes d2{{from{{transform:translate(50px,20px)}}to{{transform:translate(-70px,-20px)}}}}
  .nd{{animation:nd 2.4s ease-in-out infinite}}
  @keyframes nd{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
  .blink{{animation:bl 1s steps(1) infinite}}
  @keyframes bl{{50%{{opacity:0}}}}
  .ul{{animation:ul 3.6s ease-in-out infinite}}
  @keyframes ul{{0%{{transform:scaleX(.15)}}50%{{transform:scaleX(1)}}100%{{transform:scaleX(.15)}}}}
  .scan{{animation:sc 6s linear infinite}}
  @keyframes sc{{from{{transform:translateY(-40px)}}to{{transform:translateY({h}px)}}}}
</style>
<g clip-path="url(#frame)">
  <rect width="{w}" height="{h}" fill="url(#bgG)"/>
  <rect width="{w}" height="{h}" fill="url(#grid)" opacity="0.35"/>
  <g filter="url(#blur)" opacity="0.55">
    <ellipse class="au1" cx="260" cy="60" rx="260" ry="70" fill="{BLUE2}"/>
    <ellipse class="au2" cx="640" cy="280" rx="240" ry="60" fill="{TEAL}" opacity="0.6"/>
    <ellipse class="au3" cx="900" cy="40" rx="160" ry="50" fill="{GOLD}" opacity="0.35"/>
  </g>
  {stars}
  {''.join(edges)}
  {''.join(pulses)}
  {node_svg}
  <g class="scan"><rect x="0" y="0" width="{w}" height="40" fill="url(#scanG)" opacity="0.10"/></g>

  <text x="60" y="78" font-size="14" letter-spacing="3" fill="{TEAL}">// hello, world. i am</text>
  <text x="56" y="150" font-family="{SANS}" font-size="70" font-weight="800" letter-spacing="2"
        fill="url(#nameG)" filter="url(#glow)" textLength="500" lengthAdjust="spacingAndGlyphs">YASH PAKALE</text>
  <g style="transform-box:fill-box;transform-origin:left center" class="ul">
    <rect x="60" y="166" width="500" height="3" rx="1.5" fill="url(#edgeG)"/>
  </g>
  <text x="60" y="{ty}" font-size="18" fill="{TEAL}">&gt;</text>
  {''.join(texts)}
  {cursor}
  {''.join(chips)}
  <text x="60" y="296" font-size="11.5" letter-spacing="2" fill="{DIM}"><tspan fill="{TEAL}">●</tspan> ONLINE  ·  PUNE, IN  ·  VIT  ·  github.com/Yash151005</text>
  <text x="{w - 30}" y="296" text-anchor="end" font-size="10.5" letter-spacing="2" fill="{DIM2}">NEURAL.OS v3</text>
</g>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" fill="none" stroke="url(#edgeG)" stroke-opacity="0.8" stroke-width="1.5"/>
</svg>"""
    write_atomic("header-banner.svg", svg)


# ==================================================================== identity
def identity():
    w, h = 920, 420
    src = os.path.join(ROOT, "tools", "avatar.jpg")
    with open(src, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    ax, ay, asz = 56, 84, 220
    cxa, cya = ax + asz / 2, ay + asz / 2
    hexp = " ".join(
        f"{cxa + (asz / 2) * c:.1f},{cya + (asz / 2) * s:.1f}"
        for c, s in [(0, -1), (0.866, -0.5), (0.866, 0.5), (0, 1), (-0.866, 0.5), (-0.866, -0.5)])

    rows = [
        ("NAME", "Yash Pradip Pakale", TXT),
        ("HANDLE", "@Yash151005", TXT),
        ("ROLE", "AI Engineer · Data Scientist · Software Dev", TXT),
        ("BASE", "Pune, India · VIT", TXT),
        ("CORE", "Agentic AI · RAG · ML pipelines · Full-stack", TXT),
        ("STACK", "Python · TypeScript · PyTorch · React · Flask", TXT),
        ("MODE", "hackathon speed, production habits", TXT),
        ("STATUS", "open to internships · collabs · hackathons", TXT),
    ]
    rx, ry0 = 340, 98
    row_svg = []
    for i, (k, v, col) in enumerate(rows):
        y = ry0 + i * 34
        dot = f'<circle cx="{rx + 92}" cy="{y - 4.5}" r="3.5" fill="{TEAL}" class="pulse"/>' if k == "STATUS" else ""
        vx = rx + 104 if k == "STATUS" else rx + 92
        row_svg.append(
            f'<g class="row" style="animation-delay:{0.15 + i * 0.18:.2f}s">'
            f'<text x="{rx}" y="{y}" font-size="11" letter-spacing="2" fill="{DIM}">{k}</text>'
            f'{dot}<text x="{vx}" y="{y}" font-size="14" fill="{col}">{esc(v)}</text>'
            f'<line x1="{rx}" y1="{y + 12}" x2="{w - 40}" y2="{y + 12}" stroke="{LINE}" stroke-dasharray="2 4"/></g>')

    rnd = random.Random(7)
    bars, bx = [], ax
    while bx < ax + asz - 4:
        bw = rnd.choice([1.5, 2, 3, 4])
        bars.append(f'<rect x="{bx:.1f}" y="356" width="{bw}" height="30" fill="{TXT}" opacity="0.75"/>')
        bx += bw + rnd.choice([1.5, 2, 3])

    svg = f"""{head(w, h)}
{DEFS}
<defs>
  <clipPath id="hexC"><polygon points="{hexp}"/></clipPath>
  <pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1.4" fill="#000" opacity="0.28"/>
  </pattern>
  <linearGradient id="tint" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BLUE2}" stop-opacity="0.05"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0.35"/>
  </linearGradient>
</defs>
<style>
  .spin{{transform-box:fill-box;transform-origin:center;animation:sp 18s linear infinite}}
  .spinr{{transform-box:fill-box;transform-origin:center;animation:sp 26s linear infinite reverse}}
  @keyframes sp{{to{{transform:rotate(360deg)}}}}
  .sweep{{animation:sw 3.8s ease-in-out infinite}}
  @keyframes sw{{0%{{transform:translateY(0)}}50%{{transform:translateY({asz - 6}px)}}100%{{transform:translateY(0)}}}}
  .row{{opacity:0;animation:in .6s ease-out forwards}}
  @keyframes in{{from{{opacity:0;transform:translateX(12px)}}to{{opacity:1;transform:none}}}}
  .pulse{{animation:pl 1.6s ease-in-out infinite}}
  @keyframes pl{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
</style>
{panel(w, h, "IDENTITY.SYS", "VERIFIED · CLEARANCE: BUILDER")}
<polygon points="{hexp}" fill="{PANEL2}"/>
<g clip-path="url(#hexC)">
  <image x="{ax}" y="{ay}" width="{asz}" height="{asz}" preserveAspectRatio="xMidYMid slice"
         href="data:image/jpeg;base64,{b64}" xlink:href="data:image/jpeg;base64,{b64}"/>
  <rect x="{ax}" y="{ay}" width="{asz}" height="{asz}" fill="url(#tint)"/>
  <rect x="{ax}" y="{ay}" width="{asz}" height="{asz}" fill="url(#lines)"/>
  <g class="sweep"><rect x="{ax}" y="{ay}" width="{asz}" height="6" fill="{TEAL}" opacity="0.55" filter="url(#glow)"/></g>
</g>
<polygon points="{hexp}" fill="none" stroke="{TEAL}" stroke-width="1.8" filter="url(#glow)"/>
<circle class="spin" cx="{cxa}" cy="{cya}" r="{asz / 2 + 12}" fill="none" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="4 10 30 10"/>
<circle class="spinr" cx="{cxa}" cy="{cya}" r="{asz / 2 + 20}" fill="none" stroke="{GOLD}" stroke-opacity="0.6" stroke-width="1" stroke-dasharray="2 14"/>
{''.join(bars)}
<text x="{ax}" y="402" font-size="10.5" letter-spacing="2.4" fill="{DIM}">ID // YP-151005</text>
{''.join(row_svg)}
<text x="{rx}" y="{h - 20}" font-size="11" letter-spacing="1.6" fill="{DIM2}">MISSION :: data <tspan fill="{TEAL}">➜</tspan> model <tspan fill="{TEAL}">➜</tspan> product</text>
</svg>"""
    write_atomic("identity.svg", svg)


# ==================================================================== terminal
def system():
    w, h = 620, 400
    P = f'<tspan fill="{TEAL}">yash</tspan><tspan fill="{DIM}">@</tspan><tspan fill="{BLUE}">neural-os</tspan><tspan fill="{DIM}">:~$</tspan> '
    lines = [
        (P + "whoami", 0.04),
        (f'<tspan fill="{TXT}">Yash Pakale · AI Engineer · Data Scientist · SWE</tspan>', 0.10),
        (P + "cat focus.json", 0.18),
        (f'<tspan fill="{DIM}">{{</tspan> <tspan fill="{GOLD}">"ai"</tspan><tspan fill="{DIM}">:</tspan> <tspan fill="{TXT}">"LLM agents, RAG, multi-provider apps",</tspan>', 0.24),
        (f'  <tspan fill="{GOLD}">"ds"</tspan><tspan fill="{DIM}">:</tspan> <tspan fill="{TXT}">"forecasting, anomalies, fairness",</tspan>', 0.28),
        (f'  <tspan fill="{GOLD}">"sw"</tspan><tspan fill="{DIM}">:</tspan> <tspan fill="{TXT}">"Python, TypeScript, full-stack"</tspan> <tspan fill="{DIM}">}}</tspan>', 0.32),
        (P + "ls ./projects | wc -l", 0.42),
        (f'<tspan fill="{TXT}">70+  </tspan><tspan fill="{DIM}"># hackathons, research, products</tspan>', 0.48),
        (P + "./ship --from data --to product", 0.58),
        (f'<tspan fill="{BLUE}">[■■■■■■■■■■■■■■■■■■■■]</tspan> <tspan fill="{TXT}">100%</tspan> <tspan fill="{TEAL}">deployed ✓</tspan>', 0.70),
        (P, 0.78),
    ]
    dur = 16
    out = []
    for i, (txt, t) in enumerate(lines):
        y = 88 + i * 27
        out.append(
            f'<text x="28" y="{y}" font-size="13.5" fill="{TXT}" xml:space="preserve">{txt}'
            f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;{t};0.97" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/></text>')
    cy = 88 + (len(lines) - 1) * 27
    cursor = (f'<rect x="200" y="{cy - 13}" width="9" height="17" fill="{TEAL}" class="blink">'
              f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;0.78;0.97" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/></rect>')
    svg = f"""{head(w, h)}
{DEFS}
<style>.blink{{animation:bl 1s steps(1) infinite}}@keyframes bl{{50%{{opacity:0}}}}</style>
{panel(w, h, "SYSTEM_OVERVIEW", "zsh · 620×400")}
{''.join(out)}
{cursor}
</svg>"""
    write_atomic("system.svg", svg)


# ====================================================================== uplink
GITHUB_D = ("M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 "
            "0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7"
            "c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998"
            ".108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22"
            "-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405"
            " 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22"
            " 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286"
            " 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12")

ICONS = {
    "linkedin": '<text x="12" y="17.5" text-anchor="middle" font-family="Arial,sans-serif" font-weight="700" font-size="15" fill="#fff">in</text>',
    "email": '<rect x="3" y="5.5" width="18" height="13" rx="2" fill="none" stroke="#fff" stroke-width="1.8"/><path d="M3.5 6.5 12 13l8.5-6.5" fill="none" stroke="#fff" stroke-width="1.8"/>',
    "portfolio": '<circle cx="12" cy="12" r="9" fill="none" stroke="#fff" stroke-width="1.7"/><ellipse cx="12" cy="12" rx="4" ry="9" fill="none" stroke="#fff" stroke-width="1.5"/><path d="M3 12h18M5 7.5h14M5 16.5h14" stroke="#fff" stroke-width="1.3"/>',
    "github": f'<path d="{GITHUB_D}" fill="#fff"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="17.3" cy="6.7" r="1.2" fill="#fff"/>',
}


def chip(key, label, handle, brand):
    w, h = 320, 76
    svg = f"""{head(w, h)}
{DEFS}
<defs>
  <clipPath id="cc"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14"/></clipPath>
  <linearGradient id="shG" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".10"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
</defs>
<style>
  .sh{{animation:sh 4.2s ease-in-out infinite}}
  @keyframes sh{{0%{{transform:translateX(-140px)}}60%,100%{{transform:translateX({w + 40}px)}}}}
  .ring{{transform-box:fill-box;transform-origin:center;animation:rg 2.6s ease-out infinite}}
  @keyframes rg{{0%{{opacity:.7;transform:scale(1)}}100%{{opacity:0;transform:scale(1.35)}}}}
  .ar{{animation:ar 1.8s ease-in-out infinite}}
  @keyframes ar{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(3px,-3px)}}}}
</style>
<g clip-path="url(#cc)">
  <rect width="{w}" height="{h}" fill="url(#panelG)"/>
  <rect width="{w}" height="{h}" fill="url(#grid)" opacity="0.5"/>
  <rect x="0" y="0" width="5" height="{h}" fill="{brand}"/>
  <rect class="sh" x="0" y="0" width="120" height="{h}" fill="url(#shG)"/>
</g>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="none" stroke="{brand}" stroke-opacity="0.85" stroke-width="1.4"/>
<rect class="ring" x="20" y="16" width="44" height="44" rx="11" fill="none" stroke="{brand}"/>
<rect x="20" y="16" width="44" height="44" rx="11" fill="{brand}"/>
<g transform="translate(30 26) scale(1)">{ICONS[key]}</g>
<text x="80" y="34" font-size="11" letter-spacing="2.4" fill="{DIM}">{esc(label)}</text>
<text x="80" y="56" font-family="{SANS}" font-size="{16 if len(handle) <= 18 else 14.5}" font-weight="600" fill="{TXT}">{esc(handle)}</text>
<g class="ar"><text x="{w - 24}" y="46" text-anchor="end" font-size="20" fill="{brand}">↗</text></g>
</svg>"""
    write_atomic(f"uplink-{key}.svg", svg)


def uplinks():
    chip("linkedin", "UPLINK // LINKEDIN", "Yash Pakale", "#0A66C2")
    chip("email", "UPLINK // EMAIL", "yashpakale99@gmail.com", "#D14836")
    chip("portfolio", "UPLINK // PORTFOLIO", "yash151005.github.io", BLUE2)
    chip("github", "UPLINK // GITHUB", "@Yash151005", "#6e7681")
    chip("instagram", "UPLINK // INSTAGRAM", "@Yashpakale.swami", "#E4405F")


# ============================================================ divider + footer
def divider():
    w, h = 1000, 16
    svg = f"""{head(w, h)}
{DEFS}
<style>.mv{{animation:mv 5s linear infinite}}@keyframes mv{{from{{transform:translateX(-120px)}}to{{transform:translateX({w + 120}px)}}}}</style>
<rect x="0" y="7.25" width="{w}" height="1.5" fill="url(#edgeG)" opacity="0.45"/>
<g class="mv"><rect x="0" y="6.5" width="120" height="3" rx="1.5" fill="{TEAL}" filter="url(#glow)" opacity="0.9"/></g>
<rect x="{w / 2 - 5}" y="3" width="10" height="10" transform="rotate(45 {w / 2} 8)" fill="{BG}" stroke="{GOLD}" stroke-width="1.4"/>
</svg>"""
    write_atomic("divider.svg", svg)


def footer():
    w, h = 1000, 170

    def wave(amp, phase, base):
        pts = []
        for i in range(0, 11):
            x = i * 100
            y = base + amp * (1 if (i + phase) % 2 else -1)
            pts.append((x, y))
        d = f"M0 {h} L0 {pts[0][1]} "
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            d += f"C{x1 + 50} {y1} {x2 - 50} {y2} {x2} {y2} "
        return d + f"L{w} {h} Z"

    layers = []
    for i, (col, op, base, amp, dur) in enumerate(
            [(BLUE2, 0.35, 92, 14, 7), (TEAL, 0.25, 108, 12, 9), ("#0b1d45", 1, 126, 10, 11)]):
        a, b = wave(amp, 0, base), wave(amp, 1, base)
        layers.append(
            f'<path d="{a}" fill="{col}" fill-opacity="{op}">'
            f'<animate attributeName="d" values="{a};{b};{a}" dur="{dur}s" repeatCount="indefinite"/></path>')
    svg = f"""{head(w, h)}
{DEFS}
<defs><clipPath id="fc"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18"/></clipPath></defs>
<style>.fd{{animation:fd 3.2s ease-in-out infinite}}@keyframes fd{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}</style>
<g clip-path="url(#fc)">
  <rect width="{w}" height="{h}" fill="url(#panelG)"/>
  <rect width="{w}" height="{h}" fill="url(#grid)" opacity="0.4"/>
  {''.join(layers)}
</g>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" fill="none" stroke="url(#edgeG)" stroke-opacity="0.75" stroke-width="1.4"/>
<text x="{w / 2}" y="40" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="600" fill="{TXT}">thanks for scrolling. let's build something that ships.</text>
<text class="fd" x="{w / 2}" y="66" text-anchor="middle" font-size="11" letter-spacing="3" fill="{TEAL}">YASH.PAKALE // NEURAL.OS · END OF TRANSMISSION</text>
<text x="{w / 2}" y="156" text-anchor="middle" font-size="10" letter-spacing="2" fill="{DIM}">data ➜ model ➜ product</text>
</svg>"""
    write_atomic("footer.svg", svg)


if __name__ == "__main__":
    banner()
    identity()
    system()
    uplinks()
    divider()
    footer()
