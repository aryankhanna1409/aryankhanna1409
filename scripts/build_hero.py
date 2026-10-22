"""One-off generator for assets/hero.svg (LiDAR scan banner) and assets/pipeline.svg."""
import math, random, os
random.seed(7)
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
ORANGE, INK, BG = "#ff7a2f", "#e9edf2", "#06080b"
FONT = "JetBrains Mono, ui-monospace, Menlo, Consolas, monospace"
SWEEP = 7.0

# ---------------- hero ----------------
W, H, CX, CY, R = 960, 340, 735, 170, 150
pts = []
def add(x, y, kind="s"): pts.append((x, y, kind))
for a in range(-200, 20, 2):                      # curved far wall with gaps
    if 100 < a % 360 < 118 or -120 < a < -105: continue
    r = R * 0.93 + random.uniform(-3, 3)
    add(CX + r * math.cos(math.radians(a)), CY + r * math.sin(math.radians(a)))
for i in range(26):                               # box obstacle
    t = i / 25
    add(CX - 95 + 55 * t, CY + 40); add(CX - 95, CY + 40 - 38 * t); add(CX - 40, CY + 40 - 38 * t)
for i in range(14): add(CX + 40 + 52 * i / 13, CY - 78 + random.uniform(-2, 2))     # shelf
for i in range(10): add(CX + 40 + random.uniform(-2, 2), CY - 78 + 40 * i / 9)
person = []
px, py = CX + 55, CY + 52                         # a person (head + torso + legs)
for a in range(0, 360, 30): person.append((px + 7 * math.cos(math.radians(a)), py - 40 + 7 * math.sin(math.radians(a))))
for i in range(9):
    person += [(px - 9, py - 30 + i * 3.4), (px + 9, py - 30 + i * 3.4)]
for i in range(6): person += [(px - 5, py - 3 + i * 3), (px + 5, py - 3 + i * 3)]
for i in range(30): add(CX + random.uniform(-130, 130), CY + random.uniform(-130, 130)) if math.hypot(pts[-1][0]-CX, pts[-1][1]-CY) < R else None

def ang(x, y): return math.degrees(math.atan2(y - CY, x - CX)) % 360
def dot(x, y, col, r):
    t = ang(x, y) / 360 * SWEEP
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;0.55;0" keyTimes="0;0.02;0.45;1" dur="{SWEEP}s" begin="{t:.2f}s" repeatCount="indefinite"/></circle>')
dots = "".join(dot(x, y, INK, 1.6) for x, y, _ in pts if math.hypot(x - CX, y - CY) < R)
pdots = "".join(dot(x, y, ORANGE, 2.0) for x, y in person)
tp = ang(px, py - 20) / 360 * SWEEP
box = (f'<g opacity="0"><rect x="{px-24}" y="{py-56}" width="48" height="66" fill="none" stroke="{ORANGE}" stroke-width="1.5"/>'
       f'<text x="{px-24}" y="{py-62}" font-size="9" fill="{ORANGE}" font-family="{FONT}">PERSON 0.91</text>'
       f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.03;0.7;1" dur="{SWEEP}s" begin="{tp:.2f}s" repeatCount="indefinite"/></g>')
rings = "".join(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="#1b2430" stroke-width="1"/>' for r in (50, 100, 150))
cross = f'<path d="M{CX-R} {CY}H{CX+R}M{CX} {CY-R}V{CY+R}" stroke="#141b24"/>'
wedges = ""
for i in range(14):                               # trailing glow, fading
    a0, a1 = -4 * (i + 1), -4 * i
    p = lambda a: (CX + R * math.cos(math.radians(a)), CY + R * math.sin(math.radians(a)))
    (x0, y0), (x1, y1) = p(a0), p(a1)
    wedges += f'<path d="M{CX} {CY}L{x0:.1f} {y0:.1f}A{R} {R} 0 0 1 {x1:.1f} {y1:.1f}Z" fill="{ORANGE}" opacity="{0.34*(1-i/14):.3f}"/>'
sweep = (f'<g><animateTransform attributeName="transform" type="rotate" from="0 {CX} {CY}" to="360 {CX} {CY}" dur="{SWEEP}s" repeatCount="indefinite"/>'
         f'{wedges}<line x1="{CX}" y1="{CY}" x2="{CX+R}" y2="{CY}" stroke="{ORANGE}" stroke-width="1.6"/></g>')
grid = "".join(f'<path d="M{x} 0V{H}" stroke="#0c1118"/>' for x in range(0, W, 40)) + "".join(f'<path d="M0 {y}H{W}" stroke="#0c1118"/>' for y in range(0, H, 40))
brackets = "".join(f'<path d="{d}" fill="none" stroke="{ORANGE}" stroke-width="2"/>' for d in
    ("M14 34V14H34", f"M{W-34} 14H{W-14}V34", f"M14 {H-34}V{H-14}H34", f"M{W-34} {H-14}H{W-14}V{H-34}"))
hero = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Aryan Khanna: Robotics, AI, Software">
<rect width="{W}" height="{H}" fill="{BG}"/>{grid}{brackets}
<g font-family="{FONT}">
<text x="52" y="82" font-size="11" fill="#7d8896" letter-spacing="3">SCENE 01 / LIDAR SWEEP</text>
<text x="50" y="152" font-size="58" font-weight="800" fill="{INK}" font-family="Inter, 'Segoe UI', Helvetica, Arial, sans-serif" letter-spacing="1">ARYAN
<animate attributeName="opacity" from="0" to="1" dur="0.9s" fill="freeze"/></text>
<text x="50" y="214" font-size="58" font-weight="800" fill="{INK}" font-family="Inter, 'Segoe UI', Helvetica, Arial, sans-serif" letter-spacing="1">KHANNA
<animate attributeName="opacity" from="0" to="1" dur="0.9s" begin="0.3s" fill="freeze"/></text>
<text x="52" y="250" font-size="15" fill="{ORANGE}" letter-spacing="4">ROBOTICS / AI / SOFTWARE</text>
<text x="52" y="290" font-size="11" fill="#7d8896">sense → perceive → plan → act → learn</text>
<circle cx="{W-150}" cy="40" r="4" fill="{ORANGE}"><animate attributeName="opacity" values="1;0.15;1" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="{W-140}" y="44" font-size="10" fill="{INK}" letter-spacing="2">LIVE SCAN</text>
<text x="{CX+R}" y="{H-18}" font-size="9" fill="#7d8896" text-anchor="end">r = 12 m · 360°</text>
</g>
{rings}{cross}{dots}{pdots}{box}{sweep}
<circle cx="{CX}" cy="{CY}" r="4" fill="{ORANGE}"/>
</svg>'''
open(f"{OUT}/hero.svg", "w").write(hero)

# ---------------- pipeline ----------------
PW, PH = 960, 170
stages = [("SENSE", "LiDAR · IMU · camera"), ("PERCEIVE", "YOLO11 · RGB-thermal"), ("PLAN", "Nav2 · PSO · SFLA"),
          ("ACT", "PID · differential drive"), ("LEARN", "RF · XGBoost · RAG")]
xs = [96 + i * 192 for i in range(5)]
y = 78
line = f'<path id="rail" d="M{xs[0]} {y}H{xs[-1]}" stroke="#1b2430" stroke-width="2" stroke-dasharray="4 6"/>'
packets = "".join(
    f'<circle r="4" fill="{ORANGE}"><animateMotion dur="6s" begin="{i*1.2}s" repeatCount="indefinite" path="M{xs[0]} {y}H{xs[-1]}"/>'
    f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.92;1" dur="6s" begin="{i*1.2}s" repeatCount="indefinite"/></circle>' for i in range(5))
nodes = ""
for i, ((n, sub), x) in enumerate(zip(stages, xs)):
    nodes += (f'<g><circle cx="{x}" cy="{y}" r="26" fill="{BG}" stroke="{ORANGE}" stroke-width="2"/>'
              f'<circle cx="{x}" cy="{y}" r="26" fill="none" stroke="{ORANGE}" opacity="0"><animate attributeName="r" values="26;44" dur="3s" begin="{i*0.6}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0.6;0" dur="3s" begin="{i*0.6}s" repeatCount="indefinite"/></circle>'
              f'<text x="{x}" y="{y+5}" font-size="13" fill="{ORANGE}" text-anchor="middle" font-weight="700">0{i+1}</text>'
              f'<text x="{x}" y="{y+52}" font-size="13" fill="{INK}" text-anchor="middle" letter-spacing="2" font-weight="700">{n}</text>'
              f'<text x="{x}" y="{y+70}" font-size="10" fill="#7d8896" text-anchor="middle">{sub}</text></g>')
pipe = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="100%" role="img" aria-label="Sense, perceive, plan, act, learn">'
        f'<rect width="{PW}" height="{PH}" rx="10" fill="{BG}"/><g font-family="{FONT}">{line}{packets}{nodes}</g></svg>')
open(f"{OUT}/pipeline.svg", "w").write(pipe)
print("ok")
