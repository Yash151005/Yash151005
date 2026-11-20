"""
YASH.PAKALE // NEURAL.OS — shared design tokens + SVG helpers.

Used by both tools/build_assets.py (static art) and
tools/render_telemetry.py (daily data-driven art), so every SVG in assets/
shares one palette and one set of filters.

Design rule: every image the README shows lives in assets/ and is served by
GitHub itself, so the profile never shows "Something went wrong".
"""
import os
import xml.dom.minidom

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")

# ------------------------------------------------------------------ palette
# "Aurora" theme: deep navy, electric blue, teal, with a gold accent.
BG, PANEL, PANEL2, LINE = "#050a18", "#0a1328", "#0e1a35", "#1d2b4f"
BLUE, BLUE2, TEAL, GOLD, ROSE = "#3b82f6", "#1f6feb", "#2dd4bf", "#fbbf24", "#fb7185"
TXT, DIM, DIM2 = "#e8eefc", "#8b9bc2", "#4b5a80"
# sequential ramp (one hue, empty -> busy) for the contribution grid
LEVELS = ["#111c36", "#0f3b5f", "#0e6a8a", "#14a3b8", "#5eead4"]

MONO = "'JetBrains Mono','Cascadia Code',Consolas,'Courier New',monospace"
SANS = "'Segoe UI',Inter,'Helvetica Neue',Arial,sans-serif"


def head(w, h, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{MONO}" {extra}>')


DEFS = f"""
<defs>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="2.4" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="40"/>
  </filter>
  <linearGradient id="panelG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{PANEL2}"/><stop offset="1" stop-color="{BG}"/>
  </linearGradient>
  <linearGradient id="edgeG" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{BLUE2}"/><stop offset=".55" stop-color="{TEAL}"/><stop offset="1" stop-color="{GOLD}"/>
  </linearGradient>
  <linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{TEAL}" stop-opacity="0"/>
    <stop offset="1" stop-color="{TEAL}" stop-opacity="0.45"/>
  </linearGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="{LINE}" stroke-width="0.6" opacity="0.55"/>
  </pattern>
</defs>"""


def panel(w, h, title, right=""):
    """Rounded panel with gradient edge, faint grid and a header row."""
    return f"""
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="url(#panelG)"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="url(#grid)" opacity="0.5"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="none" stroke="url(#edgeG)" stroke-opacity="0.75" stroke-width="1.4"/>
<circle cx="30" cy="34" r="4" fill="{ROSE}"/><circle cx="44" cy="34" r="4" fill="{GOLD}"/><circle cx="58" cy="34" r="4" fill="{TEAL}"/>
<text x="76" y="38.5" font-size="13" letter-spacing="2.5" fill="{TXT}">{title}</text>
<text x="{w - 28}" y="38.5" text-anchor="end" font-size="10" letter-spacing="1.8" fill="{DIM}">{right}</text>
<line x1="22" y1="54" x2="{w - 22}" y2="54" stroke="{LINE}"/>"""


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def write_atomic(name, svg):
    """Render to .tmp, XML-validate, then swap in. A bad render never goes live."""
    os.makedirs(OUT, exist_ok=True)
    final = os.path.join(OUT, name)
    tmp = final + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + svg.strip() + "\n")
    xml.dom.minidom.parse(tmp)
    os.replace(tmp, final)
    print(f"rendered assets/{name} ({os.path.getsize(final) / 1024:.1f} KB)")
