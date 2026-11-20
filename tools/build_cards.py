#!/usr/bin/env python3
"""
Builds the animated PROJECT + RESEARCH cards in assets/cards/:

    python tools/build_cards.py

  feat-<slug>.svg     featured project card (live mini-visual per category)
  more-<slug>.svg     compact card for every project under "More builds"
  paper-<slug>.svg    IEEE publication card (animated research visual)
  strip-<key>.svg     animated category header strip
  more-teaser.svg     "+N more builds" banner shown above the collapsed list

Edit the PROJECT / MORE / PAPERS tables below, re-run, and paste nothing:
the README references the files by slug. Stdlib only, no external fonts,
images or URLs. Animations use CSS + SMIL, both render on github.com.
"""
import os
import textwrap

import theme
from theme import (BG, BLUE, BLUE2, DEFS, DIM, DIM2, GOLD, LINE, PANEL2, ROSE,
                   SANS, TEAL, TXT, esc, head, write_atomic)

theme.OUT = os.path.join(theme.ROOT, "assets", "cards")
SOFT = "#b8c4e0"            # body copy: brighter than DIM, calmer than TXT
IEEE = "#00629B"            # IEEE brand blue
GH = "https://github.com/Yash151005/"

CATS = {
    "ai": dict(color=BLUE, label="AI ENGINEERING", sub="agents · LLMs · RAG", glyph="◈"),
    "ds": dict(color=TEAL, label="DATA SCIENCE & ML", sub="forecasting · privacy · fairness", glyph="◭"),
    "sw": dict(color=GOLD, label="SOFTWARE & COMPUTER VISION", sub="products · vision · web", glyph="▣"),
}

# ------------------------------------------------------------------ data
# (slug, title, repo, category, description, tags)
FEATURED = [
    ("docmind", "DocMind", "docmind", "ai",
     "Document-to-action engine: turns contracts, reports and notes into action items, red flags and key decisions.",
     ["Python", "Claude", "GPT-4o", "Gemini"]),
    ("complygenie", "ComplyGenie AI", "ComplyGenie-AI", "ai",
     "RAG recommendation engine that finds the BIS standards that apply to an Indian small business's products.",
     ["Python", "RAG", "NLP"]),
    ("synapse", "Synapse", "Synapse", "ai",
     "Voice-first agent marketplace: splits a goal, hires specialist agents in parallel, settles in USDC on Stellar.",
     ["TypeScript", "Multi-agent", "Stellar"]),
    ("pipelinesage", "PipelineSage AI", "PipelineSage-AI", "ai",
     "DevSecOps assistant: triages CI/CD failures, flags risky code, suggests fixes and scores release readiness.",
     ["Python", "LLM", "GitLab API"]),
    ("fedscore", "FedScore", "FedScore", "ds",
     "Federated credit scoring on alternative data (UPI, telecom) for credit-invisible users, with no raw data shared.",
     ["Python", "Federated", "Privacy"]),
    ("climaguard", "ClimaGuard AI", "ClimaGuard-AI", "ds",
     "Hyperlocal early warning: ward-level flood, heatwave and landslide risk map with a 72-hour forecast.",
     ["Python", "Forecasting", "Geospatial"]),
    ("fairnexa", "FairNexa", "FairNexa", "ds",
     "Fairness + explainability audits: probes a model's API, measures bias across groups, writes the audit report.",
     ["Python", "Responsible AI", "XAI"]),
    ("gendata", "GenData-Insight", "GenData-Insight", "ds",
     "Synthetic-data evaluator: KS, JS divergence, Wasserstein, autoencoder checks, ML utility and privacy scores.",
     ["Python", "Statistics", "Deep Learning"]),
    ("terravoxis", "TerraVoxis", "TerraVoxis", "sw",
     "NASA Space Apps 2026: an Earth Information Jukebox that turns Earth-observation data into sound.",
     ["TypeScript", "Sonification", "Live"]),
    ("karigartrust", "KarigarTrust", "KarigarTrust", "sw",
     "Agentic two-sided gold ledger for jewellers and goldsmiths: issued, returned, wasted, settled, both verified.",
     ["Agentic AI", "Ledger", "Fintech"]),
    ("autofix", "AutoFix AI", "AutofixAI", "sw",
     "End-to-end pipeline that detects exterior vehicle damage with YOLO and estimates the repair cost.",
     ["Python", "YOLO", "Vision"]),
    ("sentineliq", "SentinelIQ", "SentinelIQ", "sw",
     "Insider-threat monitoring for Bank of Maharashtra (Finspark 2026): hybrid ML anomalies + live risk dashboard.",
     ["Python", "Anomaly", "Security"]),
]

MORE = [
    # ---- AI & agents
    ("lifeos", "LifeOS", "LifeOS", "ai", "AI action agent: plan, approve, execute, verify, backed by real SQLite tools.", ["Python", "Agents"]),
    ("testgenie", "TestGenie AI", "TestGenie-AI", "ai", "Generates QA test cases from requirements using several LLM providers.", ["Python", "LLM"]),
    ("mandatepay", "MandatePay AI", "MandatePay-AI", "ai", "Agentic commerce with spending limits, human approval and a hash-chained audit log.", ["Python", "Agentic AI"]),
    ("deadreckoning", "Dead Reckoning", "Dead-Reckoning", "ai", "Infers full specs for undocumented industrial parts from physics and vision.", ["Python", "Vision"]),
    ("kaamsetu", "KaamSetu AI", "KaamSetu", "ai", "Multilingual, voice-first safety net for informal and migrant workers.", ["JavaScript", "Voice AI"]),
    ("nagrik", "Nagrik Sahayak", "Nagrik-Sahayak", "ai", "Multilingual GenAI civic companion for government services.", ["Python", "GenAI"]),
    ("engageai", "EngageAI", "EngageAI", "ai", "Detects customer life events from transactions and sends personalized nudges.", ["Python", "ML"]),
    ("sentinelai", "SentinelAI", "SentinelAI", "ai", "Grooming-risk detection and evidence correlation (Hac'KP 2026).", ["Python", "NLP"]),
    ("druggpt", "DrugGPT", "DrugGpt", "ai", "Explainable drug-repurposing engine with a full-stack React interface.", ["Python", "React"]),
    ("paal", "PAAL", "PAAL", "ai", "Public AI Access Layer: an AI intermediary between citizens and government services.", ["AI Platform", "GovTech"]),
    ("ksp-ai", "KSP Crime Intel", "ksp-ai", "ai", "Local conversational AI over a police crime database with Ollama + Llama 3 (KSP Datathon 2026).", ["Ollama", "Llama 3"]),
    ("dataforge", "DataForge AI", "dataforge-ai", "ai", "AI data-preparation pipeline: raw data in, model-ready data out.", ["Python", "Streamlit"]),
    # ---- data science & analytics
    ("mindmirror", "MindMirror AI", "MindMirror-AI", "ds", "Stress detection from face (OpenCV) and voice (librosa MFCC).", ["OpenCV", "Audio ML"]),
    ("graminpulse", "GraminPulse", "GraminPulse", "ds", "Cash-flow forecasting and repayment-risk scoring for rural micro-enterprises.", ["Python", "Forecasting"]),
    ("stockpulse", "StockPulse AI", "StockPulse-AI", "ds", "Snowflake-native stock-health intelligence for hospitals and NGOs.", ["Snowflake", "Python"]),
    ("ksp-analytics", "KSP Analytics", "ksp-analytics", "ds", "Crime analytics with hotspot maps, network graphs and a local LLM.", ["Python", "Geospatial"]),
    ("redrob", "Candidate Ranker", "redrob-candidate-ranker", "ds", "Ranks the top 100 candidates out of 100,000 for a role.", ["Python", "Ranking"]),
    ("veriesg", "VeriESG", "VeriESG", "ds", "ESG compliance checks with smart contracts and ML anomaly detection.", ["Python", "Blockchain"]),
    ("indradhanu", "Indradhanu", "Indradhanu", "ds", "Climate resilience linking health, marine and circular-economy data with LSTM forecasts.", ["LSTM", "Climate"]),
    ("greenchain", "GreenChain", "GreenChain", "ds", "Tracks fleet emissions against India's baseline, grades drivers, earns carbon credits.", ["TypeScript", "Gemini"]),
    ("saferoute", "SafeRoute.AI", "Real-Time-Route-Safety-Scoring-System-for-Pedestrians-or-Vehicles", "ds", "Real-time safety scoring and safer route suggestions for pedestrians and drivers.", ["TypeScript", "Maps"]),
    # ---- software, web & computer vision
    ("railguard", "RailGuard", "RailGuard", "sw", "Real-time railway anomaly detection with a rules + Llama 3 hybrid.", ["Python", "Llama 3"]),
    ("visionguard", "VisionGuard AI", "VisionGuard-AI", "sw", "Explainable OpenCV visual-inspection agent for images and video.", ["Python", "OpenCV"]),
    ("focusguard", "FocusGuard", "Student-Attention-Detection", "sw", "Flask + MediaPipe student attention monitoring from a webcam.", ["Flask", "MediaPipe"]),
    ("facechain", "FaceChain", "FaceChain", "sw", "Face detection + reverse search, with an immutable on-chain record.", ["Python", "Blockchain"]),
    ("faceauth", "Offline Face Auth", "NHAI", "sw", "Offline face recognition and liveness detection for field staff (NHAI hackathon).", ["Kotlin", "On-device ML"]),
    ("roadcrack", "Road Crack Detect", "smart-road-crack-detectction-web-app", "sw", "Flask web app that detects and catalogues road cracks from uploaded images.", ["Flask", "CV"]),
    ("provenancex", "ProvenanceX", "PROVENANCEX", "sw", "Registers and verifies the source and edit history of photos, videos and files.", ["JavaScript", "Provenance"]),
    ("roadbid", "RoadBid", "RoadBid", "sw", "Transparent road-repair tenders: officers post, contractors bid, citizens verify.", ["JavaScript", "Maps"]),
    ("noted", "Noted.", "Symptomline", "sw", "Turns symptom logs into doctor-ready timelines and PDF reports.", ["JavaScript", "Health"]),
    ("carecircle", "CareCircle", "CareCircle", "sw", "Shared medication and appointment manager for elderly care.", ["Python", "Health"]),
    ("steadystep", "SteadyStep", "SteadyStep", "sw", "Adaptive, no-blame behavior-change coach.", ["Python", "Wellness"]),
    ("climascope", "CLIMASCOPE", "CLIMASCOPE", "sw", "Checks whether the evidence actually supports a climate decision.", ["TypeScript", "Climate"]),
    ("teamsync", "TeamSync", "TeamSync", "sw", "Mobile-first teammate discovery and matching for hackathons.", ["JavaScript", "Web"]),
    ("freelance", "Freelance Bidding", "Freelance-bidding-platform", "sw", "Freelance marketplace with a weighted auction algorithm for picking the best bid.", ["JavaScript", "Algorithms"]),
    ("artgen", "AI Art Generator", "ai-art-generator", "sw", "Text-to-image art generator supporting several diffusion models.", ["TypeScript", "GenAI"]),
]

# (slug, title, subtitle, url, doc id, visual, keywords)
PAPERS = [
    ("attention", "Student Attention Detection System",
     "Real-Time Classroom Engagement Monitoring Using Computer Vision and Deep Learning.",
     "https://ieeexplore.ieee.org/document/11735961", "11735961", "vision",
     ["Computer Vision", "Deep Learning", "Real-Time"]),
    ("brainwave", "Brain Frequency Analysis Concentration Level Prediction",
     "A research study exploring brain-frequency signals for concentration-level prediction.",
     "https://ieeexplore.ieee.org/document/11747711/", "11747711", "eeg",
     ["Brain Frequencies", "Signal Analysis", "Prediction"]),
]


# ----------------------------------------------------------------- helpers
def wrap(text, width, max_lines, where):
    lines = textwrap.wrap(text, width)
    if len(lines) > max_lines:
        raise SystemExit(f"{where}: text needs {len(lines)} lines (max {max_lines}): {text!r}")
    return lines


def chips(tags, x, y, color, size=11, h=22):
    out = []
    for t in tags:
        w = len(t) * size * 0.62 + 18
        out.append(
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{color}" fill-opacity="0.10" '
            f'stroke="{color}" stroke-opacity="0.55"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + size * 0.36:.1f}" text-anchor="middle" font-size="{size}" '
            f'fill="{TXT}">{esc(t)}</text>')
        x += w + 8
    return "".join(out), x


def card_frame(w, h, color, rx, delay, trace_len=140):
    """Panel, grid, shimmer sweep and a light that runs around the border."""
    perim = 2 * (w + h)
    return f"""
<defs>
  <clipPath id="cf"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx}"/></clipPath>
  <linearGradient id="shG" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="haloG" cx="1" cy="0" r="0.9">
    <stop offset="0" stop-color="{color}" stop-opacity="0.22"/><stop offset="1" stop-color="{color}" stop-opacity="0"/>
  </radialGradient>
</defs>
<style>
  .sh{{animation:sh 6s ease-in-out infinite;animation-delay:{delay:.2f}s}}
  @keyframes sh{{0%{{transform:translateX(-{w // 2}px)}}55%,100%{{transform:translateX({w + 60}px)}}}}
  .trace{{animation:tr 7s linear infinite;animation-delay:-{delay * 2:.2f}s}}
  @keyframes tr{{from{{stroke-dashoffset:{perim}}}to{{stroke-dashoffset:0}}}}
  .in{{animation:in .8s cubic-bezier(.2,.7,.2,1) both}}
  @keyframes in{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
  .pulse{{animation:pl 1.8s ease-in-out infinite}}
  @keyframes pl{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
  .ring{{transform-box:fill-box;transform-origin:center;animation:rg 2.2s ease-out infinite}}
  @keyframes rg{{0%{{opacity:.8;transform:scale(1)}}100%{{opacity:0;transform:scale(3)}}}}
  .ar{{animation:ar 1.6s ease-in-out infinite}}
  @keyframes ar{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(3px,-3px)}}}}
</style>
<g clip-path="url(#cf)">
  <rect width="{w}" height="{h}" fill="url(#panelG)"/>
  <rect width="{w}" height="{h}" fill="url(#grid)" opacity="0.45"/>
  <rect width="{w}" height="{h}" fill="url(#haloG)"/>
  <rect class="sh" x="0" y="0" width="{w // 3}" height="{h}" fill="url(#shG)"/>
</g>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx}" fill="none" stroke="{LINE}" stroke-width="1.2"/>
<rect class="trace" x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx}" fill="none" stroke="{color}" stroke-width="1.8"
      stroke-dasharray="{trace_len} {perim - trace_len}" stroke-linecap="round" filter="url(#glow)"/>"""


# ------------------------------------------------------------ mini visuals
def vis_neural(color):
    """Tiny neural net with signals travelling along the edges (100x90 box)."""
    layers = [(14, [18, 45, 72]), (50, [12, 34, 56, 78]), (86, [30, 60])]
    edges, pulses, k = [], [], 0
    for (xa, ya_l), (xb, yb_l) in zip(layers, layers[1:]):
        for ya in ya_l:
            for yb in yb_l:
                edges.append(f'<path id="e{k}" d="M{xa} {ya} L{xb} {yb}" stroke="{color}" stroke-opacity="0.25"/>')
                if k % 3 == 0:
                    dur = 1.6 + (k % 4) * 0.3
                    pulses.append(
                        f'<circle r="2" fill="{TEAL}"><animateMotion dur="{dur:.1f}s" begin="-{k * 0.23 % dur:.2f}s" '
                        f'repeatCount="indefinite"><mpath href="#e{k}" xlink:href="#e{k}"/></animateMotion></circle>')
                k += 1
    nodes = "".join(
        f'<circle cx="{x}" cy="{y}" r="4.2" fill="{BG}" stroke="{color if i % 3 else GOLD}" stroke-width="1.4" '
        f'class="pulse" style="animation-delay:-{i * 0.27:.2f}s"/>'
        for i, (x, y) in enumerate((x, y) for x, ys in layers for y in ys))
    return "".join(edges) + "".join(pulses) + nodes


def vis_chart(color):
    """Bars that breathe and a forecast line that keeps redrawing."""
    bars = []
    for i, hgt in enumerate([28, 46, 36, 58, 50, 68]):
        bars.append(
            f'<rect x="{10 + i * 14}" y="{82 - hgt}" width="9" height="{hgt}" rx="2" fill="{color}" fill-opacity="0.28" '
            f'class="bar" style="animation-delay:-{i * 0.35:.2f}s"/>')
    pts = "10,66 24,54 38,60 52,38 66,44 80,22 94,14"
    return f"""
<style>
  .bar{{transform-box:fill-box;transform-origin:bottom;animation:br 2.4s ease-in-out infinite}}
  @keyframes br{{0%,100%{{transform:scaleY(.6)}}50%{{transform:scaleY(1)}}}}
  .ln{{stroke-dasharray:130;animation:ln 3.2s ease-in-out infinite}}
  @keyframes ln{{0%{{stroke-dashoffset:130}}55%,85%{{stroke-dashoffset:0}}100%{{stroke-dashoffset:-130}}}}
</style>
<line x1="6" y1="82" x2="98" y2="82" stroke="{DIM2}"/>
{''.join(bars)}
<polyline class="ln" points="{pts}" fill="none" stroke="{GOLD}" stroke-width="2" stroke-linejoin="round" filter="url(#glow)"/>
<circle cx="94" cy="14" r="3" fill="{GOLD}" class="pulse"/>"""


def vis_scan(color):
    """Viewfinder with a sweeping scan line and a locking detection box."""
    c = color
    br = (f'<path d="M6 18V6H18 M82 6H94V18 M94 72V84H82 M18 84H6V72" fill="none" stroke="{c}" stroke-width="2"/>')
    return f"""
<style>
  .sc{{animation:sc 2.6s ease-in-out infinite}}
  @keyframes sc{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(70px)}}}}
  .lock{{transform-box:fill-box;transform-origin:center;animation:lk 2.6s ease-in-out infinite}}
  @keyframes lk{{0%,20%{{opacity:0;transform:scale(1.5)}}40%,85%{{opacity:1;transform:scale(1)}}100%{{opacity:0;transform:scale(1)}}}}
</style>
{br}
<rect x="30" y="38" width="40" height="22" rx="5" fill="{DIM2}" fill-opacity="0.6"/>
<circle cx="38" cy="62" r="5" fill="{DIM2}"/><circle cx="62" cy="62" r="5" fill="{DIM2}"/>
<rect x="38" y="30" width="22" height="10" rx="3" fill="{DIM2}" fill-opacity="0.6"/>
<g class="lock"><rect x="24" y="24" width="52" height="46" fill="none" stroke="{TEAL}" stroke-width="1.6" stroke-dasharray="5 3"/>
<rect x="24" y="15" width="34" height="9" fill="{TEAL}"/><text x="27" y="22" font-size="7" fill="{BG}">DETECT</text></g>
<g class="sc"><rect x="8" y="8" width="84" height="2" fill="{c}" filter="url(#glow)"/></g>"""


VISUALS = {"ai": vis_neural, "ds": vis_chart, "sw": vis_scan}


# ------------------------------------------------------------ featured card
def featured_card(i, n, slug, title, repo, cat, desc, tags):
    w, h = 500, 260
    c = CATS[cat]
    col = c["color"]
    lines = wrap(desc, 46, 3, slug)
    desc_svg = "".join(
        f'<text x="26" y="{132 + j * 21}" font-family="{SANS}" font-size="13.5" fill="{SOFT}" class="in" '
        f'style="animation-delay:{0.35 + j * 0.12:.2f}s">{esc(t)}</text>' for j, t in enumerate(lines))
    chip_svg, _ = chips(tags, 26, 196, col)
    svg = f"""{head(w, h)}
{DEFS}
{card_frame(w, h, col, 16, (i % 4) * 0.7)}
<rect x="22" y="22" width="4" height="16" rx="2" fill="{col}"/>
<text x="34" y="35" font-size="11" letter-spacing="2.2" fill="{col}">{esc(c['label'])}</text>
<text x="{w - 26}" y="35" text-anchor="end" font-size="11" letter-spacing="2" fill="{DIM}">{i + 1:02d} / {n:02d}</text>
<line x1="22" y1="50" x2="{w - 22}" y2="50" stroke="{LINE}"/>
<g transform="translate({w - 126} 62)">
  <rect x="0" y="0" width="100" height="90" rx="10" fill="{BG}" fill-opacity="0.65" stroke="{LINE}"/>
  {VISUALS[cat](col)}
</g>
<text x="24" y="98" font-family="{SANS}" font-size="27" font-weight="700" fill="{TXT}" class="in" style="animation-delay:.15s">{esc(title)}</text>
<rect x="26" y="108" width="60" height="2.5" rx="1.2" fill="{col}" class="in" style="animation-delay:.25s"/>
{desc_svg}
<g class="in" style="animation-delay:.75s">{chip_svg}</g>
<line x1="22" y1="232" x2="{w - 22}" y2="232" stroke="{LINE}" stroke-dasharray="2 4"/>
<circle cx="30" cy="246" r="3" fill="{TEAL}"/><circle cx="30" cy="246" r="3" fill="none" stroke="{TEAL}" class="ring"/>
<text x="40" y="250" font-size="10.5" letter-spacing="1" fill="{DIM}">github.com/Yash151005/{esc(repo[:30])}</text>
<g class="ar"><text x="{w - 26}" y="250" text-anchor="end" font-size="11" font-weight="700" letter-spacing="2" fill="{col}">VIEW REPO ↗</text></g>
</svg>"""
    write_atomic(f"feat-{slug}.svg", svg)


# ---------------------------------------------------------------- more card
def more_card(i, slug, title, repo, cat, desc, tags):
    w, h = 340, 172
    c = CATS[cat]
    col = c["color"]
    lines = wrap(desc, 44, 3, slug)
    desc_svg = "".join(
        f'<text x="20" y="{82 + j * 17}" font-family="{SANS}" font-size="12" fill="{SOFT}">{esc(t)}</text>'
        for j, t in enumerate(lines))
    chip_svg, _ = chips(tags, 20, 136, col, size=10, h=20)
    short = {"ai": "AI · AGENTS", "ds": "DATA · ML", "sw": "SOFTWARE · CV"}[cat]
    svg = f"""{head(w, h)}
{DEFS}
{card_frame(w, h, col, 12, (i % 6) * 0.5, trace_len=90)}
<circle cx="24" cy="24" r="3.5" fill="{col}"/><circle cx="24" cy="24" r="3.5" fill="none" stroke="{col}" class="ring" style="animation-delay:-{i * 0.3 % 2.2:.2f}s"/>
<text x="34" y="28" font-size="9.5" letter-spacing="2" fill="{col}">{short}</text>
<g class="ar"><text x="{w - 18}" y="30" text-anchor="end" font-size="15" fill="{col}">↗</text></g>
<text x="19" y="58" font-family="{SANS}" font-size="18" font-weight="700" fill="{TXT}" class="in">{esc(title)}</text>
<g class="in" style="animation-delay:.2s">{desc_svg}</g>
<g class="in" style="animation-delay:.4s">{chip_svg}</g>
</svg>"""
    write_atomic(f"more-{slug}.svg", svg)


# --------------------------------------------------------------- paper card
def vis_vision():
    """Face-tracking viewfinder with gaze ray, landmarks and attention meter."""
    return f"""
<style>
  .look{{animation:lk 5s ease-in-out infinite}}
  @keyframes lk{{0%,40%{{transform:translateX(0)}}50%,65%{{transform:translateX(7px)}}75%,100%{{transform:translateX(0)}}}}
  .blinkeye{{transform-box:fill-box;transform-origin:center;animation:be 4s ease-in-out infinite}}
  @keyframes be{{0%,46%,54%,100%{{transform:scaleY(1)}}50%{{transform:scaleY(.1)}}}}
  .meter{{transform-box:fill-box;transform-origin:left;animation:mt 5s ease-in-out infinite}}
  @keyframes mt{{0%,40%{{transform:scaleX(.92)}}50%,65%{{transform:scaleX(.38)}}75%,100%{{transform:scaleX(.92)}}}}
  .st1{{animation:s1 5s steps(1) infinite}}.st2{{animation:s2 5s steps(1) infinite}}
  @keyframes s1{{0%{{opacity:1}}48%{{opacity:0}}70%{{opacity:1}}}}
  @keyframes s2{{0%{{opacity:0}}48%{{opacity:1}}70%{{opacity:0}}}}
  .scan{{animation:scn 3s ease-in-out infinite}}
  @keyframes scn{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(150px)}}}}
</style>
<path d="M14 30V14H30 M270 14H286V30 M286 164V180H270 M30 180H14V164" fill="none" stroke="{TEAL}" stroke-width="2"/>
<g opacity="0.9">
  <path d="M110 176 C110 140 190 140 190 176" fill="{DIM2}" fill-opacity="0.55"/>
  <ellipse cx="150" cy="96" rx="34" ry="42" fill="{PANEL2}" stroke="{DIM}" stroke-width="1.2"/>
  <g class="look">
    <g class="blinkeye"><ellipse cx="137" cy="90" rx="6" ry="4" fill="{TXT}"/><ellipse cx="163" cy="90" rx="6" ry="4" fill="{TXT}"/></g>
    <circle cx="137" cy="90" r="2.2" fill="{BG}"/><circle cx="163" cy="90" r="2.2" fill="{BG}"/>
  </g>
  <path d="M141 116 Q150 121 159 116" fill="none" stroke="{DIM}" stroke-width="1.4"/>
</g>
<g fill="{TEAL}">{''.join(f'<circle cx="{x}" cy="{y}" r="1.6" class="pulse" style="animation-delay:-{k * 0.2:.1f}s"/>' for k, (x, y) in enumerate([(131, 90), (143, 90), (157, 90), (169, 90), (150, 104), (141, 116), (159, 116), (150, 134), (122, 100), (178, 100)]))}</g>
<rect x="106" y="46" width="88" height="100" fill="none" stroke="{TEAL}" stroke-width="1.6" stroke-dasharray="6 4"/>
<rect x="106" y="34" width="88" height="12" fill="{TEAL}"/>
<text x="110" y="43.5" font-size="8.5" fill="{BG}" class="st1">FACE · ENGAGED</text>
<text x="110" y="43.5" font-size="8.5" fill="{BG}" class="st2">FACE · LOOK-AWAY</text>
<text x="208" y="70" font-size="8.5" letter-spacing="1.2" fill="{DIM}">ATTENTION</text>
<rect x="208" y="76" width="70" height="6" rx="3" fill="{LINE}"/>
<rect x="208" y="76" width="70" height="6" rx="3" fill="{TEAL}" class="meter"/>
<text x="208" y="102" font-size="8.5" letter-spacing="1.2" fill="{DIM}">GAZE</text>
<text x="208" y="116" font-size="10" fill="{TXT}" class="st1">on-screen</text>
<text x="208" y="116" font-size="10" fill="{GOLD}" class="st2">off-screen</text>
<text x="22" y="70" font-size="8.5" letter-spacing="1.2" fill="{DIM}">CAM 01</text>
<circle cx="26" cy="82" r="3.5" fill="{ROSE}" class="pulse"/><text x="34" y="85" font-size="9" fill="{TXT}">LIVE</text>
<g class="scan"><rect x="16" y="20" width="268" height="2" fill="{TEAL}" opacity="0.6" filter="url(#glow)"/></g>"""


def vis_eeg():
    """Scrolling multi-band brain waves + band power equalizer + focus gauge."""
    import math
    bands = [("δ", 2, 7, BLUE2), ("θ", 4, 6, BLUE), ("α", 6, 5, TEAL), ("β", 11, 4, GOLD)]
    W = 200
    waves = []
    for k, (name, cycles, amp, col) in enumerate(bands):
        y0 = 34 + k * 30
        period = W / cycles
        pts = []
        x = 0.0
        while x <= W + period + 0.1:
            noise = math.sin(x * 0.37 + k) * amp * 0.25
            pts.append(f"{x:.1f},{y0 + amp * math.sin(2 * math.pi * x / period) + noise * math.sin(2 * math.pi * x / period):.1f}")
            x += 2
        dur = 3 + k * 0.6
        waves.append(
            f'<text x="-14" y="{y0 + 4}" font-size="11" fill="{col}">{name}</text>'
            f'<g clip-path="url(#wc)"><g><polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="1.6" '
            f'stroke-linejoin="round"/><animateTransform attributeName="transform" type="translate" from="0 0" '
            f'to="-{period:.2f} 0" dur="{dur:.1f}s" repeatCount="indefinite"/></g></g>')
    eq = "".join(
        f'<rect x="{248 + j * 9}" y="40" width="6" height="60" rx="2" fill="{col}" fill-opacity="0.75" class="eq" '
        f'style="animation-delay:-{j * 0.31:.2f}s;animation-duration:{1.2 + j * 0.25:.2f}s"/>'
        for j, (_, _, _, col) in enumerate(bands))
    return f"""
<defs><clipPath id="wc"><rect x="0" y="14" width="200" height="130"/></clipPath></defs>
<style>
  .eq{{transform-box:fill-box;transform-origin:bottom;animation:eq 1.6s ease-in-out infinite}}
  @keyframes eq{{0%,100%{{transform:scaleY(.25)}}50%{{transform:scaleY(1)}}}}
  .needle{{transform-origin:150px 186px;animation:nd 4s ease-in-out infinite}}
  @keyframes nd{{0%,100%{{transform:rotate(-55deg)}}50%{{transform:rotate(40deg)}}}}
</style>
<g transform="translate(34 0)">{''.join(waves)}</g>
<line x1="34" y1="144" x2="234" y2="144" stroke="{LINE}"/>
<text x="246" y="30" font-size="8.5" letter-spacing="1.2" fill="{DIM}">POWER</text>
{eq}
<text x="246" y="116" font-size="8.5" fill="{DIM}">δ θ α β</text>
<path d="M110 186 A40 40 0 0 1 190 186" fill="none" stroke="{LINE}" stroke-width="6"/>
<path d="M110 186 A40 40 0 0 1 190 186" fill="none" stroke="url(#edgeG)" stroke-width="2.4"/>
<g class="needle"><line x1="150" y1="186" x2="150" y2="152" stroke="{TXT}" stroke-width="2" stroke-linecap="round"/></g>
<circle cx="150" cy="186" r="4" fill="{GOLD}"/>
<text x="196" y="184" font-size="8.5" letter-spacing="1.2" fill="{DIM}">FOCUS</text>
<text x="70" y="184" font-size="8.5" letter-spacing="1.2" fill="{DIM}">LOW</text>"""


def paper_card(i, slug, title, subtitle, url, doc, visual, keywords):
    w, h = 1000, 250
    tl = wrap(title, 36, 2, slug)
    sl = wrap(subtitle, 64, 2, slug)
    tx = 360
    ty = 108 if len(tl) == 1 else 100
    t_svg = "".join(
        f'<text x="{tx}" y="{ty + j * 32}" font-family="{SANS}" font-size="27" font-weight="700" fill="{TXT}" '
        f'class="in" style="animation-delay:{0.15 + j * 0.1:.2f}s">{esc(t)}</text>' for j, t in enumerate(tl))
    sy = ty + len(tl) * 32 - 6
    s_svg = "".join(
        f'<text x="{tx}" y="{sy + j * 19}" font-family="{SANS}" font-size="14" fill="{SOFT}" class="in" '
        f'style="animation-delay:{0.4 + j * 0.1:.2f}s">{esc(t)}</text>' for j, t in enumerate(sl))
    chip_svg, _ = chips(keywords, tx, max(190, sy + (len(sl) - 1) * 19 + 16), TEAL)
    vis = vis_vision() if visual == "vision" else vis_eeg()
    svg = f"""{head(w, h)}
{DEFS}
{card_frame(w, h, IEEE, 18, i * 1.3, trace_len=220)}
<style>
  .btn{{animation:bt 2.4s ease-in-out infinite}}
  @keyframes bt{{0%,100%{{fill-opacity:.12}}50%{{fill-opacity:.32}}}}
  .seal{{transform-box:fill-box;transform-origin:center;animation:sp 14s linear infinite}}
  @keyframes sp{{to{{transform:rotate(360deg)}}}}
</style>
<g transform="translate(28 28)">
  <rect width="300" height="194" rx="12" fill="{BG}" fill-opacity="0.7" stroke="{LINE}"/>
  {vis}
</g>
<rect x="{tx}" y="30" width="118" height="24" rx="5" fill="{IEEE}"/>
<text x="{tx + 59}" y="46.5" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="700" letter-spacing="1.5" fill="#fff">IEEE Xplore</text>
<circle cx="{tx + 136}" cy="42" r="3.5" fill="{TEAL}"/><circle cx="{tx + 136}" cy="42" r="3.5" fill="none" stroke="{TEAL}" class="ring"/>
<text x="{tx + 146}" y="46" font-size="11" letter-spacing="2" fill="{TEAL}">PUBLISHED · PEER-REVIEWED</text>
<text x="{w - 32}" y="46" text-anchor="end" font-size="11" letter-spacing="2" fill="{DIM}">PAPER {i + 1:02d}</text>
<line x1="{tx}" y1="66" x2="{w - 32}" y2="66" stroke="{LINE}"/>
{t_svg}
{s_svg}
<g class="in" style="animation-delay:.6s">{chip_svg}</g>
<g transform="translate({w - 92} 92)">
  <circle class="seal" r="34" fill="none" stroke="{GOLD}" stroke-opacity="0.7" stroke-dasharray="3 5"/>
  <circle r="26" fill="{GOLD}" fill-opacity="0.08" stroke="{GOLD}" stroke-opacity="0.5"/>
  <text y="-2" text-anchor="middle" font-size="9" letter-spacing="1.5" fill="{GOLD}">IEEE</text>
  <text y="11" text-anchor="middle" font-size="8" letter-spacing="1" fill="{DIM}">INDEXED</text>
</g>
<rect class="btn" x="{w - 182}" y="190" width="150" height="34" rx="17" fill="{IEEE}" stroke="{IEEE}" stroke-width="1.4"/>
<rect x="{w - 182}" y="190" width="150" height="34" rx="17" fill="none" stroke="#4aa3df" stroke-opacity="0.8"/>
<g class="ar"><text x="{w - 107}" y="211.5" text-anchor="middle" font-size="12" font-weight="700" letter-spacing="1.8" fill="{TXT}">READ PAPER ↗</text></g>
<text x="{w - 107}" y="178" text-anchor="middle" font-size="10" letter-spacing="1.5" fill="{DIM}">DOC · {doc}</text>
</svg>"""
    write_atomic(f"paper-{slug}.svg", svg)


# ------------------------------------------------------------------- strips
def strip(key, label, sub, count, color, glyph, noun="BUILDS"):
    w, h = 1000, 64
    svg = f"""{head(w, h)}
{DEFS}
<style>
  .mv{{animation:mv 4.5s ease-in-out infinite}}
  @keyframes mv{{0%{{transform:translateX(0)}}50%{{transform:translateX({w - 320}px)}}100%{{transform:translateX(0)}}}}
  .gl{{transform-box:fill-box;transform-origin:center;animation:gl 3s ease-in-out infinite}}
  @keyframes gl{{0%,100%{{transform:rotate(0) scale(1)}}50%{{transform:rotate(180deg) scale(1.1)}}}}
  .tick{{animation:tk 1.2s steps(1) infinite}}@keyframes tk{{50%{{opacity:0}}}}
</style>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="url(#panelG)"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="url(#grid)" opacity="0.4"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="none" stroke="{color}" stroke-opacity="0.45"/>
<rect x="16" y="14" width="36" height="36" rx="9" fill="{color}" fill-opacity="0.14" stroke="{color}"/>
<text x="34" y="39" text-anchor="middle" font-size="19" fill="{color}" class="gl">{glyph}</text>
<text x="68" y="31" font-family="{SANS}" font-size="17" font-weight="700" letter-spacing="1.5" fill="{TXT}">{esc(label)}</text>
<text x="68" y="49" font-size="11" letter-spacing="1.5" fill="{DIM}">// {esc(sub)}<tspan fill="{color}" class="tick"> _</tspan></text>
<text x="{w - 24}" y="38" text-anchor="end" font-size="12" letter-spacing="2.4" fill="{color}">{count:02d} {noun}</text>
<rect x="300" y="58" width="{w - 320}" height="1" fill="{LINE}"/>
<g class="mv"><rect x="300" y="57" width="60" height="3" rx="1.5" fill="{color}" filter="url(#glow)"/></g>
</svg>"""
    write_atomic(f"strip-{key}.svg", svg)


def teaser(count):
    w, h = 1000, 120
    stack = "".join(
        f'<rect x="{40 + k * 14}" y="{30 + k * 8}" width="120" height="66" rx="9" fill="{PANEL2}" stroke="{col}" '
        f'stroke-opacity="0.8" class="fan" style="animation-delay:{k * 0.15:.2f}s"/>'
        for k, col in enumerate([BLUE, TEAL, GOLD]))
    stack += (f'<g class="fan" style="animation-delay:.3s"><rect x="80" y="58" width="60" height="6" rx="3" fill="{TXT}" fill-opacity=".8"/>'
              f'<rect x="80" y="72" width="88" height="4" rx="2" fill="{DIM}"/><rect x="80" y="81" width="70" height="4" rx="2" fill="{DIM}"/>'
              f'<circle cx="182" cy="62" r="4" fill="{GOLD}" class="dot"/></g>')
    svg = f"""{head(w, h)}
{DEFS}
<defs>
  <linearGradient id="tG" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="{TEAL}"/><stop offset="1" stop-color="{GOLD}"/>
  </linearGradient>
</defs>
<style>
  .fan{{animation:fan 3.2s ease-in-out infinite}}
  @keyframes fan{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(10px,-8px)}}}}
  .bob{{animation:bob 1.4s ease-in-out infinite}}
  @keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(5px)}}}}
  .dot{{animation:pl 1.2s ease-in-out infinite}}@keyframes pl{{0%,100%{{opacity:.2}}50%{{opacity:1}}}}
</style>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="url(#panelG)"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="url(#grid)" opacity="0.45"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="none" stroke="url(#edgeG)" stroke-opacity="0.7" stroke-width="1.4"/>
{stack}
<text x="250" y="58" font-family="{SANS}" font-size="34" font-weight="800" fill="url(#tG)">+{count} MORE BUILDS</text>
<text x="252" y="86" font-size="12" letter-spacing="2" fill="{DIM}">AI &amp; AGENTS · DATA SCIENCE · SOFTWARE &amp; VISION · all public on GitHub</text>
<g class="bob"><text x="{w - 40}" y="58" text-anchor="end" font-size="12" letter-spacing="2.4" fill="{TEAL}">CLICK  ▸ MORE_BUILDS  BELOW</text>
<text x="{w - 40}" y="84" text-anchor="end" font-size="18" fill="{TEAL}">▼</text></g>
{''.join(f'<circle cx="{w - 88 + k * 12}" cy="79" r="2.5" fill="{TEAL}" class="dot" style="animation-delay:{k * 0.2:.1f}s"/>' for k in range(3))}
</svg>"""
    write_atomic("more-teaser.svg", svg)


if __name__ == "__main__":
    for i, p in enumerate(FEATURED):
        featured_card(i, len(FEATURED), *p)
    for i, p in enumerate(MORE):
        more_card(i, *p)
    for i, p in enumerate(PAPERS):
        paper_card(i, *p)
    for cat, c in CATS.items():
        nf = sum(1 for p in FEATURED if p[3] == cat)
        nm = sum(1 for p in MORE if p[3] == cat)
        strip(f"feat-{cat}", c["label"], c["sub"], nf, c["color"], c["glyph"])
        strip(f"more-{cat}", c["label"], c["sub"], nm, c["color"], c["glyph"])
    strip("ieee", "IEEE PUBLICATIONS", "peer-reviewed research · indexed in IEEE Xplore", len(PAPERS), "#4aa3df", "✦", "PAPERS")
    teaser(len(MORE))
