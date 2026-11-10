"""Liquid-glass design kit for the profile README.

Every asset is a self-contained animated SVG (SMIL, no scripts, no web fonts,
no heavy blur filters) so it plays inside a GitHub README through <img>.

    python scripts/glass.py        # writes everything into ../assets
"""
import math
import os

FONT = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', 'Segoe UI', Inter, Roboto, Arial, sans-serif"
W = 1200

VIOLET, CYAN, PINK, AMBER, BLUE, MINT = "#8b5cf6", "#22d3ee", "#ff5fa2", "#ffb347", "#3b82f6", "#34d399"

STOPS = [
    ("MOVE", "autonomous-bot", "a robot that maps and navigates", AMBER),
    ("SEE", "sentinel", "vision that finds people in the dark", PINK),
    ("KNOW", "finintel", "AI that cites its sources", CYAN),
    ("ACT", "nexus", "an agent that fixes incidents", VIOLET),
    ("SHIP", "dishdecoded", "a product people can use", MINT),
]

PROJECTS = {
    "autonomous-bot": ("A ROS 2 robot that maps, localises and navigates on its own, with an IoT dashboard and a swarm auction.", ["ROS 2", "Nav2", "SLAM", "MQTT"]),
    "sentinel": ("Search-and-rescue vision: YOLO11 on RGB and simulated thermal feeds to find people in the dark.", ["YOLO11", "OpenCV", "ONNX"]),
    "finintel": ("A financial RAG system that writes grounded, citation-backed reports from filings.", ["RAG", "GraphRAG", "Claude", "64 tests"]),
    "nexus": ("Network intelligence and an autonomous DevSecOps agent that finds the root cause and fixes the incident.", ["FastAPI", "PostgreSQL", "React", "Claude / NIM"]),
    "dishdecoded": ("Snap a dish or a menu and get its story, allergens and a recipe.", ["Next.js 15", "React 19", "Claude vision"]),
}

TOOLKIT = {
    "Robotics": (AMBER, ["ROS 2", "Nav2", "SLAM", "Sensor fusion (ESKF)", "RPLIDAR", "Arduino"]),
    "Vision": (PINK, ["YOLO11", "OpenCV", "PyTorch", "RGB-thermal fusion", "Jetson", "ONNX"]),
    "AI": (CYAN, ["Claude API", "NVIDIA NIM", "RAG + GraphRAG", "Agent tool use", "Anomaly detection", "Random Forest"]),
    "Systems": (VIOLET, ["FastAPI", "PostgreSQL", "Redis", "React", "Docker", "C (ASan clean)"]),
}

_n = [0]


def uid(p="i"):
    _n[0] += 1
    return f"{p}{_n[0]}"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


# ------------------------------------------------------------------ stage
def blob(cx, cy, r, color, dur, dx, dy, op=0.9):
    g = uid("g")
    return (f'<radialGradient id="{g}"><stop offset="0" stop-color="{color}" stop-opacity="{op}"/>'
            f'<stop offset="0.55" stop-color="{color}" stop-opacity="{op*0.35:.2f}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>',
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{g})"><animateTransform attributeName="transform" type="translate" '
            f'values="0 0;{dx} {dy};{-dx*0.6:.0f} {dy*0.5:.0f};0 0" dur="{dur}s" repeatCount="indefinite" calcMode="spline" '
            f'keySplines=".4 0 .6 1;.4 0 .6 1;.4 0 .6 1"/></circle>')


def stage(w, h, body, label, blobs, sharp="", r=28, extra_defs=""):
    """Dark aurora card. #bgsoft = light only, #bg = light + sharp details."""
    defs, circles = "", ""
    for b in blobs:
        d, c = blob(*b)
        defs += d
        circles += c
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(label)}" font-family="{FONT}">'
        f'<defs>{defs}'
        f'<linearGradient id="base" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060714"/><stop offset="0.5" stop-color="#0a0d26"/><stop offset="1" stop-color="#130a26"/></linearGradient>'
        f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.85"/><stop offset="0.3" stop-color="#fff" stop-opacity="0.18"/><stop offset="0.65" stop-color="#fff" stop-opacity="0.06"/><stop offset="1" stop-color="#fff" stop-opacity="0.45"/></linearGradient>'
        f'<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.20"/><stop offset="0.45" stop-color="#fff" stop-opacity="0.07"/><stop offset="1" stop-color="#fff" stop-opacity="0.03"/></linearGradient>'
        f'<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.20"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<radialGradient id="spec"><stop offset="0" stop-color="#fff" stop-opacity="0.42"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="ink" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset="0.5" stop-color="#dbe7ff"/><stop offset="1" stop-color="#ffffff"/></linearGradient>'
        f'<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>'
        f'<clipPath id="card"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>'
        f'<g id="bgsoft"><rect width="{w}" height="{h}" fill="url(#base)"/>{circles}</g>'
        f'<g id="sharp">{sharp}</g>'
        f'{extra_defs}</defs>'
        f'<g clip-path="url(#card)"><use xlink:href="#bgsoft" href="#bgsoft"/><use xlink:href="#sharp" href="#sharp"/>{body}</g>'
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="#fff" stroke-opacity="0.10"/>'
        f'</svg>')


def glass(x, y, w, h, r, inner="", sweep=None, tint=None, lens=True, shadow=True, frost_sharp=False):
    """A pane of liquid glass: refracted backdrop, sheen, specular, rim light."""
    c = uid("c")
    cx, cy = x + w / 2, y + h / 2
    o = f'<clipPath id="{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>'
    if shadow:
        for i, a in enumerate((0.10, 0.08, 0.06)):
            o += f'<rect x="{x-2-i*3}" y="{y+6+i*5}" width="{w+4+i*6}" height="{h+2+i*2}" rx="{r+i*3}" fill="#02030a" opacity="{a}"/>'
    o += f'<g clip-path="url(#{c})">'
    if lens:  # backdrop seen through the glass: magnified, so light bends at the rim
        o += f'<g transform="translate({cx:.1f} {cy:.1f}) scale(1.22) translate({-cx:.1f} {-cy:.1f})"><use xlink:href="#bgsoft" href="#bgsoft"/>'
        if frost_sharp:
            o += '<use xlink:href="#sharp" href="#sharp" filter="url(#soft)" opacity="0.8"/>'
        o += '</g>'
    o += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#sheen)"/>'
    if tint:
        o += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{tint}" opacity="0.14"/>'
    o += f'<ellipse cx="{x+w*0.22:.1f}" cy="{y}" rx="{w*0.45:.1f}" ry="{min(h*0.55, 120):.1f}" fill="url(#spec)" opacity="0.55"/>'
    if sweep is not None:
        bw = max(w * 0.3, 60)
        o += (f'<rect x="{x-bw}" y="{y-10}" width="{bw:.0f}" height="{h+20}" fill="url(#sweep)" transform="skewX(-18)" style="transform-origin:{cx:.0f}px {cy:.0f}px">'
              f'<animate attributeName="x" values="{x-bw-40:.0f};{x-bw-40:.0f};{x+w+60:.0f};{x+w+60:.0f}" keyTimes="0;{0.05+sweep:.2f};{0.3+sweep:.2f};1" dur="9s" repeatCount="indefinite"/></rect>')
    o += inner + '</g>'
    o += f'<rect x="{x+0.75}" y="{y+0.75}" width="{w-1.5}" height="{h-1.5}" rx="{r}" fill="none" stroke="url(#edge)" stroke-width="1.5"/>'
    o += f'<rect x="{x+3}" y="{y+3}" width="{w-6}" height="{h-6}" rx="{max(r-3,1)}" fill="none" stroke="#fff" stroke-opacity="0.07"/>'
    return o


def bead(cx, cy, r, color, glyph="", pulse=None):
    """A liquid drop of coloured glass with a glyph inside."""
    g = uid("b")
    o = (f'<radialGradient id="{g}" cx="0.35" cy="0.28" r="0.9"><stop offset="0" stop-color="#fff" stop-opacity="0.95"/><stop offset="0.18" stop-color="{color}" stop-opacity="0.95"/>'
         f'<stop offset="0.75" stop-color="{color}" stop-opacity="0.55"/><stop offset="1" stop-color="#0a0d26" stop-opacity="0.55"/></radialGradient>')
    o += f'<circle cx="{cx}" cy="{cy}" r="{r*1.45:.1f}" fill="{color}" opacity="0.16">'
    if pulse is not None:
        o += f'<animate attributeName="opacity" values="0.10;0.34;0.10" dur="5s" begin="{pulse}s" repeatCount="indefinite"/>'
    o += '</circle>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{g})"/>'
    o += f'<ellipse cx="{cx-r*0.25:.1f}" cy="{cy-r*0.48:.1f}" rx="{r*0.52:.1f}" ry="{r*0.26:.1f}" fill="#fff" opacity="0.38"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r-0.75}" fill="none" stroke="url(#edge)" stroke-width="1.5"/>'
    if glyph:
        o += f'<g transform="translate({cx} {cy}) scale({r/26:.2f})" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>'
    return o


GLYPH = {
    "MOVE": '<path d="M0 -13 L10 11 L0 5 L-10 11 Z" fill="#fff" fill-opacity="0.9"/>',
    "SEE": '<path d="M-14 0 Q0 -12 14 0 Q0 12 -14 0 Z"/><circle r="4" fill="#fff"/>',
    "KNOW": '<path d="M-9 8 L0 -9 L9 8"/><circle cx="-9" cy="8" r="3.4" fill="#fff"/><circle cx="0" cy="-9" r="3.4" fill="#fff"/><circle cx="9" cy="8" r="3.4" fill="#fff"/><path d="M-9 8 L9 8"/>',
    "ACT": '<path d="M3 -14 L-8 2 L0 2 L-3 14 L8 -2 L0 -2 Z" fill="#fff" fill-opacity="0.9"/>',
    "SHIP": '<path d="M-13 -1 L13 -11 L5 12 L-1 3 Z" fill="#fff" fill-opacity="0.9"/><path d="M-1 3 L13 -11"/>',
}


def text(x, y, s, size, weight=500, fill="#fff", op=1.0, anchor="start", ls=0, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" fill-opacity="{op}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{esc(s)}</text>')


def wrap(s, n):
    out, cur = [], ""
    for wd in s.split():
        if len(cur) + len(wd) + 1 > n and cur:
            out.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    return out + [cur]


def rays(x, y, n=5, length=900, spread=46, start=18):
    """Shafts of light falling from a point."""
    g = uid("r")
    o = (f'<linearGradient id="{g}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0.30"/>'
         f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    for i in range(n):
        a = start + i * spread / max(n - 1, 1)
        wdt = 26 + (i * 37) % 50
        o += (f'<polygon points="0,0 {length},{-wdt} {length},{wdt}" fill="url(#{g})" transform="translate({x} {y}) rotate({a:.1f})" opacity="0.25">'
              f'<animate attributeName="opacity" values="0.10;0.42;0.10" dur="{6+i*1.7:.1f}s" begin="{i*0.9:.1f}s" repeatCount="indefinite"/></polygon>')
    return o


def stars(w, h, n, seed=7):
    o, s = "", seed
    for i in range(n):
        s = (s * 1103515245 + 12345) % 2147483648
        x = s % w
        s = (s * 1103515245 + 12345) % 2147483648
        y = s % h
        r = 0.7 + (s % 10) / 9
        o += (f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="#fff" opacity="0.5"><animate attributeName="opacity" values="0.15;0.9;0.15" '
              f'dur="{3+(s%40)/10:.1f}s" begin="{(s%30)/10:.1f}s" repeatCount="indefinite"/></circle>')
    return o


# ------------------------------------------------------------------ hero
def hero():
    h = 620
    blobs = [(180, 120, 420, VIOLET, 26, 90, 60), (1040, 160, 380, CYAN, 31, -110, 70, 0.75),
             (860, 560, 420, PINK, 29, -80, -70, 0.8), (240, 600, 340, BLUE, 34, 100, -50), (620, 300, 260, AMBER, 23, 60, 40, 0.45)]
    sharp = rays(-40, -60) + stars(W, h, 46)
    # orbits with travelling light
    for i, (rx, ry, rot, dur, col) in enumerate([(520, 210, -12, 22, CYAN), (430, 150, 14, 17, PINK), (600, 260, 4, 30, "#fff")]):
        p = f"M{600-rx} 300 a{rx} {ry} 0 1 0 {2*rx} 0 a{rx} {ry} 0 1 0 {-2*rx} 0"
        sharp += (f'<g transform="rotate({rot} 600 300)"><path d="{p}" fill="none" stroke="#fff" stroke-opacity="0.16" stroke-width="1"/>'
                  f'<circle r="9" fill="{col}" opacity="0.35"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{p}"/></circle>'
                  f'<circle r="3.2" fill="#fff"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{p}"/></circle></g>')
    b = ""
    # menu bar
    mb = bead(74, 54, 9, "#ff5f57") + bead(100, 54, 9, "#febc2e") + bead(126, 54, 9, "#28c840")
    mb += text(160, 59, "aryankhanna1409", 15, 600, op=0.95)
    for i, t in enumerate(["Story", "Projects", "Toolkit", "Contact"]):
        mb += text(360 + i * 96, 59, t, 14, 500, op=0.7)
    mb += text(1128, 59, "Pune, IN  ·  B.Tech Robotics ’27", 14, 500, op=0.8, anchor="end")
    b += glass(40, 28, 1120, 52, 26, mb, sweep=0.45, frost_sharp=True)
    # floating drops
    for (cx, cy, r, col, dur, dy) in [(118, 300, 44, CYAN, 9, -22), (1092, 250, 56, PINK, 11, 26), (1040, 420, 22, AMBER, 7, -16), (176, 430, 18, VIOLET, 8, 14)]:
        b += (f'<g>{bead(cx, cy, r, col)}<animateTransform attributeName="transform" type="translate" values="0 0;0 {dy};0 0" dur="{dur}s" '
              f'repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1"/></g>')
    # main pane
    x, y, pw, ph = 190, 122, 820, 300
    inner = text(600, y + 62, "ROBOTICS  ·  AI  ·  SOFTWARE", 15, 600, op=0.72, anchor="middle", ls=5)
    inner += (f'<text x="600" y="{y+158}" font-size="96" font-weight="700" text-anchor="middle" letter-spacing="-3" fill="#000" fill-opacity="0.25">Aryan Khanna</text>'
              f'<text x="600" y="{y+154}" font-size="96" font-weight="700" text-anchor="middle" letter-spacing="-3" fill="url(#name)">Aryan Khanna</text>')
    inner += text(600, y + 204, "I build machines that move, see, know, act and ship.", 21, 400, op=0.86, anchor="middle")
    chips = ["Pune, IN", "B.Tech Robotics, class of 2027", "Published, IJCIS 2025"]
    widths = [len(c) * 8.2 + 36 for c in chips]
    cx0 = 600 - (sum(widths) + 14 * 2) / 2
    for c, cw in zip(chips, widths):
        inner += (f'<rect x="{cx0:.0f}" y="{y+232}" width="{cw:.0f}" height="34" rx="17" fill="#fff" fill-opacity="0.10" stroke="#fff" stroke-opacity="0.30"/>'
                  + text(cx0 + cw / 2, y + 254, c, 14, 500, op=0.92, anchor="middle"))
        cx0 += cw + 14
    b += glass(x, y, pw, ph, 46, inner, sweep=0.0, frost_sharp=True)
    # dock
    dx, dy, dw, dh = 330, 462, 540, 118
    dock = ""
    for i, (verb, repo, line, col) in enumerate(STOPS):
        cx = dx + 70 + i * 100
        t = i * 0.16
        dock += (f'<g>{bead(cx, dy+50, 30, col, GLYPH[verb], pulse=i)}'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -12;0 0;0 0" keyTimes="0;{t:.2f};{t+0.08:.2f};{t+0.16:.2f};1" dur="6s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;.2 .8 .3 1;.5 0 .7 .4;0 0 1 1"/></g>'
                 + text(cx, dy + 104, verb, 12, 700, op=0.85, anchor="middle", ls=2.5))
    b += glass(dx, dy, dw, dh, 36, dock, sweep=0.25, frost_sharp=True)
    extra = ('<linearGradient id="name" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">'
             '<stop offset="0" stop-color="#fff"/><stop offset="0.35" stop-color="#fff"/><stop offset="0.5" stop-color="#9be8ff"/><stop offset="0.65" stop-color="#fff"/><stop offset="1" stop-color="#fff"/>'
             '<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="5s" repeatCount="indefinite"/></linearGradient>')
    return stage(W, h, b, "Aryan Khanna: robotics, AI and software. I build machines that move, see, know, act and ship.", blobs, sharp, extra_defs=extra)


# ------------------------------------------------------------------ story
def story():
    h = 400
    blobs = [(120, 80, 320, AMBER, 27, 60, 40, 0.6), (420, 380, 300, PINK, 31, 50, -40, 0.65), (640, 60, 300, CYAN, 25, -50, 40, 0.6),
             (880, 400, 320, VIOLET, 33, -60, -30, 0.8), (1120, 100, 300, MINT, 29, -50, 50, 0.55)]
    n, tw, th, top = 5, 196, 236, 62
    gap = (W - 80 - n * tw) / (n - 1)
    xs = [40 + i * (tw + gap) for i in range(n)]
    mid = top + th / 2
    # the current that runs through every stop and loops back underneath
    path = f"M{xs[0]+tw/2} {mid} L{xs[-1]+tw/2} {mid} Q{W-6} {mid} {W-22} {top+th+40} Q{W-40} {h-28} {W-120} {h-28} L120 {h-28} Q40 {h-28} 22 {top+th+40} Q6 {mid} {xs[0]+tw/2} {mid}"
    sharp = stars(W, h, 24, 11)
    sharp += (f'<path d="{path}" fill="none" stroke="url(#flow)" stroke-width="2.5" stroke-opacity="0.9"/>'
              f'<path d="{path}" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="2 26" opacity="0.8">'
              f'<animate attributeName="stroke-dashoffset" values="0;-280" dur="6s" repeatCount="indefinite"/></path>')
    for k in range(2):
        sharp += (f'<circle r="16" fill="#fff" opacity="0.22"><animateMotion dur="12s" begin="{-6*k}s" repeatCount="indefinite" path="{path}"/></circle>'
                  f'<circle r="5" fill="#fff"><animateMotion dur="12s" begin="{-6*k}s" repeatCount="indefinite" path="{path}"/></circle>')
    b = text(600, h - 46, "what each stop learns feeds the next", 13, 600, op=0.8, anchor="middle", ls=3)
    for i, (verb, repo, line, col) in enumerate(STOPS):
        x = xs[i]
        cx = x + tw / 2
        inner = bead(cx, top + 66, 30, col, GLYPH[verb], pulse=i)
        inner += text(x + 20, top + 30, f"0{i+1}", 13, 700, op=0.6, ls=1)
        inner += text(cx, top + 142, verb, 30, 700, anchor="middle", ls=3)
        inner += text(cx, top + 167, repo, 15, 600, fill=col, anchor="middle", extra='style="filter:brightness(1.5)"')
        for j, ln in enumerate(wrap(line, 22)):
            inner += text(cx, top + 194 + j * 19, ln, 15, 400, op=0.85, anchor="middle")
        g = (f'<g>{glass(x, top, tw, th, 30, inner, sweep=i*0.12, tint=col, frost_sharp=True)}'
             f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -7;0 0" dur="7s" begin="{-i*1.4}s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1"/></g>')
        b += g
    stops = "".join(f'<stop offset="{i/4}" stop-color="{s[3]}"/>' for i, s in enumerate(STOPS))
    extra = f'<linearGradient id="flow" gradientUnits="userSpaceOnUse" x1="40" y1="0" x2="{W-40}" y2="0">{stops}</linearGradient>'
    return stage(W, h, b, "The loop: move (autonomous-bot), see (sentinel), know (finintel), act (nexus), ship (dishdecoded). What each stop learns feeds the next.", blobs, sharp, extra_defs=extra)


# ------------------------------------------------------------------ section header
def section(num, title, sub, c1, c2):
    h = 96
    blobs = [(120, 20, 240, c1, 21, 80, 10, 0.8), (700, 110, 260, c2, 27, -90, -10, 0.55), (1150, 10, 220, c1, 24, -60, 20, 0.5)]
    sharp = (f'<line x1="330" y1="48" x2="1160" y2="48" stroke="#fff" stroke-opacity="0.18"/>'
             f'<rect x="330" y="46.5" width="120" height="3" rx="1.5" fill="url(#sweep)"><animate attributeName="x" values="330;1040;330" dur="9s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1"/></rect>')
    b = text(1160, 38, sub, 13, 500, op=0.7, anchor="end", ls=1.5)
    inner = bead(64, 48, 17, c1) + text(64, 53, num, 13, 800, anchor="middle") + text(96, 58, title, 28, 700, ls=-0.5)
    b += glass(24, 18, 280, 60, 30, inner, sweep=0.1)
    return stage(W, h, b, f"{num} {title}", blobs, sharp, r=24)


# ------------------------------------------------------------------ project cards
def project(i, w=600, h=420):
    verb, repo, line, col = STOPS[i]
    tag, chips = PROJECTS[repo]
    other = STOPS[(i + 2) % 5][3]
    blobs = [(80, 60, 300, col, 24, 60, 40, 0.8), (w - 60, h - 40, 300, other, 29, -60, -40, 0.6), (w * 0.6, 40, 200, BLUE, 33, -40, 30, 0.5)]
    sharp = stars(w, h, 14, 3 + i) + rays(-30, -40, n=3, length=700, spread=30, start=24)
    m = 26
    inner = bead(m + 62, m + 66, 36, col, GLYPH[verb], pulse=0)
    inner += text(m + 116, m + 56, f"0{i+1}  ·  {verb}", 15, 700, op=0.75, ls=3)
    inner += text(m + 114, m + 96, repo, 38, 700, ls=-1)
    y = m + 148
    for ln in wrap(tag, 46):
        inner += text(m + 30, y, ln, 19, 400, op=0.88)
        y += 28
    cx = m + 30
    cy = h - m - 62
    for c in chips:
        cw = len(c) * 8.4 + 30
        inner += (f'<rect x="{cx:.0f}" y="{cy}" width="{cw:.0f}" height="32" rx="16" fill="#fff" fill-opacity="0.10" stroke="#fff" stroke-opacity="0.30"/>'
                  + text(cx + cw / 2, cy + 21, c, 14, 500, op=0.92, anchor="middle"))
        cx += cw + 10
    inner += (f'<g transform="translate({w-m-58} {m+52})"><circle r="20" fill="#fff" fill-opacity="0.12" stroke="#fff" stroke-opacity="0.4"/>'
              f'<path d="M-6 6 L6 -6 M-3 -6 L6 -6 L6 3" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
              f'<animateTransform attributeName="transform" type="translate" values="0 0;2 -2;0 0" dur="2.4s" repeatCount="indefinite"/></path></g>')
    b = glass(m, m, w - 2 * m, h - 2 * m, 34, inner, sweep=0.1, frost_sharp=True)
    return stage(w, h, b, f"0{i+1} {verb}: {repo}. {tag}", blobs, sharp, r=26)


def bot_scene(w=600, h=420):
    """Stands in for a demo recording of autonomous-bot: a lidar sweep building a map."""
    blobs = [(120, 340, 320, AMBER, 26, 50, -40, 0.55), (520, 60, 300, BLUE, 30, -50, 40, 0.7), (320, 220, 220, VIOLET, 22, 30, 30, 0.4)]
    m = 26
    cx, cy = w / 2, h / 2 + 6
    grid = "".join(f'<line x1="{x}" y1="{m}" x2="{x}" y2="{h-m}" stroke="#fff" stroke-opacity="0.06"/>' for x in range(m + 40, w - m, 40))
    grid += "".join(f'<line x1="{m}" y1="{y}" x2="{w-m}" y2="{y}" stroke="#fff" stroke-opacity="0.06"/>' for y in range(m + 40, h - m, 40))
    walls = [(90, 90, 250, 90), (250, 90, 250, 130), (330, 80, 500, 80), (500, 80, 500, 200), (90, 90, 90, 300), (90, 300, 200, 300), (200, 300, 200, 340),
             (280, 340, 510, 340), (510, 260, 510, 340), (400, 180, 440, 180), (400, 180, 400, 215)]
    inner = grid
    for k, (x1, y1, x2, y2) in enumerate(walls):
        ang = (math.degrees(math.atan2((y1 + y2) / 2 - cy, (x1 + x2) / 2 - cx)) + 360) % 360
        t = ang / 360
        inner += (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity="0.25">'
                  f'<animate attributeName="opacity" values="0.25;0.25;1;0.25" keyTimes="0;{max(t-0.01,0):.3f};{min(t+0.02,0.99):.3f};1" dur="5s" repeatCount="indefinite"/></line>')
    inner += (f'<g><path d="M{cx} {cy} L{cx+260} {cy-46} A264 264 0 0 1 {cx+260} {cy+46} Z" fill="url(#beam)"/>'
              f'<animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};360 {cx} {cy}" dur="5s" repeatCount="indefinite"/></g>')
    for rr in (60, 120, 180):
        inner += f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="#fff" stroke-opacity="0.10" stroke-dasharray="3 7"/>'
    inner += f'<path d="M{cx} {cy} C{cx+60} {cy+70} {cx+120} {cy+20} {cx+150} {cy-60}" fill="none" stroke="{AMBER}" stroke-width="2.5" stroke-dasharray="6 8" stroke-linecap="round"><animate attributeName="stroke-dashoffset" values="0;-56" dur="2s" repeatCount="indefinite"/></path>'
    inner += bead(cx + 150, cy - 60, 9, MINT, pulse=0)
    inner += bead(cx, cy, 20, AMBER, GLYPH["MOVE"], pulse=0)
    inner += text(m + 26, m + 38, "LIDAR  ·  SLAM  ·  NAV2", 13, 700, op=0.8, ls=3)
    inner += text(w - m - 26, h - m - 22, "illustration, no demo recording yet", 12, 500, op=0.65, anchor="end")
    extra = (f'<linearGradient id="beam" gradientUnits="userSpaceOnUse" x1="{cx}" y1="{cy}" x2="{cx+264}" y2="{cy}"><stop offset="0" stop-color="{AMBER}" stop-opacity="0.55"/>'
             f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>')
    b = glass(m, m, w - 2 * m, h - 2 * m, 34, inner)
    return stage(w, h, b, "autonomous-bot: an illustration of a lidar sweep building a map (no demo recording yet)", blobs, "", r=26, extra_defs=extra)


# ------------------------------------------------------------------ toolkit
def toolkit():
    h = 430
    blobs = [(140, 90, 320, AMBER, 28, 50, 40, 0.55), (460, 400, 320, PINK, 32, 40, -50, 0.6), (760, 40, 320, CYAN, 26, -50, 40, 0.6), (1080, 380, 340, VIOLET, 30, -50, -40, 0.8)]
    sharp = stars(W, h, 26, 23) + rays(1240, -60, n=4, length=900, spread=36, start=126)
    n, m, gap = 4, 34, 20
    cw = (W - 2 * m - (n - 1) * gap) / n
    b = ""
    for ci, (grp, (col, items)) in enumerate(TOOLKIT.items()):
        x = m + ci * (cw + gap)
        inner = bead(x + 42, 78, 18, col, pulse=ci) + text(x + 72, 86, grp, 23, 700, ls=-0.3)
        for ri, it in enumerate(items):
            y = 116 + ri * 45
            k = (ci * 6 + ri) * 0.35
            inner += (f'<rect x="{x+18}" y="{y}" width="{cw-36}" height="35" rx="17.5" fill="#fff" fill-opacity="0.07" stroke="#fff" stroke-opacity="0.22">'
                      f'<animate attributeName="fill-opacity" values="0.07;0.07;0.22;0.07;0.07" keyTimes="0;0.02;0.06;0.14;1" dur="9s" begin="{k:.2f}s" repeatCount="indefinite"/></rect>'
                      f'<circle cx="{x+38}" cy="{y+17.5}" r="4" fill="{col}"/>'
                      + text(x + 54, y + 23, it, 15, 500, op=0.93))
        b += glass(x, 34, cw, h - 68, 30, inner, sweep=ci * 0.12, tint=col, frost_sharp=True)
    return stage(W, h, b, "Toolkit: " + "; ".join(f"{g}: {', '.join(v[1])}" for g, v in TOOLKIT.items()), blobs, sharp)


def research():
    h = 170
    blobs = [(160, 80, 300, MINT, 25, 60, 20, 0.6), (700, 160, 320, BLUE, 30, -70, -30, 0.7), (1100, 20, 260, VIOLET, 27, -50, 30, 0.7)]
    inner = (f'<text x="68" y="112" font-size="72" font-weight="700" letter-spacing="-2" fill="url(#name)">62.5%</text>'
             + text(300, 72, "RESEARCH  ·  PUBLISHED 2025", 13, 700, op=0.7, ls=3)
             + text(300, 102, "better reward personalisation", 25, 600)
             + text(300, 130, "Random Forest, XGBoost and K-Means · International Journal of Computational Intelligence Systems", 14, 400, op=0.8))
    b = glass(28, 26, W - 56, h - 52, 32, inner, sweep=0.1, frost_sharp=True)
    extra = ('<linearGradient id="name" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="0.5" stop-color="#a7f3d0"/><stop offset="1" stop-color="#fff"/>'
             '<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="5s" repeatCount="indefinite"/></linearGradient>')
    return stage(W, h, b, "Research: 62.5% better reward personalisation from a Random Forest, XGBoost and K-Means system, published in the International Journal of Computational Intelligence Systems (2025).",
                 blobs, stars(W, h, 14, 5), extra_defs=extra)


# ------------------------------------------------------------------ buttons, footer, avatar
def button(label, col, glyph):
    w, h = 280, 72
    blobs = [(40, 10, 150, col, 9, 60, 20, 0.95), (250, 70, 140, BLUE, 11, -70, -20, 0.7)]
    inner = bead(40, 36, 17, col, glyph) + text(70, 43, label, 20, 600, ls=-0.2)
    inner += (f'<path d="M{w-40} 30 l7 6 l-7 6" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" opacity="0.8">'
              f'<animateTransform attributeName="transform" type="translate" values="0 0;4 0;0 0" dur="1.8s" repeatCount="indefinite"/></path>')
    b = glass(5, 5, w - 10, h - 10, 31, inner, sweep=0.05, shadow=False)
    return stage(w, h, b, label, blobs, r=36)


BTN_GLYPH = {
    "Email": '<rect x="-11" y="-8" width="22" height="16" rx="3"/><path d="M-10 -6 L0 2 L10 -6"/>',
    "LinkedIn": '<path d="M-9 -3 V9 M-9 -9 V-8.5 M-2 9 V-3 M-2 3 C-2 -5 9 -5 9 3 V9"/>',
    "GitHub": '<path d="M-7 -9 L-11 0 L-7 9 M7 -9 L11 0 L7 9 M3 -11 L-3 11"/>',
}


def footer():
    h = 220
    blobs = [(200, 220, 360, VIOLET, 24, 80, -30), (620, 240, 320, PINK, 28, -60, -30, 0.7), (1020, 220, 360, CYAN, 26, -80, -20, 0.7), (600, -40, 260, BLUE, 30, 40, 30, 0.6)]
    sharp = stars(W, h, 34, 31)
    for k, (amp, y0, dur, op) in enumerate([(22, 150, 11, 0.5), (16, 166, 8, 0.35), (28, 182, 14, 0.25)]):
        def wave(ph):
            pts = [f"{x},{y0 + amp*math.sin(x/190 + ph + k):.1f}" for x in range(-20, W + 40, 30)]
            return "M" + " L".join(pts)
        sharp += (f'<path fill="none" stroke="#fff" stroke-opacity="{op}" stroke-width="1.5" d="{wave(0)}">'
                  f'<animate attributeName="d" values="{wave(0)};{wave(math.pi)};{wave(2*math.pi)}" dur="{dur}s" repeatCount="indefinite"/></path>')
    inner = (f'<text x="600" y="92" font-size="30" font-weight="700" text-anchor="middle" letter-spacing="-0.5" fill="url(#name)">Thanks for stopping by</text>'
             + text(600, 120, "move  ·  see  ·  know  ·  act  ·  ship", 13, 600, op=0.75, anchor="middle", ls=4))
    b = glass(330, 40, 540, 104, 40, inner, sweep=0.1, frost_sharp=True)
    extra = ('<linearGradient id="name" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="0.5" stop-color="#9be8ff"/><stop offset="1" stop-color="#fff"/>'
             '<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="5s" repeatCount="indefinite"/></linearGradient>')
    return stage(W, h, b, "Thanks for stopping by", blobs, sharp, extra_defs=extra)


def avatar():
    s = 1000
    blobs = [(240, 220, 620, VIOLET, 26, 0, 0), (820, 300, 560, CYAN, 26, 0, 0, 0.8), (700, 860, 620, PINK, 26, 0, 0, 0.85), (180, 820, 460, BLUE, 26, 0, 0), (520, 480, 360, AMBER, 26, 0, 0, 0.4)]
    sharp = rays(-60, -80, n=5, length=1500, spread=44, start=22) + stars(s, s, 40, 9)
    inner = (f'<text x="500" y="606" font-size="330" font-weight="700" text-anchor="middle" letter-spacing="-14" fill="#000" fill-opacity="0.22">AK</text>'
             f'<text x="500" y="596" font-size="330" font-weight="700" text-anchor="middle" letter-spacing="-14" fill="#fff">AK</text>')
    b = glass(170, 170, 660, 660, 200, inner, frost_sharp=True)
    b += bead(790, 230, 54, CYAN) + bead(216, 800, 34, PINK)
    return stage(s, s, b, "AK", blobs, sharp, r=0)


def write(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(s)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "glass")
    jobs = {"hero": hero(), "story": story(), "toolkit": toolkit(), "research": research(), "footer": footer(), "bot-scene": bot_scene(), "avatar": avatar(),
            "section-01": section("01", "Story", "ONE LOOP, FIVE STOPS", VIOLET, CYAN),
            "section-02": section("02", "Projects", "FIVE REPOS, IN LOOP ORDER", PINK, AMBER),
            "section-03": section("03", "Toolkit", "WHAT I HAVE BUILT WITH", CYAN, MINT),
            "section-04": section("04", "Contact", "SAY HELLO", MINT, VIOLET)}
    # each card matches the aspect ratio of the demo it sits beside
    for i, hh in enumerate([420, 450, 426, 365, 432]):
        jobs[f"card-{STOPS[i][1]}"] = project(i, h=hh)
    for lab, col in [("Email", PINK), ("LinkedIn", BLUE), ("GitHub", VIOLET)]:
        jobs[f"btn-{lab.lower()}"] = button(lab, col, BTN_GLYPH[lab])
    for k, v in jobs.items():
        write(f"{out}/{k}.svg", v)
        print(k, len(v))
