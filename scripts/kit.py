"""Retro-Macintosh design kit shared by the profile and every repo README.

Generates 1-bit SVGs (animated with SMIL, so they play inside GitHub READMEs):
  hero, story (the five-stop loop), extensions (skills), section bars,
  contact buttons, footer, per-repo banner + loop strip, and the avatar.

    python scripts/kit.py                 # profile assets -> ../assets
    python scripts/kit.py --repo NAME DIR # banner + loop strip for one repo
"""
import os
import sys

FONT = "Geneva, Monaco, 'Courier New', Courier, monospace"
W = 880
INK, PAPER = "#000", "#fff"

# The story: one loop, five stops, one repo each.
STOPS = [
    ("MOVE", "autonomous-bot", "a robot that maps and navigates"),
    ("SEE", "sentinel", "vision that finds people in the dark"),
    ("KNOW", "finintel", "AI that cites its sources"),
    ("ACT", "nexus", "an agent that fixes incidents"),
    ("SHIP", "dishdecoded", "a product people can use"),
]

DEFS = f"""<defs>
<pattern id="dither" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="{PAPER}"/><rect width="2" height="2" fill="{INK}"/><rect x="2" y="2" width="2" height="2" fill="{INK}"/></pattern>
<pattern id="light" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="{PAPER}"/><rect width="1" height="1" fill="{INK}"/><rect x="2" y="2" width="1" height="1" fill="{INK}"/></pattern>
<pattern id="stripes" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="{PAPER}"/><rect y="1" width="4" height="1" fill="{INK}"/></pattern>
<pattern id="gray" width="2" height="2" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="{PAPER}"/><rect width="1" height="1" fill="{INK}"/></pattern>
</defs>"""


def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" '
            f'aria-label="{label}" shape-rendering="crispEdges" font-family="{FONT}">{DEFS}{body}</svg>')


def window(x, y, w, h, title, inner="", shadow=3):
    tw = len(title) * 8 + 24
    return (f'<rect x="{x+shadow}" y="{y+shadow}" width="{w}" height="{h}" fill="{INK}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="22" fill="url(#stripes)"/>'
            f'<line x1="{x}" y1="{y+24}" x2="{x+w}" y2="{y+24}" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="{x+10}" y="{y+6}" width="13" height="13" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="{x+(w-tw)/2}" y="{y+3}" width="{tw}" height="18" fill="{PAPER}"/>'
            f'<text x="{x+w/2}" y="{y+17}" font-size="13" font-weight="bold" text-anchor="middle" fill="{INK}">{title}</text>'
            f'{inner}')


def happy_mac(x, y, s=1.0, blink=True):
    g = f'<g transform="translate({x},{y}) scale({s})">'
    g += f'<rect x="3" y="3" width="64" height="76" fill="{INK}"/>'
    g += f'<rect x="0" y="0" width="64" height="76" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
    g += f'<rect x="8" y="8" width="48" height="38" fill="url(#light)" stroke="{INK}" stroke-width="3"/>'
    g += f'<rect x="12" y="12" width="40" height="30" fill="{PAPER}"/>'
    for ex in (21, 38):
        a = (f'<animate attributeName="height" values="8;8;1;8;8" keyTimes="0;0.9;0.93;0.96;1" dur="4s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="19;19;26;19;19" keyTimes="0;0.9;0.93;0.96;1" dur="4s" repeatCount="indefinite"/>') if blink else ""
        g += f'<rect x="{ex}" y="19" width="4" height="8" fill="{INK}">{a}</rect>'
    g += f'<rect x="31" y="22" width="2" height="8" fill="{INK}"/>'
    g += f'<path d="M20 35 h4 v3 h16 v-3 h4" fill="none" stroke="{INK}" stroke-width="3"/>'
    g += f'<rect x="12" y="58" width="30" height="4" fill="{INK}"/><rect x="46" y="56" width="6" height="6" fill="{INK}"/>'
    g += f'<rect x="8" y="66" width="48" height="2" fill="url(#stripes)"/></g>'
    return g


def folder(x, y, label, sel_delay=None, s=1.0):
    """Desktop folder icon with an (optionally animated) selected label."""
    g = f'<g transform="translate({x},{y}) scale({s})">'
    g += f'<path d="M2 8 h16 l4 5 h30 v30 h-50z" fill="{INK}" transform="translate(3,3)"/>'
    g += f'<path d="M2 8 h16 l4 5 h30 v30 h-50z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    g += f'<line x1="2" y1="17" x2="52" y2="17" stroke="{INK}" stroke-width="2"/>'
    g += f'<rect x="5" y="20" width="44" height="20" fill="url(#gray)"/></g>'
    lw = len(label) * 7.4 + 8
    cx = x + 27 * s
    ly = y + 58 * s
    g += f'<rect x="{cx-lw/2}" y="{ly}" width="{lw}" height="16" fill="{PAPER}"/>'
    g += f'<rect x="{cx-lw/2}" y="{ly}" width="{lw}" height="16" fill="{INK}" opacity="0">'
    if sel_delay is not None:
        g += (f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{sel_delay:.2f};{sel_delay+0.01:.2f};{sel_delay+0.16:.2f};{sel_delay+0.17:.2f};1" '
              f'dur="10s" repeatCount="indefinite" calcMode="discrete"/>')
    g += '</rect>'
    g += f'<text x="{cx}" y="{ly+12}" font-size="12" font-weight="bold" text-anchor="middle" fill="{INK}">{label}</text>'
    if sel_delay is not None:  # inverted copy of the label while selected
        g += (f'<text x="{cx}" y="{ly+12}" font-size="12" font-weight="bold" text-anchor="middle" fill="{PAPER}" opacity="0">{label}'
              f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{sel_delay:.2f};{sel_delay+0.01:.2f};{sel_delay+0.16:.2f};{sel_delay+0.17:.2f};1" '
              f'dur="10s" repeatCount="indefinite" calcMode="discrete"/></text>')
    return g


def cursor(x, y):
    return (f'<g transform="translate({x},{y})"><path d="M0 0 v17 l4 -4 l3 7 l3 -1 l-3 -7 h6z" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/></g>')


def menubar(items, right=""):
    b = f'<rect width="{W}" height="26" fill="{PAPER}"/><line x1="0" y1="26" x2="{W}" y2="26" stroke="{INK}" stroke-width="2"/>'
    b += f'<rect x="14" y="7" width="12" height="13" rx="2" fill="{INK}"/>'
    x = 44
    for it in items:
        b += f'<text x="{x}" y="18" font-size="13" font-weight="bold" fill="{INK}">{it}</text>'
        x += len(it) * 9 + 18
    b += f'<text x="{W-16}" y="18" font-size="13" text-anchor="end" fill="{INK}">{right}</text>'
    return b


# ------------------------------------------------------------------ hero
def hero():
    h = 520
    b = f'<rect width="{W}" height="{h}" fill="url(#dither)"/>' + menubar(["File", "Edit", "View", "Special"], "Pune, IN")
    # main window
    L = [("Processor", "robotics engineer, class of 2027"),
         ("Built-in memory", "ROS 2 · PyTorch · C · React"),
         ("Startup disk", "5 projects, one loop"),
         ("Published", "IJCIS 2025, 62.5% better rewards"),
         ("Version", "robotics → AI → systems")]
    inner = happy_mac(46, 90, 1.55)
    inner += f'<text x="190" y="118" font-size="40" font-weight="bold" fill="{INK}">Aryan Khanna</text>'
    inner += f'<text x="192" y="144" font-size="14" fill="{INK}">About this portfolio</text>'
    inner += f'<line x1="190" y1="156" x2="560" y2="156" stroke="{INK}" stroke-width="2"/>'
    for i, (k, v) in enumerate(L):
        y = 182 + i * 26
        inner += f'<text x="192" y="{y}" font-size="13" font-weight="bold" fill="{INK}">{k}:</text>'
        inner += (f'<text x="330" y="{y}" font-size="13" fill="{INK}" opacity="0">{v}'
                  f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{0.05+i*0.07:.2f};{0.06+i*0.07:.2f};1" dur="9s" repeatCount="indefinite" calcMode="discrete"/></text>')
    inner += f'<text x="192" y="338" font-size="12" fill="{INK}">Loading the loop…</text>'
    inner += f'<rect x="192" y="346" width="368" height="14" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    inner += (f'<rect x="194" y="348" width="0" height="10" fill="url(#gray)"><animate attributeName="width" values="0;364;364" '
              f'keyTimes="0;0.8;1" dur="9s" repeatCount="indefinite"/></rect>')
    b += window(36, 50, 560, 318, "About This Portfolio", inner)
    note = (f'<text x="22" y="46" font-size="13" font-weight="bold" fill="{INK}">Now building</text>'
            f'<text x="22" y="68" font-size="12" fill="{INK}">Sentinel: an RGB-thermal rescue scanner</text>'
            f'<text x="22" y="86" font-size="12" fill="{INK}">autonomous-bot: an IoT mobile robot on ROS 2</text>'
            f'<text x="22" y="104" font-size="12" fill="{INK}">nexus: an autonomous DevSecOps agent</text>')
    b += window(36, 388, 560, 112, "Note Pad", "").replace('</svg>', '')
    b += f'<g transform="translate(36,388)">{note}</g>' 
    # desktop icons
    names = [s[1] for s in STOPS]
    for i, n in enumerate(names):
        b += folder(668, 52 + i * 84, n, sel_delay=0.04 + i * 0.19)
    # bottom hint + cursor
    b += f'<rect x="{W-210}" y="{h-30}" width="200" height="18" fill="{PAPER}"/><text x="{W-14}" y="{h-16}" font-size="12" font-weight="bold" text-anchor="end" fill="{INK}">5 folders · pick one below</text>'
    ky = [(700, 70), (700, 154), (700, 238), (700, 322), (700, 406), (700, 70)]
    vals = ";".join(f"{x},{y}" for x, y in ky)
    b += (f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" '
          f'keyTimes="0;0.2;0.4;0.6;0.8;1" dur="10s" repeatCount="indefinite" calcMode="spline" '
          f'keySplines="0.4 0 0.2 1;0.4 0 0.2 1;0.4 0 0.2 1;0.4 0 0.2 1;0.4 0 0.2 1"/>' + cursor(0, 0) + '</g>')
    return svg(W, h, b, "Aryan Khanna: robotics, AI and software, shown as a retro Macintosh desktop")


# ------------------------------------------------------------------ story
def stop_icon(kind, cx, cy):
    g = f'<g transform="translate({cx-24},{cy-20})" fill="none" stroke="{INK}" stroke-width="3">'
    if kind == "MOVE":  # robot with wheels and lidar
        g += f'<rect x="8" y="14" width="32" height="18"/><rect x="2" y="30" width="10" height="8" fill="{INK}"/><rect x="36" y="30" width="10" height="8" fill="{INK}"/><circle cx="24" cy="10" r="4" fill="{INK}"/>'
    elif kind == "SEE":  # eye
        g += f'<path d="M2 22 Q24 2 46 22 Q24 42 2 22z"/><circle cx="24" cy="22" r="7" fill="{INK}"/>'
    elif kind == "KNOW":  # document with lines
        g += f'<rect x="8" y="3" width="32" height="38"/><line x1="14" y1="13" x2="34" y2="13"/><line x1="14" y1="21" x2="34" y2="21"/><line x1="14" y1="29" x2="26" y2="29"/>'
    elif kind == "ACT":  # play / gear-ish arrow
        g += f'<circle cx="24" cy="22" r="17"/><path d="M19 13 L33 22 L19 31z" fill="{INK}"/>'
    else:  # SHIP: app window
        g += f'<rect x="3" y="5" width="42" height="34"/><line x1="3" y1="14" x2="45" y2="14"/><rect x="9" y="20" width="12" height="12" fill="{INK}"/><line x1="27" y1="22" x2="39" y2="22"/><line x1="27" y1="30" x2="39" y2="30"/>'
    return g + '</g>'


def story():
    h = 330
    b = f'<rect width="{W}" height="{h}" fill="url(#dither)"/>'
    inner = ""
    n = len(STOPS)
    bw, gap = 124, 30
    x0 = (W - 60 - (n * bw + (n - 1) * gap)) / 2 + 30 - 30
    x0 = 74
    cy = 120
    for i, (verb, repo, line) in enumerate(STOPS):
        x = x0 + i * (bw + gap)
        inner += f'<rect x="{x+3}" y="{cy-52+3}" width="{bw}" height="104" fill="{INK}"/>'
        inner += f'<rect x="{x}" y="{cy-52}" width="{bw}" height="104" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
        inner += f'<text x="{x+bw/2}" y="{cy-34}" font-size="11" font-weight="bold" text-anchor="middle" fill="{INK}">0{i+1}</text>'
        inner += stop_icon(verb, x + bw / 2, cy - 2)
        inner += f'<text x="{x+bw/2}" y="{cy+42}" font-size="14" font-weight="bold" text-anchor="middle" fill="{INK}">{verb}</text>'
        inner += f'<text x="{x+bw/2}" y="{cy+76}" font-size="12" font-weight="bold" text-anchor="middle" fill="{INK}">{repo}</text>'
        # wrap tagline in two lines
        words = line.split()
        mid = len(words) // 2 + (len(words) % 2)
        l1, l2 = " ".join(words[:mid]), " ".join(words[mid:])
        inner += f'<text x="{x+bw/2}" y="{cy+92}" font-size="10" text-anchor="middle" fill="{INK}">{l1}</text>'
        inner += f'<text x="{x+bw/2}" y="{cy+104}" font-size="10" text-anchor="middle" fill="{INK}">{l2}</text>'
        if i < n - 1:
            ax = x + bw + 4
            inner += (f'<line x1="{ax}" y1="{cy}" x2="{ax+gap-14}" y2="{cy}" stroke="{INK}" stroke-width="2" stroke-dasharray="6 4">'
                      f'<animate attributeName="stroke-dashoffset" from="20" to="0" dur="0.8s" repeatCount="indefinite"/></line>'
                      f'<path d="M{ax+gap-18} {cy-6} l8 6 l-8 6z" fill="{INK}"/>')
    # feedback loop under the boxes + travelling packet
    xl = x0 - 26
    xr = x0 + (n - 1) * (bw + gap) + bw + 26
    xs, xe = xl, xr
    ly = cy + 126
    path = f"M{xr-22} {cy} H{xr} V{ly} H{xl} V{cy} H{x0-6}"
    inner += f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="6 4"><animate attributeName="stroke-dashoffset" from="0" to="20" dur="1.2s" repeatCount="indefinite"/></path>'
    inner += f'<path d="M{x0-12} {cy-6} l8 6 l-8 6z" fill="{INK}"/>'
    inner += f'<rect x="{(xs+xe)/2-110}" y="{ly-9}" width="220" height="18" fill="{PAPER}"/><text x="{(xs+xe)/2}" y="{ly+4}" font-size="12" font-weight="bold" text-anchor="middle" fill="{INK}">what the system learns feeds back</text>'
    full = f"M{x0+bw/2} {cy-60} H{xr} V{ly} H{xl} V{cy-60} Z"
    inner += (f'<rect x="-5" y="-5" width="10" height="10" fill="{INK}"><animateMotion path="{full}" dur="7s" repeatCount="indefinite"/></rect>')
    b += window(18, 14, W - 42, h - 40, "The Loop: five stops, one idea", inner)
    return svg(W, h, b, "The loop: move, see, know, act, ship")


# ------------------------------------------------------------------ extensions (skills)
EXT = {
    "Robotics": ["ROS 2", "Nav2", "SLAM", "Sensor fusion (ESKF)", "RPLIDAR", "Arduino"],
    "Vision": ["YOLO11", "OpenCV", "PyTorch", "RGB-thermal fusion", "Jetson", "ONNX"],
    "AI": ["Claude API", "NVIDIA NIM", "RAG + GraphRAG", "Agent tool use", "Anomaly detection", "Random Forest"],
    "Systems": ["FastAPI", "PostgreSQL", "Redis", "React", "Docker", "C (ASan clean)"],
}


def extensions():
    h = 290
    b = f'<rect width="{W}" height="{h}" fill="{PAPER}"/>'
    inner = ""
    colw = (W - 70) / 4
    for ci, (grp, items) in enumerate(EXT.items()):
        x = 34 + ci * colw
        inner += f'<text x="{x}" y="64" font-size="14" font-weight="bold" fill="{INK}">{grp}</text><line x1="{x}" y1="72" x2="{x+colw-24}" y2="72" stroke="{INK}" stroke-width="2"/>'
        for ri, it in enumerate(items):
            y = 98 + ri * 28
            inner += f'<rect x="{x}" y="{y-12}" width="14" height="14" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
            inner += (f'<path d="M{x+3} {y-5} l3 4 l6 -9" fill="none" stroke="{INK}" stroke-width="2.5" opacity="0">'
                      f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{0.02+(ci*6+ri)*0.03:.2f};{0.03+(ci*6+ri)*0.03:.2f};1" dur="8s" repeatCount="indefinite" calcMode="discrete"/></path>')
            inner += f'<text x="{x+24}" y="{y}" font-size="13" fill="{INK}">{it}</text>'
    b += window(8, 6, W - 22, h - 20, "Extensions", inner)
    return svg(W, h, b, "Extensions: the tools I have built with")


# ------------------------------------------------------------------ section bars, buttons, footer
def section_bar(n, title):
    h = 40
    b = (f'<rect width="{W}" height="{h}" fill="{PAPER}"/>'
         f'<rect x="3" y="5" width="{W-8}" height="30" fill="{INK}"/>'
         f'<rect x="0" y="2" width="{W-8}" height="30" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
         f'<rect x="1" y="3" width="{W-10}" height="28" fill="url(#stripes)"/>'
         f'<rect x="10" y="9" width="16" height="16" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
    label = f"{n} · {title}"
    tw = len(label) * 9 + 28
    b += f'<rect x="{(W-8-tw)/2}" y="6" width="{tw}" height="22" fill="{PAPER}"/>'
    b += f'<text x="{(W-8)/2}" y="22" font-size="15" font-weight="bold" text-anchor="middle" fill="{INK}">{label}</text>'
    return svg(W, h, b, f"{n} {title}")


def button(label):
    w, h = 200, 46
    b = (f'<rect x="3" y="3" width="{w-5}" height="{h-5}" rx="10" fill="{INK}"/>'
         f'<rect x="1" y="1" width="{w-5}" height="{h-5}" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
         f'<rect x="5" y="5" width="{w-13}" height="{h-13}" rx="7" fill="none" stroke="{INK}" stroke-width="2">'
         f'<animate attributeName="stroke-dasharray" values="0 0;6 4;0 0" dur="3s" repeatCount="indefinite"/></rect>'
         f'<text x="{(w-4)/2}" y="28" font-size="15" font-weight="bold" text-anchor="middle" fill="{INK}">{label}</text>')
    return svg(w, h, b, label)


def footer():
    h = 200
    b = f'<rect width="{W}" height="{h}" fill="url(#dither)"/>'
    inner = happy_mac(90, 56, 1.0)
    inner += f'<text x="190" y="82" font-size="18" font-weight="bold" fill="{INK}">Thanks for stopping by.</text>'
    inner += f'<text x="190" y="108" font-size="13" fill="{INK}">It\'s now safe to build something together.</text>'
    inner += (f'<rect x="{W-200}" y="96" width="76" height="30" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
              f'<rect x="{W-196}" y="100" width="68" height="22" rx="5" fill="none" stroke="{INK}" stroke-width="2">'
              f'<animate attributeName="opacity" values="1;0;1" dur="1.4s" repeatCount="indefinite" calcMode="discrete"/></rect>'
              f'<text x="{W-162}" y="117" font-size="14" font-weight="bold" text-anchor="middle" fill="{INK}">OK</text>')
    b += window(60, 22, W - 120, 150, "Alert", inner)
    return svg(W, h, b, "Thanks for stopping by")


# ------------------------------------------------------------------ per-repo banner and loop strip
def scene(repo):
    """Small animated 1-bit scene (about 200x130) for each repo."""
    s = ""
    if repo == "autonomous-bot":
        s += f'<rect x="0" y="0" width="200" height="130" fill="url(#light)"/><rect x="10" y="10" width="180" height="110" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
        s += f'<path d="M30 100 H90 V60 H150 V30" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="5 4"/>'
        s += (f'<g><animateMotion path="M30 100 H90 V60 H150 V30" dur="6s" repeatCount="indefinite"/>'
              f'<rect x="-9" y="-7" width="18" height="14" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/><rect x="-11" y="-9" width="5" height="4" fill="{INK}"/><rect x="6" y="-9" width="5" height="4" fill="{INK}"/><rect x="-11" y="5" width="5" height="4" fill="{INK}"/><rect x="6" y="5" width="5" height="4" fill="{INK}"/>'
              f'<path d="M0 0 L26 -12 A28 28 0 0 1 26 12z" fill="url(#gray)" stroke="{INK}"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="2s" repeatCount="indefinite"/></path></g>')
    elif repo == "sentinel":
        s += f'<rect x="0" y="0" width="200" height="130" fill="{INK}"/><rect x="10" y="10" width="180" height="110" fill="url(#gray)" stroke="{PAPER}" stroke-width="2"/>'
        s += f'<circle cx="100" cy="46" r="11" fill="{PAPER}" stroke="{INK}" stroke-width="3"/><rect x="86" y="60" width="28" height="42" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
        for (x, y, dx, dy) in [(72, 26, 1, 1), (128, 26, -1, 1), (72, 108, 1, -1), (128, 108, -1, -1)]:
            s += f'<path d="M{x} {y+dy*14} V{y} H{x+dx*14}" fill="none" stroke="{INK}" stroke-width="4"><animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite" calcMode="discrete"/></path>'
        s += f'<rect x="12" y="12" width="176" height="3" fill="{INK}"><animate attributeName="y" values="12;115;12" dur="2.6s" repeatCount="indefinite"/></rect>'
        s += f'<rect x="62" y="12" width="76" height="13" fill="{PAPER}"/><text x="100" y="22" font-size="9" font-weight="bold" fill="{INK}" text-anchor="middle">person 0.91</text>'
    elif repo == "finintel":
        s += f'<rect x="0" y="0" width="200" height="130" fill="url(#light)"/><rect x="14" y="8" width="130" height="114" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
        for i in range(7):
            y = 24 + i * 14
            s += f'<line x1="24" y1="{y}" x2="{134 if i%3 else 112}" y2="{y}" stroke="{INK}" stroke-width="3"/>'
        s += f'<rect x="20" y="17" width="118" height="12" fill="url(#gray)" opacity="0.9"><animate attributeName="y" values="17;45;73;101;17" keyTimes="0;0.25;0.5;0.75;1" dur="6s" repeatCount="indefinite" calcMode="discrete"/></rect>'
        s += f'<rect x="132" y="48" width="58" height="30" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/><text x="161" y="68" font-size="13" font-weight="bold" text-anchor="middle" fill="{INK}">[1] [2]</text>'
        s += f'<path d="M132 63 H118" stroke="{INK}" stroke-width="2" stroke-dasharray="3 2"/>'
    elif repo == "nexus":
        s += f'<rect x="0" y="0" width="200" height="130" fill="url(#light)"/><rect x="10" y="8" width="180" height="114" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
        s += f'<path d="M20 92 H70 L90 40 L120 28 L134 30 L150 84 H182" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="320" stroke-dashoffset="320"><animate attributeName="stroke-dashoffset" values="320;0;0;320" keyTimes="0;0.6;0.9;1" dur="6s" repeatCount="indefinite"/></path>'
        s += f'<line x1="134" y1="14" x2="134" y2="112" stroke="{INK}" stroke-width="2" stroke-dasharray="4 3"/><text x="138" y="22" font-size="9" font-weight="bold" fill="{INK}">rollback</text>'
        s += f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.35;0.4;0.7;0.72" dur="6s" repeatCount="indefinite" calcMode="discrete"/><rect x="22" y="14" width="86" height="28" rx="5" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/><text x="65" y="32" font-size="11" font-weight="bold" text-anchor="middle" fill="{INK}">approve? y/N</text></g>'
    else:  # dishdecoded
        s += f'<rect x="0" y="0" width="200" height="130" fill="url(#light)"/><circle cx="100" cy="65" r="48" fill="{PAPER}" stroke="{INK}" stroke-width="3"/><circle cx="100" cy="65" r="34" fill="none" stroke="{INK}" stroke-width="2"/>'
        s += f'<circle cx="100" cy="65" r="54" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="8 8"><animateTransform attributeName="transform" type="rotate" from="0 100 65" to="360 100 65" dur="8s" repeatCount="indefinite"/></circle>'
        s += f'<path d="M84 52 q16 -14 32 0 q-16 22 -32 0z" fill="{INK}"/><path d="M100 62 v14" stroke="{INK}" stroke-width="3"/>'
        s += f'<path d="M170 20 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 l10 -4z" fill="{INK}"><animate attributeName="opacity" values="1;0;1" dur="1.6s" repeatCount="indefinite" calcMode="discrete"/></path>'
    return s


def loop_strip(current, y=0, w=W, h=56, with_bg=True):
    n = len(STOPS)
    cw = (w - 40) / n
    b = f'<rect x="0" y="{y}" width="{w}" height="{h}" fill="{PAPER}"/>' if with_bg else ""
    for i, (verb, repo, line) in enumerate(STOPS):
        x = 20 + i * cw
        on = repo == current
        b += f'<rect x="{x+2}" y="{y+6}" width="{cw-8}" height="{h-12}" rx="5" fill="{INK if on else PAPER}" stroke="{INK}" stroke-width="2"/>'
        col = PAPER if on else INK
        b += f'<text x="{x+cw/2-2}" y="{y+h/2-3}" font-size="12" font-weight="bold" text-anchor="middle" fill="{col}">0{i+1} {verb}</text>'
        b += f'<text x="{x+cw/2-2}" y="{y+h/2+11}" font-size="10" text-anchor="middle" fill="{col}">{repo}</text>'
        if i < n - 1:
            b += f'<path d="M{x+cw-6} {y+h/2-4} l6 4 l-6 4z" fill="{INK}"/>'
    return b


def repo_banner(repo, tagline, chips):
    stop = next(i for i, s in enumerate(STOPS) if s[1] == repo)
    verb = STOPS[stop][0]
    h = 280
    b = f'<rect width="{W}" height="{h}" fill="url(#dither)"/>'
    inner = f'<g transform="translate(626,48)">{scene(repo)}</g>'
    inner += f'<text x="34" y="86" font-size="40" font-weight="bold" fill="{INK}">{repo}</text>'
    # wrap tagline to ~48 chars
    words, lines, cur = tagline.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > 56:
            lines.append(cur); cur = wd
        else:
            cur = (cur + " " + wd).strip()
    lines.append(cur)
    for i, ln in enumerate(lines[:3]):
        inner += f'<text x="36" y="{114+i*20}" font-size="14" fill="{INK}">{ln}</text>'
    cx = 36
    for c in chips:
        cw = len(c) * 8 + 16
        inner += f'<rect x="{cx}" y="170" width="{cw}" height="22" rx="4" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><text x="{cx+cw/2}" y="185" font-size="12" font-weight="bold" text-anchor="middle" fill="{INK}">{c}</text>'
        cx += cw + 10
    inner += f'<line x1="15" y1="202" x2="{W-17}" y2="202" stroke="{INK}" stroke-width="2"/>'
    inner += f'<g transform="translate(0,0)">{loop_strip(repo, 204, W-34, 44, with_bg=False)}</g>'
    b += window(14, 12, W - 30, h - 28, f"{repo}   ·   stop {stop+1} of 5: {verb}", inner)
    return svg(W, h, b, f"{repo}: {tagline}")


def repo_loop_footer(current):
    h = 110
    b = f'<rect width="{W}" height="{h}" fill="url(#dither)"/>'
    inner = loop_strip(current, 30, W - 60, 56, with_bg=False)
    b += window(14, 8, W - 30, h - 20, "Part of a five-stop loop", inner)
    return svg(W, h, b, f"{current} is one stop in a loop: move, see, know, act, ship")


# ------------------------------------------------------------------ avatar
def avatar(S=500):
    b = f'<rect width="{S}" height="{S}" fill="{PAPER}"/>'
    # dithered "sky" gradient: denser toward the top
    for band, (pat, y0, y1) in enumerate([("dither", 0, 140), ("light", 140, 260), ("gray", 260, 360)]):
        b += f'<rect y="{y0}" width="{S}" height="{y1-y0}" fill="url(#{pat})"/>'
    b += f'<rect y="360" width="{S}" height="{S-360}" fill="{INK}"/>'
    for i in range(0, S, 28):  # checker floor
        b += f'<rect x="{i}" y="388" width="14" height="14" fill="{PAPER}"/><rect x="{i+14}" y="402" width="14" height="14" fill="{PAPER}"/><rect x="{i}" y="430" width="14" height="14" fill="{PAPER}"/><rect x="{i+14}" y="444" width="14" height="14" fill="{PAPER}"/>'
    # Mac body, large, with bevel and shadow
    mx, my, sc = 124, 66, 3.8
    b += f'<rect x="{mx+12}" y="{my+14}" width="{64*sc}" height="{76*sc}" fill="{INK}" opacity="0.9"/>'
    b += happy_mac(mx, my, sc)
    # pixel monogram on the case
    # sparkles
    for (x, y, r) in [(62, 70, 14), (432, 120, 10), (78, 260, 8), (420, 300, 12)]:
        b += f'<path d="M{x} {y-r} l{r/3} {r*2/3} l{r*2/3} {r/3} l-{r*2/3} {r/3} l-{r/3} {r*2/3} l-{r/3} -{r*2/3} l-{r*2/3} -{r/3} l{r*2/3} -{r/3}z" fill="{INK}"/>'
    # arrow cursor pointing at the Mac
    b += f'<g transform="translate(372,318) scale(3)">{cursor(0,0)}</g>'
    return svg(S, S, b, "Aryan Khanna: a smiling retro Macintosh on a dithered desktop").replace('width="100%"', f'width="{S}" height="{S}"')


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


REPOS = {
    "autonomous-bot": ("A ROS 2 robot that maps, localises and navigates on its own, with an IoT dashboard and a swarm auction.", ["ROS 2", "Nav2", "SLAM", "MQTT"]),
    "sentinel": ("Search-and-rescue vision: YOLO11 on RGB and simulated thermal feeds to find people in the dark.", ["YOLO11", "OpenCV", "ONNX"]),
    "finintel": ("A financial RAG system that writes grounded, citation-backed reports from filings.", ["RAG", "GraphRAG", "Claude", "64 tests"]),
    "nexus": ("Network intelligence and an autonomous DevSecOps agent: finds the root cause and fixes the incident.", ["FastAPI", "PostgreSQL", "React", "Claude / NIM"]),
    "dishdecoded": ("Snap a dish or a menu and get its story, allergens and a recipe.", ["Next.js 15", "React 19", "Claude vision"]),
}

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) >= 4 and sys.argv[1] == "--repo":
        name, d = sys.argv[2], sys.argv[3]
        tag, chips = REPOS[name]
        write(os.path.join(d, "assets", "banner.svg"), repo_banner(name, tag, chips))
        write(os.path.join(d, "assets", "loop.svg"), repo_loop_footer(name))
        print("wrote banner + loop for", name)
    else:
        out = os.path.join(here, "..", "assets")
        write(f"{out}/hero.svg", hero())
        write(f"{out}/story.svg", story())
        write(f"{out}/extensions.svg", extensions())
        for n, t in [("01", "STORY"), ("02", "PROJECTS"), ("03", "TOOLKIT"), ("04", "CONTACT")]:
            write(f"{out}/section-{n}.svg", section_bar(n, t))
        for n, l in [("email", "Email"), ("linkedin", "LinkedIn"), ("github", "GitHub")]:
            write(f"{out}/btn-{n}.svg", button(l))
        write(f"{out}/footer.svg", footer())
        write(f"{out}/avatar.svg", avatar())
        print("profile assets written")
