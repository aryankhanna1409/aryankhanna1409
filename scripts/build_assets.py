"""Generate the classic-Macintosh style SVGs used by the profile README.

Everything is 1-bit black & white on a dithered desktop, with small SMIL
animations (blinking cursor, typing, marching ants, progress bar).
Run:  python scripts/build_assets.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)
FONT = "Geneva, Monaco, 'Courier New', Courier, monospace"
W = 880
INK, PAPER = "#000", "#fff"

DEFS = f"""<defs>
<pattern id="dither" width="4" height="4" patternUnits="userSpaceOnUse">
<rect width="4" height="4" fill="{PAPER}"/><rect width="2" height="2" fill="{INK}"/><rect x="2" y="2" width="2" height="2" fill="{INK}"/></pattern>
<pattern id="stripes" width="4" height="4" patternUnits="userSpaceOnUse">
<rect width="4" height="4" fill="{PAPER}"/><rect y="1" width="4" height="1" fill="{INK}"/></pattern>
<pattern id="gray" width="2" height="2" patternUnits="userSpaceOnUse">
<rect width="2" height="2" fill="{PAPER}"/><rect width="1" height="1" fill="{INK}"/></pattern>
</defs>"""


def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" '
            f'role="img" aria-label="{label}" shape-rendering="crispEdges" '
            f'font-family="{FONT}">{DEFS}{body}</svg>')


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


def window(x, y, w, h, title, inner=""):
    """Classic window: shadow, border, striped title bar, close box, centred title."""
    tw = len(title) * 8 + 24
    return (
        f'<rect x="{x+3}" y="{y+3}" width="{w}" height="{h}" fill="{INK}"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
        f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="22" fill="url(#stripes)"/>'
        f'<line x1="{x}" y1="{y+24}" x2="{x+w}" y2="{y+24}" stroke="{INK}" stroke-width="2"/>'
        f'<rect x="{x+10}" y="{y+6}" width="13" height="13" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
        f'<rect x="{x+(w-tw)/2}" y="{y+3}" width="{tw}" height="18" fill="{PAPER}"/>'
        f'<text x="{x+w/2}" y="{y+17}" font-size="13" font-weight="bold" text-anchor="middle" fill="{INK}">{title}</text>'
        f'{inner}')


def happy_mac(x, y, s=1.0):
    """Generic compact Mac with a blinking smiley face (drawn from rectangles)."""
    g = f'<g transform="translate({x},{y}) scale({s})">'
    g += f'<rect x="0" y="0" width="64" height="76" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
    g += f'<rect x="8" y="8" width="48" height="38" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
    # eyes (blink)
    for ex in (21, 38):
        g += (f'<rect x="{ex}" y="19" width="4" height="8" fill="{INK}">'
              f'<animate attributeName="height" values="8;8;1;8;8" keyTimes="0;0.9;0.93;0.96;1" dur="4s" repeatCount="indefinite"/>'
              f'<animate attributeName="y" values="19;19;26;19;19" keyTimes="0;0.9;0.93;0.96;1" dur="4s" repeatCount="indefinite"/></rect>')
    g += f'<rect x="31" y="22" width="2" height="8" fill="{INK}"/>'  # nose
    g += f'<path d="M20 35 h4 v3 h16 v-3 h4" fill="none" stroke="{INK}" stroke-width="3"/>'  # smile
    g += f'<rect x="12" y="58" width="30" height="4" fill="{INK}"/>'  # floppy slot
    g += f'<rect x="46" y="56" width="6" height="6" fill="{INK}"/></g>'
    return g


def menubar(items):
    b = f'<rect width="{W}" height="26" fill="{PAPER}"/><line x1="0" y1="26" x2="{W}" y2="26" stroke="{INK}" stroke-width="2"/>'
    b += f'<rect x="14" y="7" width="12" height="13" rx="2" fill="{INK}"/>'  # abstract solid glyph (not a logo)
    x = 44
    for it in items:
        b += f'<text x="{x}" y="18" font-size="13" font-weight="bold" fill="{INK}">{it}</text>'
        x += len(it) * 9 + 18
    b += (f'<text x="{W-16}" y="18" font-size="13" text-anchor="end" fill="{INK}">'
          f'<animate attributeName="opacity" values="1;1;1;1" dur="1s" repeatCount="indefinite"/>Pune, IN</text>')
    return b


# ---------------------------------------------------------------- hero
def hero():
    h = 380
    b = f'<rect width="{W}" height="{h}" fill="url(#dither)"/>' + menubar(["File", "Edit", "View", "Special"])
    inner = happy_mac(64, 100, 1.6)
    inner += f'<text x="210" y="140" font-size="44" font-weight="bold" fill="{INK}">Hello, I\'m Aryan.</text>'
    inner += f'<text x="212" y="172" font-size="16" fill="{INK}">Robotics engineer, moving up the stack to AI + software.</text>'
    # cycling tagline w/ blinking cursor
    lines = ["Sensing  ·  Planning  ·  Learning", "ROS 2  ·  YOLO  ·  RAG  ·  Embedded", "B.Tech Robotics '27  ·  Pune, India"]
    n = len(lines)
    dur = 3 * n
    for i, t in enumerate(lines):
        kt = [0, i / n, i / n + 0.001, (i + 1) / n - 0.001, (i + 1) / n, 1]
        vals = ["0", "0", "1", "1", "0", "0"] if i else ["1", "1", "1", "1", "0", "0"]
        if i == 0:
            kt = [0, 1 / n - 0.001, 1 / n, 1]
            vals = ["1", "1", "0", "0"]
        elif i == n - 1:
            kt = [0, i / n - 0.001, i / n, 1]
            vals = ["0", "0", "1", "1"]
        else:
            kt = [0, i / n - 0.001, i / n, (i + 1) / n - 0.001, (i + 1) / n, 1]
            vals = ["0", "0", "1", "1", "0", "0"]
        inner += (f'<text x="212" y="226" font-size="20" font-weight="bold" fill="{INK}" opacity="0">{t}'
                  f'<animate attributeName="opacity" values="{";".join(vals)}" keyTimes="{";".join(f"{k:.3f}" for k in kt)}" '
                  f'dur="{dur}s" repeatCount="indefinite" calcMode="discrete"/></text>')
    inner += (f'<rect x="212" y="236" width="10" height="3" fill="{INK}">'
              f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" calcMode="discrete"/></rect>')
    # progress bar "Loading projects..."
    inner += f'<text x="212" y="282" font-size="13" fill="{INK}">Loading projects…</text>'
    inner += f'<rect x="212" y="290" width="440" height="16" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    inner += (f'<rect x="214" y="292" width="0" height="12" fill="url(#gray)"><animate attributeName="width" values="0;436;436" '
              f'keyTimes="0;0.85;1" dur="6s" repeatCount="indefinite"/></rect>')
    inner += f'<rect x="214" y="292" width="0" height="12" fill="{INK}" opacity="0.0"/>'
    b += window(48, 56, W - 96, 290, "Aryan Khanna", inner)
    return svg(W, h, b, "Hello, I'm Aryan: retro Macintosh desktop")


# ---------------------------------------------------------------- section bars
def section_bar(n, title):
    h = 40
    b = (f'<rect width="{W}" height="{h}" fill="{PAPER}"/>'
         f'<rect x="2" y="4" width="{W-6}" height="30" fill="{INK}"/>'
         f'<rect x="0" y="2" width="{W-6}" height="30" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
         f'<rect x="1" y="3" width="{W-8}" height="28" fill="url(#stripes)"/>'
         f'<rect x="10" y="9" width="16" height="16" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
    label = f"{n} · {title}"
    tw = len(label) * 9 + 28
    b += f'<rect x="{(W-6-tw)/2}" y="6" width="{tw}" height="22" fill="{PAPER}"/>'
    b += f'<text x="{(W-6)/2}" y="22" font-size="15" font-weight="bold" text-anchor="middle" fill="{INK}">{label}</text>'
    return svg(W, h, b, f"{n} {title}")


# ---------------------------------------------------------------- pipeline
def pipeline():
    h = 140
    steps = ["SENSE", "PERCEIVE", "PLAN", "ACT", "LEARN"]
    bw, gap = 128, 48
    x0 = (W - (len(steps) * bw + (len(steps) - 1) * gap)) / 2
    b = ""
    for i, s in enumerate(steps):
        x = x0 + i * (bw + gap)
        b += f'<rect x="{x+3}" y="43" width="{bw}" height="54" fill="{INK}"/>'
        b += f'<rect x="{x}" y="40" width="{bw}" height="54" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
        b += f'<text x="{x+bw/2}" y="68" font-size="14" font-weight="bold" text-anchor="middle" fill="{INK}">{s}</text>'
        b += f'<text x="{x+bw/2}" y="88" font-size="10" text-anchor="middle" fill="{INK}">0{i+1}</text>'
        if i < len(steps) - 1:
            ax = x + bw + 6
            b += (f'<line x1="{ax}" y1="67" x2="{ax+gap-12}" y2="67" stroke="{INK}" stroke-width="2" stroke-dasharray="6 4">'
                  f'<animate attributeName="stroke-dashoffset" from="20" to="0" dur="0.8s" repeatCount="indefinite"/></line>'
                  f'<path d="M{ax+gap-18} 61 l8 6 l-8 6z" fill="{INK}"/>')
    # feedback loop
    xs, xe = x0 + bw / 2, x0 + 4 * (bw + gap) + bw / 2
    b += (f'<path d="M{xe} 94 v22 H{xs} v-22" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="6 4">'
          f'<animate attributeName="stroke-dashoffset" from="0" to="20" dur="1.2s" repeatCount="indefinite"/></path>')
    b += f'<path d="M{xs-6} 106 l6 -10 l6 10z" fill="{INK}"/>'
    return svg(W, h, b, "Sense, perceive, plan, act, learn loop")


# ---------------------------------------------------------------- buttons
def button(name, label):
    w, h = 200, 46
    b = (f'<rect x="3" y="3" width="{w-5}" height="{h-5}" rx="10" fill="{INK}"/>'
         f'<rect x="1" y="1" width="{w-5}" height="{h-5}" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
         f'<rect x="5" y="5" width="{w-13}" height="{h-13}" rx="7" fill="none" stroke="{INK}" stroke-width="2">'
         f'<animate attributeName="stroke-dasharray" values="0 0;6 4;0 0" dur="3s" repeatCount="indefinite"/></rect>'
         f'<text x="{(w-4)/2}" y="28" font-size="15" font-weight="bold" text-anchor="middle" fill="{INK}">{label}</text>')
    write(f"btn-{name}.svg", svg(w, h, b, label))


# ---------------------------------------------------------------- footer
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


if __name__ == "__main__":
    write("hero.svg", hero())
    for n, t in [("01", "IDENTITY"), ("02", "ENGINEERING"), ("03", "PROJECTS"), ("04", "SYSTEMS"), ("05", "EXPERIENCE"), ("06", "CONTACT")]:
        write(f"section-{n}.svg", section_bar(n, t))
    write("pipeline.svg", pipeline())
    button("email", "Email")
    button("linkedin", "LinkedIn")
    button("github", "GitHub")
    write("footer.svg", footer())
    print("assets written to", os.path.abspath(OUT))
