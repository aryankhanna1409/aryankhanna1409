"""Coffee-lounge design kit shared by the profile and every repo README.

Walnut wall, smoked amber glass, brass trim. Generates animated SVGs (SMIL, so
they play inside GitHub READMEs):
  hero, loop strip, section bars, project cards, roast (experience),
  reserve shelf, tasting notes (skills), origin, contact buttons, footer,
  avatar, and a banner + footer for every repo.

    python scripts/kit.py                 # profile assets -> ../assets
    python scripts/kit.py --repo NAME DIR # banner + footer for one repo
"""
import os
import sys

W = 880
CREMA, PARCH, BRASS = "#efdfc4", "#bda98b", "#cfa75c"
SERIF = "'Bodoni 72','Bodoni MT',Didot,'Playfair Display',Georgia,'Times New Roman',serif"
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'SF Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"

# The story: one loop, five pours, one repo each.
# (brew stage, verb, repo, tag, one-line description, chips)
STOPS = [
    ("Grind", "MOVE", "autonomous-bot", "Team build",
     "A ROS 2 robot that maps, localises and navigates on its own, with an IoT dashboard and a swarm auction.",
     ["ROS 2", "C++", "Nav2", "SLAM", "OpenRMF", "MQTT"]),
    ("Bloom", "SEE", "sentinel", "Thermal-ready",
     "Search-and-rescue vision: a YOLO11 scanner that finds people who are hidden or in the dark, across RGB, near-infrared and thermal views.",
     ["YOLO11", "OpenCV", "ONNX", "Python"]),
    ("Steep", "KNOW", "finintel", "Prototype",
     "A financial RAG system that writes grounded, citation-backed advisory reports from SEC filings.",
     ["RAG", "GraphRAG", "Python", "Claude API", "64 tests"]),
    ("Pour", "ACT", "nexus", "Prototype",
     "Network intelligence and a policy-gated DevSecOps agent: it finds the root cause, proposes the fix and waits for approval.",
     ["C", "FastAPI", "PostgreSQL", "Redis", "React"]),
    ("Serve", "SHIP", "dishdecoded", "Product",
     "Snap a dish or a menu and get its story, allergens and a recipe.",
     ["Next.js 15", "React 19", "TypeScript", "Claude vision"]),
]

# Off the menu: (display name, tagline, chips)
ARCHIVE = {
    "one-click-crave": ("One Click Crave", "An AI meal assistant, shaped by six months of testing with blind, deaf and elderly users.",
                        ["Base44", "Python", "Streamlit", "Accessibility"]),
    "snacksave": ("SnackSave", "An Android app that taps you on the shoulder before an unnecessary coffee.",
                  ["Kotlin", "Jetpack Compose", "Geofencing"]),
    "credit-card": ("credit-card", "Spending-habit segmentation and reward modelling on Indian credit-card data.",
                    ["Python", "scikit-learn", "XGBoost", "IJCIS 2025"]),
    "murdle": ("Murdle", "A terminal whodunit where your AI assistant knows the answer and is insufferable about it.",
               ["Python", "ChatGPT API", "Terminal"]),
    "overthinkers-assistant": ("Overthinker's Assistant", "Type a decision. Get pros, cons, sarcasm and a flowchart.",
                               ["Python", "Flask", "Graphviz"]),
    "auto_wordle": ("auto_wordle", "A bot that opens today's Wordle, reads the tiles and solves it for you.",
                    ["Python", "Playwright"]),
    "fakespotter": ("fakespotter", "Tracks how Reddit talks about counterfeit goods and scores the sentiment of every thread.",
                    ["Python", "PRAW", "DistilBERT", "pandas"]),
    "kinematics-calculator": ("Kinematics Calculator", "Forward and inverse kinematics for robot arms of 1 to 6 degrees of freedom, with 3D animation.",
                              ["Python", "NumPy", "Matplotlib", "Colab"]),
}


# ------------------------------------------------------------------ primitives
def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def defs(w, h, rx=22):
    return f"""<defs>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#24150c"/><stop offset=".6" stop-color="#170e09"/><stop offset="1" stop-color="#0f0906"/></linearGradient>
<radialGradient id="lamp" cx=".84" cy="0" r=".95"><stop offset="0" stop-color="#cfa75c" stop-opacity=".30"/><stop offset="1" stop-color="#cfa75c" stop-opacity="0"/></radialGradient>
<radialGradient id="ember" cx="0" cy=".7" r=".8"><stop offset="0" stop-color="#7a3a1e" stop-opacity=".55"/><stop offset="1" stop-color="#7a3a1e" stop-opacity="0"/></radialGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#efdfc4" stop-opacity=".13"/><stop offset="1" stop-color="#efdfc4" stop-opacity=".03"/></linearGradient>
<linearGradient id="green" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1d4435" stop-opacity=".85"/><stop offset="1" stop-color="#efdfc4" stop-opacity=".04"/></linearGradient>
<linearGradient id="brass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f3d898"/><stop offset=".5" stop-color="#cfa75c"/><stop offset="1" stop-color="#8a5a22"/></linearGradient>
<linearGradient id="neo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a2411"/><stop offset="1" stop-color="#22140b"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cfa75c" stop-opacity=".75"/><stop offset="1" stop-color="#cfa75c" stop-opacity="0"/></linearGradient>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".11 .005" numOctaves="3" seed="7"/><feColorMatrix values="0 0 0 0 .62  0 0 0 0 .38  0 0 0 0 .2  1.4 0 0 0 -.42"/></filter>
<filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="36"/></filter>
<filter id="lift" x="-20%" y="-40%" width="140%" height="190%"><feDropShadow dx="3" dy="4" stdDeviation="4" flood-color="#000" flood-opacity=".6"/><feDropShadow dx="-2" dy="-2" stdDeviation="2.5" flood-color="#96623a" flood-opacity=".26"/></filter>
<clipPath id="clip"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>
</defs>"""


def svg(w, h, body, label, rx=22):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" '
            f'aria-label="{esc(label)}">{defs(w, h, rx)}{body}</svg>')


def wall(w, h, blobs=True, rx=22):
    b = f'<g clip-path="url(#clip)"><rect width="{w}" height="{h}" fill="url(#wall)"/>'
    b += f'<rect width="{w}" height="{h}" fill="url(#ember)"/><rect width="{w}" height="{h}" fill="url(#lamp)"/>'
    b += f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity=".5"/>'
    if blobs:
        b += (f'<ellipse cx="{w*.12:.0f}" cy="{h*.75:.0f}" rx="130" ry="90" fill="#8a4a22" opacity=".5" filter="url(#blur)">'
              f'<animateTransform attributeName="transform" type="translate" values="0 0;34 -18;-18 12;0 0" dur="24s" repeatCount="indefinite"/></ellipse>')
        b += (f'<ellipse cx="{w*.62:.0f}" cy="{h*.95:.0f}" rx="150" ry="80" fill="#1d4435" opacity=".55" filter="url(#blur)">'
              f'<animateTransform attributeName="transform" type="translate" values="0 0;-40 -14;22 10;0 0" dur="29s" repeatCount="indefinite"/></ellipse>')
    b += '</g>'
    b += f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="{BRASS}" stroke-opacity=".3"/>'
    return b


def t(x, y, s, size, fill=CREMA, family=SANS, italic=False, anchor=None, ls=None, weight=None, opacity=None):
    a = f' font-style="italic"' if italic else ""
    a += f' text-anchor="{anchor}"' if anchor else ""
    a += f' letter-spacing="{ls}"' if ls else ""
    a += f' font-weight="{weight}"' if weight else ""
    a += f' opacity="{opacity}"' if opacity else ""
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{fill}"{a}>{esc(s)}</text>'


def eyebrow(x, y, s, fill=BRASS, anchor=None):
    return t(x, y, s.upper(), 11.5, fill, MONO, ls="2.6", anchor=anchor)


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        if cur and len(cur) + len(wd) + 1 > n:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return lines


def para(x, y, text, n, size=14, fill=PARCH, lh=None, family=SANS, italic=False):
    lh = lh or round(size * 1.5)
    out = ""
    for i, ln in enumerate(wrap(text, n)):
        out += t(x, y + i * lh, ln, size, fill, family, italic=italic)
    return out, y + len(wrap(text, n)) * lh


def glass(x, y, w, h, rx=18, fill="glass"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{fill})" stroke="{BRASS}" stroke-opacity=".34"/>'
            f'<path d="M{x+rx} {y+1.2} H{x+w-rx}" stroke="#fff0d2" stroke-opacity=".22" stroke-linecap="round"/>')


def chip_w(s):
    return round(len(s) * 7.3 + 26)


def chips(x, y, items, maxx=W - 40, gap=9):
    """Raised neumorphic chips; wraps to new rows. Returns (svg, bottom y)."""
    out, cx, cy = "", x, y
    for it in items:
        cw = chip_w(it)
        if cx + cw > maxx and cx > x:
            cx, cy = x, cy + 36
        out += (f'<g filter="url(#lift)"><rect x="{cx}" y="{cy}" width="{cw}" height="27" rx="13.5" fill="url(#neo)" stroke="{BRASS}" stroke-opacity=".16"/></g>'
                + t(cx + cw / 2, cy + 18, it, 12, CREMA, MONO, anchor="middle"))
        cx += cw + gap
    return out, cy + 27


def tag(x, y, s, green=False):
    w = round(len(s) * 7.6 + 22)
    col = "#8fc7ab" if green else BRASS
    bg = f'fill="#1d4435" fill-opacity=".5"' if green else 'fill="none"'
    return (f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="11" {bg} stroke="{col}" stroke-opacity=".6"/>'
            + t(x + w / 2, y + 15, s.upper(), 10.5, col, MONO, anchor="middle", ls="1.4")), w


def steam(x, y, s=1.0, n=3):
    out = f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{CREMA}" stroke-width="2" stroke-linecap="round">'
    for i in range(n):
        dx = i * 18
        out += (f'<path d="M{dx} 40c-8-10 8-15 0-25s6-12 2-18" opacity="0">'
                f'<animate attributeName="opacity" values="0;.65;0" dur="4.5s" begin="{i*1.4:.1f}s" repeatCount="indefinite"/>'
                f'<animateTransform attributeName="transform" type="translate" values="0 10;0 -12" dur="4.5s" begin="{i*1.4:.1f}s" repeatCount="indefinite"/></path>')
    return out + '</g>'


def bean(x, y, r=7, rot=-28, on=True):
    f = 'fill="url(#brass)"' if on else f'fill="{BRASS}" fill-opacity=".18"'
    return (f'<g transform="translate({x},{y}) rotate({rot})"><ellipse rx="{r*.72:.1f}" ry="{r}" {f}/>'
            f'<path d="M0 {-r*.8:.1f}c{r*.45:.1f} {r*.5:.1f} {-r*.45:.1f} {r*1.1:.1f} 0 {r*1.6:.1f}" fill="none" stroke="#1a0f08" stroke-opacity=".7" stroke-width="1"/></g>')


# ------------------------------------------------------------------ icons (in a 170 x 170 box)
def icon(kind):
    s = f'fill="none" stroke="url(#brass)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "Grind":   # two beans and a few grounds
        g = f'<g {s}><g transform="translate(66,82) rotate(-32)"><ellipse rx="26" ry="38"/><path d="M0 -32c14 14 -14 44 0 64"/></g>'
        g += f'<g transform="translate(116,104) rotate(24)"><ellipse rx="17" ry="25"/><path d="M0 -21c9 9 -9 30 0 42"/></g></g>'
        g += f'<g fill="{BRASS}">' + "".join(f'<circle cx="{x}" cy="{y}" r="1.8"/>' for x, y in [(112, 54), (124, 62), (104, 44), (132, 50), (40, 132), (54, 140)]) + '</g>'
        return g
    if kind == "Bloom":   # pour-over dripper on a carafe
        return (f'<g {s}><path d="M42 44h86l-26 46h-34z"/><path d="M60 90h50"/><path d="M68 98h34l12 44a6 6 0 0 1-6 7h-46a6 6 0 0 1-6-7z"/>'
                f'<path d="M62 124h46" stroke-opacity=".6"/></g>'
                f'<circle cx="85" cy="100" r="2.4" fill="{BRASS}"><animate attributeName="cy" values="94;120" dur="1.6s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="1;0" dur="1.6s" repeatCount="indefinite"/></circle>' + steam(66, 2, .9))
    if kind == "Steep":   # french press
        return (f'<g {s}><rect x="52" y="52" width="58" height="92" rx="6"/><path d="M46 52h70"/><path d="M81 22v52"/><circle cx="81" cy="18" r="6"/>'
                f'<path d="M56 74h50"/><path d="M110 70h10a14 14 0 0 1 14 14v26a14 14 0 0 1-14 14h-10"/><path d="M52 112h58" stroke-opacity=".55"/></g>')
    if kind == "Pour":    # gooseneck kettle
        return (f'<g {s}><path d="M56 70h54l10 62a8 8 0 0 1-8 9H54a8 8 0 0 1-8-9z"/><path d="M62 70a21 12 0 0 1 42 0"/><circle cx="83" cy="52" r="5"/>'
                f'<path d="M48 116c-18-4-24-22-22-44s-2-30-12-32"/><path d="M112 82c22-10 34 6 26 26s-22 18-22 18"/></g>'
                f'<path d="M14 44v30" stroke="{BRASS}" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="4 7">'
                f'<animate attributeName="stroke-dashoffset" values="0;-22" dur="1.2s" repeatCount="indefinite"/></path>')
    if kind == "Serve":   # cup and saucer
        return (f'<g {s}><path d="M40 70h82v22a38 38 0 0 1-38 38h-6a38 38 0 0 1-38-38z"/><path d="M122 78h8a14 14 0 0 1 0 28h-10"/>'
                f'<path d="M30 142h102"/><path d="M48 80h66" stroke-opacity=".55"/></g>' + steam(62, 14, 1.0))
    # archive: a house stamp with one bean
    return (f'<g {s}><circle cx="85" cy="85" r="56" stroke-dasharray="3 6"/><circle cx="85" cy="85" r="44"/>'
            f'<g transform="translate(85,85) rotate(-30)"><ellipse rx="17" ry="25"/><path d="M0 -21c9 9 -9 30 0 42"/></g></g>')


# ------------------------------------------------------------------ profile pieces
def hero():
    h = 440
    b = wall(W, h)
    b += eyebrow(48, 66, "Robotics & AI · Pune, India")
    b += t(42, 168, "Aryan", 100, CREMA, SERIF)
    b += t(98, 258, "Khanna", 100, BRASS, SERIF, italic=True)
    b += t(48, 312, "I build AI for the real world.", 25, CREMA, SERIF, italic=True)
    b += t(48, 346, "Search-and-rescue vision, warehouse robots and FinTech ML.", 14.5, PARCH)
    b += t(48, 368, "Incoming FDE intern at Incedo · published researcher", 14.5, PARCH)
    b += t(48, 390, "Robotics & Automation at SIT Pune, class of 2027", 14.5, PARCH)
    # menu card
    x, y, w, hh = 548, 86, 290, 300
    b += steam(x + 206, y - 52, 1.1)
    b += glass(x, y, w, hh)
    b += eyebrow(x + 24, y + 36, "House notes")
    b += t(x + 24, y + 68, "Served since 2023", 23, CREMA, SERIF, italic=True)
    rows = [("Projects in the loop", "5"), ("Peer-reviewed paper", "1"), ("Patent application published", "1"),
            ("Robocon 2026 prelim score", "90/100"), ("B.Tech CGPA", "8.14")]
    for i, (k, v) in enumerate(rows):
        ry = y + 104 + i * 34
        b += f'<path d="M{x+24} {ry-20}H{x+w-24}" stroke="{BRASS}" stroke-opacity=".25" stroke-dasharray="3 4"/>'
        b += t(x + 24, ry, k, 13, PARCH) + t(x + w - 24, ry + 1, v, 19, CREMA, SERIF, anchor="end")
    b += t(x + 24, y + hh - 20, "NEXT POUR: INCEDO, JANUARY 2027", 10, PARCH, MONO, ls="1")
    return svg(W, h, b, "Aryan Khanna. I build AI for the real world. Robotics and AI, Pune, India.")


def section_bar(kicker, plain, em):
    h = 96
    b = wall(W, h, blobs=False, rx=18)
    b += eyebrow(30, 36, kicker)
    b += (f'<text x="28" y="74" font-family="{SERIF}" font-size="36" fill="{CREMA}">{esc(plain)} '
          f'<tspan font-style="italic" fill="{BRASS}">{esc(em)}</tspan></text>')
    for i in range(3):
        b += bean(W - 44 - i * 22, 50, 7, -28 + i * 14, on=(i == 0))
    b += f'<rect x="30" y="86" width="{W-60}" height="1" fill="url(#fade)"/>'
    return svg(W, h, b, f"{kicker}: {plain} {em}", rx=18)


def loop_row(y, current=None, x0=40, x1=W - 40, compact=False):
    """Five brew stages joined by a brass pour line. `current` is a repo name."""
    n = len(STOPS)
    step = (x1 - x0) / n
    xs = [x0 + step * (i + .5) for i in range(n)]
    b = f'<path d="M{xs[0]} {y}H{xs[-1]}" stroke="{BRASS}" stroke-opacity=".25" stroke-width="2"/>'
    b += (f'<path d="M{xs[0]} {y}H{xs[-1]}" stroke="url(#brass)" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="60 {xs[-1]-xs[0]}">'
          f'<animate attributeName="stroke-dashoffset" values="60;{-(xs[-1]-xs[0])}" dur="5s" repeatCount="indefinite"/></path>')
    for i, (brew, verb, repo, *_r) in enumerate(STOPS):
        on = current is None or repo == current
        op = "1" if on else ".5"
        x = xs[i]
        if repo == current:
            b += (f'<circle cx="{x}" cy="{y}" r="15" fill="none" stroke="{BRASS}" stroke-opacity=".7">'
                  f'<animate attributeName="r" values="12;19;12" dur="2.6s" repeatCount="indefinite"/>'
                  f'<animate attributeName="stroke-opacity" values=".8;0;.8" dur="2.6s" repeatCount="indefinite"/></circle>')
        b += f'<circle cx="{x}" cy="{y}" r="{9 if repo == current else 7}" fill="url(#brass)" stroke="#150d09" stroke-width="3" opacity="{op}"/>'
        if compact:
            b += t(x, y + 26, f"{brew.upper()} · {verb}", 10, BRASS if repo == current else PARCH, MONO, anchor="middle", ls="1.2", opacity=op)
        else:
            b += t(x, y - 22, f"0{i+1}", 11, PARCH, MONO, anchor="middle", ls="2", opacity=op)
            b += t(x, y + 40, brew, 25, CREMA, SERIF, italic=True, anchor="middle", opacity=op)
            b += t(x, y + 62, f"{verb} · {repo}", 10.5, BRASS, MONO, anchor="middle", opacity=op)
    return b


def loop(current=None):
    h = 168
    b = wall(W, h, blobs=False) + loop_row(64, current)
    label = "The loop: grind (move), bloom (see), steep (know), pour (act), serve (ship)"
    if current:
        label = f"{current} is one pour in a five-stage loop: move, see, know, act, ship"
    return svg(W, h, b, label)


def archive_card(key):
    name, tagline, cs = ARCHIVE[key]
    w, h = 432, 190
    b = wall(w, h, blobs=False, rx=18)
    b += eyebrow(26, 38, "Off the menu")
    size = min(30, int(380 / (len(name) * .56)))
    b += t(24, 76, name, size, CREMA, SERIF)
    p, _ = para(26, 104, tagline, 54, 13.5, PARCH, 20)
    b += p
    b += t(26, h - 22, " · ".join(cs).upper(), 10, BRASS, MONO, ls="1.2")
    b += bean(w - 34, 34, 8)
    return svg(w, h, b, f"{name}: {tagline}", rx=18)


ROLES = [
    ("From Jan 2027", 1, "Forward Deployed Engineer Intern", "Incedo · Hi-Tech · Pune",
     "Joining for six months through the North Stars intern program, one of 14 students selected from SIT. Pre-joining work so far: the AWS AI Practitioner certification and the nexus project."),
    ("Sep 2024 – now", 5, "Research Assistant", "Symbiosis Institute of Technology",
     "Applied research across machine learning, autonomous robots and computer vision. Built the credit-card reward system that reached R² 0.99 and a 62.5% improvement in personalisation, worked on the IoT warehouse robot, and now the multimodal search-and-rescue system."),
    ("Jan – Jun 2026", 4, "Documentation Lead & Vision Mentor", "Team Robominds · DD Robocon 2026",
     "Helped lead vision across two robots: camera calibration, model training, datasets and testing. Deployed the vision pipeline for the navigation team and taught the basics to juniors. The team scored 90/100 and reached the National Finals at IIT Delhi."),
    ("Jul – Dec 2025", 3, "Research Intern", "SCAAI · Symbiosis Centre for Applied AI",
     "Built and evaluated models for applied AI projects focused on deployment, compliance and automation, and designed the experiments that validated them."),
    ("Mar – Dec 2025", 3, "Club Head, Robotic Process Automation", "Department of Robotics and Automation, SIT",
     "Re-established the club and ran 5+ workshops, webinars and industry events for 150+ students."),
    ("Aug 2025 – now", 2, "Student Coordinator", "Campus Wellness Advisory Committee · SCHC",
     "Coordinates student-facing programs that reach 500+ students and keeps students and faculty talking to each other."),
]


def roast():
    rows, y = "", 18
    for when, lvl, title, org, desc in ROLES:
        lines = wrap(desc, 92)
        rh = 84 + len(lines) * 20
        rows += glass(18, y, W - 36, rh)
        rows += t(42, y + 38, when.upper(), 11, PARCH, MONO, ls="1")
        for k in range(5):
            rows += bean(48 + k * 17, y + 62, 6.5, -24, on=k < lvl)
        rows += t(196, y + 42, title, 24, CREMA, SERIF)
        rows += t(196, y + 64, org, 13.5, BRASS)
        for k, ln in enumerate(lines):
            rows += t(196, y + 90 + k * 20, ln, 13.5, PARCH)
        y += rh + 14
    h = y + 4
    return svg(W, h, wall(W, h) + rows, "Experience, newest first: " + "; ".join(f"{r[2]}, {r[3]}, {r[0]}" for r in ROLES))


def reserve():
    h = 424
    b = wall(W, h)
    # the paper
    x, y, w, hh = 18, 18, 330, 388
    b += glass(x, y, w, hh, fill="green")
    b += eyebrow(x + 24, y + 38, "Published · IJCIS 2025")
    ty = y + 74
    for ln in wrap("Analyzing and Rewarding Credit Card Spending Habits in India: a Machine Learning Approach", 27):
        b += t(x + 24, ty, ln, 22, CREMA, SERIF, italic=True)
        ty += 28
    p, ty = para(x + 24, ty + 8, "International Journal of Computational Intelligence Systems. Random Forest, XGBoost and K-Means.", 42, 13, PARCH, 19)
    b += p
    b += t(x + 24, y + hh - 54, "0.99", 46, BRASS, SERIF) + t(x + 24, y + hh - 28, "R² on reward prediction", 12.5, PARCH)
    b += t(x + 182, y + hh - 54, "62.5%", 46, BRASS, SERIF) + t(x + 182, y + hh - 28, "better personalisation", 12.5, PARCH)
    cells = [
        ("Patent", None, "IoT-Enabled Low-Cost Mobile Robot System for Autonomous Search and Rescue",
         "Application published by the Indian Patent Office."),
        ("Competition", "90/100", None, "DD Robocon 2026 preliminary round, through to the National Finals at IIT Delhi."),
        ("Certification", None, "AWS Certified AI Practitioner", "Passed October 2026. Generative AI, foundation models and responsible AI on AWS."),
        ("Coursework", "12", None, "Claude Academy courses: Claude Code, MCP, agent skills, the API, AWS and Google Cloud."),
    ]
    for i, (k, big, title, desc) in enumerate(cells):
        cx, cy, cw, ch = 364 + (i % 2) * 254, 18 + (i // 2) * 201, 240, 187
        b += glass(cx, cy, cw, ch)
        b += eyebrow(cx + 20, cy + 34, k)
        yy = cy + 62
        if big:
            b += t(cx + 20, cy + 84, big, 46, BRASS, SERIF)
            yy = cy + 112
        if title:
            for ln in wrap(title, 26):
                b += t(cx + 20, yy, ln, 16.5, CREMA, SERIF)
                yy += 21
            yy += 4
        p, _ = para(cx + 20, yy, desc, 34, 12, PARCH, 17)
        b += p
    return svg(W, h, b, "Research and recognition: IJCIS 2025 paper (R squared 0.99, 62.5% better personalisation), published patent application, "
               "DD Robocon 2026 national finals with 90/100, AWS Certified AI Practitioner, 12 Claude Academy courses")


NOTES = [
    ("Body · robotics", ["ROS 2", "Nav2", "SLAM", "OpenRMF", "C++", "Arduino", "STM32", "Jetson"]),
    ("Aroma · vision", ["OpenCV", "YOLO11", "ONNX", "Camera calibration", "Sensor fusion"]),
    ("Acidity · AI & data", ["Python", "Machine learning", "RAG", "LLM agents", "XGBoost", "SQL"]),
    ("Finish · software", ["FastAPI", "React", "Next.js", "TypeScript", "C", "PostgreSQL", "Docker", "Kotlin"]),
]


def notes():
    body, y = "", 44
    for k, items in NOTES:
        body += eyebrow(40, y, k, PARCH)
        c, yb = chips(40, y + 14, items, maxx=W - 40)
        body += c
        y = yb + 40
    h = y - 8
    return svg(W, h, wall(W, h) + glass(18, 14, W - 36, h - 28) + body,
               "Skills: " + "; ".join(f"{k}: {', '.join(v)}" for k, v in NOTES))


SCHOOLS = [
    ("2023 – 2027", "B.Tech, Robotics & Automation", "Symbiosis Institute of Technology, Pune · CGPA 8.14"),
    ("2024 – 2026", "Diploma, Business Administration", "Symbiosis Institute of Business Management, Pune · 8.35"),
    ("Jan – Feb 2025", "Global Immersion Program, Dubai", "One of 25 students selected. Generative AI, sustainability and finance."),
]


def origin():
    h = 250
    b = wall(W, h, blobs=False) + glass(18, 14, W - 36, h - 28)
    for i, (when, what, where) in enumerate(SCHOOLS):
        y = 56 + i * 70
        if i:
            b += f'<path d="M40 {y-32}H{W-40}" stroke="{BRASS}" stroke-opacity=".25" stroke-dasharray="3 4"/>'
        b += t(42, y, when.upper(), 11, BRASS, MONO, ls="1")
        b += t(196, y, what, 22, CREMA, SERIF)
        b += t(196, y + 22, where, 13.5, PARCH)
    return svg(W, h, b, "Education: " + "; ".join(f"{b_}, {c} ({a})" for a, b_, c in SCHOOLS))


def button(kind, value):
    w, h = 432, 78
    b = (f'<g filter="url(#lift)"><rect x="8" y="8" width="{w-16}" height="{h-18}" rx="18" fill="url(#neo)" stroke="{BRASS}" stroke-opacity=".2"/></g>')
    b += f'<circle cx="46" cy="38" r="15" fill="none" stroke="url(#brass)" stroke-width="2"/>' + bean(46, 38, 7.5)
    b += t(76, 33, kind.upper(), 10.5, BRASS, MONO, ls="2")
    b += t(76, 53, value, 15, CREMA, SANS)
    b += t(w - 30, 44, "→", 18, BRASS, SANS, anchor="end")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" role="img" aria-label="{esc(kind)}: {esc(value)}">'
            f'{defs(w, h)}{b}</svg>')


def cup(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="url(#brass)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M0 0h62v16a28 28 0 0 1-28 28h-6a28 28 0 0 1-28-28z"/><path d="M62 6h6a11 11 0 0 1 0 22h-8"/><path d="M-8 54h78"/></g>')


def footer(line="Brewed slowly, shipped warm.", sub="ARYAN KHANNA · PUNE, INDIA"):
    h = 130
    b = wall(W, h, blobs=False)
    b += steam(86, 14, .9) + cup(74, 58)
    b += t(190, 68, line, 30, CREMA, SERIF, italic=True)
    b += t(192, 94, sub, 11, BRASS, MONO, ls="2.4")
    for i in range(4):
        b += bean(W - 50 - i * 24, 66, 8, -28 + i * 12, on=i < 2)
    return svg(W, h, b, line)


def avatar(S=500):
    b = (f'<rect width="{S}" height="{S}" fill="url(#wall)"/><rect width="{S}" height="{S}" fill="url(#ember)"/>'
         f'<rect width="{S}" height="{S}" fill="url(#lamp)"/><rect width="{S}" height="{S}" filter="url(#grain)" opacity=".5"/>')
    b += f'<circle cx="250" cy="250" r="176" fill="url(#glass)" stroke="url(#brass)" stroke-width="5"/>'
    b += f'<circle cx="250" cy="250" r="156" fill="none" stroke="{BRASS}" stroke-opacity=".5" stroke-dasharray="3 8" stroke-width="2"/>'
    b += t(250, 300, "AK", 150, BRASS, SERIF, italic=True, anchor="middle")
    b += bean(250, 118, 13) + bean(250, 384, 13, 28)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}" role="img" '
            f'aria-label="AK monogram in brass on walnut">{defs(S, S, 0)}{b}</svg>')


# ------------------------------------------------------------------ per-repo pieces
def repo_banner(key):
    stop = next((i for i, s in enumerate(STOPS) if s[2] == key), None)
    if stop is not None:
        brew, verb, name, tg, tagline, cs = STOPS[stop]
        kicker, kind = f"Stop 0{stop+1} of 05 · {verb} · the {brew}", brew
    else:
        name, tagline, cs = ARCHIVE[key]
        kicker, kind = "Off the menu · from the archive", "archive"
    h = 312
    b = wall(W, h)
    b += eyebrow(42, 60, kicker)
    if stop is not None:
        tsvg, tw = tag(0, 0, tg, green=tg != "Prototype")
        b += f'<g transform="translate({640-tw},44)">{tsvg}</g>'
    size = min(60, int(590 / (len(name) * .56)))
    b += t(40, 128, name, size, CREMA, SERIF)
    p, yb = para(42, 162, tagline, 68, 15, PARCH, 22)
    b += p
    c, _ = chips(42, max(yb, 196) + 0, cs, maxx=640)
    b += c
    b += glass(672, 44, 170, 170, rx=26) + f'<g transform="translate(672,44)">{icon(kind)}</g>'
    if stop is not None:
        b += loop_row(270, name, x0=30, x1=W - 30, compact=True)
    else:
        b += f'<rect x="42" y="268" width="{W-84}" height="1" fill="url(#fade)"/>'
        b += t(42, 290, "BREWED BY ARYAN KHANNA · PUNE, INDIA", 10, PARCH, MONO, ls="2.2")
        for i in range(3):
            b += bean(W - 50 - i * 22, 284, 7, -28 + i * 14, on=i == 0)
    return svg(W, h, b, f"{name}: {tagline}")


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) >= 4 and sys.argv[1] == "--repo":
        name, d = sys.argv[2], sys.argv[3]
        write(os.path.join(d, "assets", "banner.svg"), repo_banner(name))
        if any(s[2] == name for s in STOPS):
            write(os.path.join(d, "assets", "loop.svg"), loop(name))
        else:
            write(os.path.join(d, "assets", "footer.svg"), footer("Off the menu.", "FROM THE ARCHIVE · ARYAN KHANNA"))
        print("wrote banner + footer for", name)
    else:
        out = os.path.join(here, "..", "assets")
        write(f"{out}/hero.svg", hero())
        write(f"{out}/loop.svg", loop())
        for n, (k, p, e) in {"loop": ("The house blend", "One loop,", "five pours"),
                             "archive": ("Off the menu", "From the", "archive"),
                             "roast": ("Experience", "The", "roast"),
                             "reserve": ("Research & recognition", "The", "reserve shelf"),
                             "notes": ("Skills", "Tasting", "notes"),
                             "origin": ("Education", "The", "origin"),
                             "contact": ("Last call", "Let's talk over", "coffee")}.items():
            write(f"{out}/section-{n}.svg", section_bar(k, p, e))
        for s in STOPS:
            write(f"{out}/projects/{s[2]}.svg", repo_banner(s[2]))
        for k in ARCHIVE:
            write(f"{out}/archive/{k}.svg", archive_card(k))
        write(f"{out}/roast.svg", roast())
        write(f"{out}/reserve.svg", reserve())
        write(f"{out}/notes.svg", notes())
        write(f"{out}/origin.svg", origin())
        for n, k, v in [("email", "Email", "aryankhanna2k22@gmail.com"), ("github", "GitHub", "github.com/aryankhanna1409"),
                        ("linkedin", "LinkedIn", "linkedin.com/in/aryandkhanna"), ("orcid", "ORCID", "0009-0001-1710-2367")]:
            write(f"{out}/btn-{n}.svg", button(k, v))
        write(f"{out}/footer.svg", footer())
        write(f"{out}/avatar.svg", avatar())
        print("profile assets written")
