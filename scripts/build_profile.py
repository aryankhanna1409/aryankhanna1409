"""Generate terminal.svg, orbit.svg, footer.svg and languages.svg for the profile README."""
import math, os, json, subprocess, sys, urllib.request, random
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
BG, BLUE, CYAN, VIOLET, INK, MUTED, DIM = "#0b1020", "#5aa2ff", "#67e8f9", "#8b5cf6", "#e6edf3", "#8b98b5", "#25375f"
FONT = "JetBrains Mono, ui-monospace, Menlo, Consolas, monospace"
GLOW = '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'

# ---------- terminal ----------
lines = [("$ whoami", INK, "aryan-khanna  // robotics engineer, moving up the stack", CYAN),
         ("$ cat now.txt", INK, "sentinel · autonomous-bot · finintel", CYAN),
         ("$ ls skills/", INK, "ros2/  perception/  rag/  embedded/  data/", CYAN),
         ("$ brew status", INK, "coffee: nerd-level · bugs: negotiable", CYAN)]
tw, th = 960, 70 + len(lines) * 56
t = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {tw} {th}" width="100%" role="img" aria-label="Terminal intro"><defs>{GLOW}</defs>'
t += f'<rect width="{tw}" height="{th}" rx="12" fill="{BG}" stroke="{DIM}"/><rect width="{tw}" height="34" rx="12" fill="#101a33"/><rect y="20" width="{tw}" height="14" fill="#101a33"/>'
t += "".join(f'<circle cx="{22+i*20}" cy="17" r="6" fill="{c}"/>' for i, c in enumerate(["#f87171", "#fbbf24", "#4ade80"]))
t += f'<text x="{tw/2}" y="22" font-size="12" fill="{MUTED}" text-anchor="middle" font-family="{FONT}">aryan@pune: ~</text><g font-family="{FONT}" font-size="16">'
tcur = 0.4
for i, (cmd, c1, out, c2) in enumerate(lines):
    y = 76 + i * 56; cw, ow = len(cmd) * 9.6, len(out) * 9.6; d1 = len(cmd) * .028; d2 = len(out) * .011
    t += f'<clipPath id="a{i}"><rect x="24" y="{y-18}" width="0" height="26"><animate attributeName="width" from="0" to="{cw+4:.0f}" dur="{d1:.2f}s" begin="{tcur:.2f}s" fill="freeze"/></rect></clipPath>'
    t += f'<text x="24" y="{y}" fill="{CYAN}" clip-path="url(#a{i})">{cmd}</text>'
    tcur += d1 + .15
    t += f'<clipPath id="b{i}"><rect x="24" y="{y+6}" width="0" height="26"><animate attributeName="width" from="0" to="{ow+4:.0f}" dur="{d2:.2f}s" begin="{tcur:.2f}s" fill="freeze"/></rect></clipPath>'
    t += f'<text x="24" y="{y+26}" fill="{INK}" clip-path="url(#b{i})">{out}</text>'
    tcur += d2 + .2
t += f'<rect x="24" y="{th-26}" width="10" height="18" fill="{CYAN}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect></g></svg>'
open(f"{OUT}/terminal.svg", "w").write(t)

# ---------- orbit ----------
OW, OH, cx, cy = 960, 420, 480, 210
rings = [(80, 22, ["ROS 2", "YOLO11", "PyTorch"], 22, BLUE), (135, 28, ["OpenCV", "Nav2", "Jetson", "Arduino", "C++"], 34, CYAN),
         (190, 34, ["Python", "SQL", "RAG", "React", "Streamlit", "Git", "Gym/PPO"], 48, VIOLET)]
o = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {OW} {OH}" width="100%" role="img" aria-label="Skills orbit"><defs>{GLOW}<radialGradient id="core"><stop offset="0" stop-color="#2a4fb0"/><stop offset="1" stop-color="{BG}"/></radialGradient></defs>'
o += f'<rect width="{OW}" height="{OH}" rx="14" fill="{BG}" stroke="{DIM}"/>'
random.seed(11); o += "".join(f'<circle cx="{random.uniform(0,OW):.0f}" cy="{random.uniform(0,OH):.0f}" r="{random.choice([.6,1,1.4])}" fill="{INK}" opacity="0"><animate attributeName="opacity" values="0;.8;0" dur="{random.uniform(3,7):.1f}s" begin="{random.uniform(0,5):.1f}s" repeatCount="indefinite"/></circle>' for _ in range(80))
for r, _, _, _, col in rings: o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-opacity=".35" stroke-dasharray="2 6"/>'
o += f'<circle cx="{cx}" cy="{cy}" r="46" fill="url(#core)" filter="url(#glow)"/><circle cx="{cx}" cy="{cy}" r="46" fill="none" stroke="{CYAN}" stroke-opacity=".6"><animate attributeName="r" values="46;62" dur="3s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0" dur="3s" repeatCount="indefinite"/></circle>'
o += f'<text x="{cx}" y="{cy+5}" font-size="14" font-weight="700" fill="{INK}" text-anchor="middle" font-family="{FONT}" letter-spacing="2">STACK</text>'
for ri, (r, h, names, dur, col) in enumerate(rings):
    dirn = 1 if ri % 2 == 0 else -1; sweep = f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="{360*dirn} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'
    o += f'<g>{sweep}'
    for i, n in enumerate(names):
        a = i / len(names) * 2 * math.pi; x, y = cx + r * math.cos(a), cy + r * math.sin(a); w = len(n) * 8 + 22
        o += f'<g transform="translate({x:.1f},{y:.1f})"><g><animateTransform attributeName="transform" type="rotate" from="0" to="{-360*dirn}" dur="{dur}s" repeatCount="indefinite"/>'
        o += f'<rect x="{-w/2:.0f}" y="-13" width="{w:.0f}" height="26" rx="13" fill="{BG}" stroke="{col}" stroke-width="1.5" filter="url(#glow)"/><text y="4" font-size="12" fill="{INK}" text-anchor="middle" font-family="{FONT}">{n}</text></g></g>'
    o += '</g>'
open(f"{OUT}/orbit.svg", "w").write(o + "</svg>")

# ---------- footer wave ----------
FW, FH = 960, 120
f = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {FW} {FH}" width="100%" aria-hidden="true"><defs><linearGradient id="w" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient></defs>'
for k, (amp, dur, op) in enumerate([(18, 9, .25), (14, 7, .4), (10, 5, .7)]):
    p1 = "M0 60 " + " ".join(f"Q{x+60} {60-amp} {x+120} 60 T{x+240} 60" for x in range(0, FW + 240, 240))
    p2 = "M0 60 " + " ".join(f"Q{x+60} {60+amp} {x+120} 60 T{x+240} 60" for x in range(0, FW + 240, 240))
    f += f'<path d="{p1} V{FH} H0Z" fill="url(#w)" opacity="{op*.32}"><animate attributeName="d" values="{p1} V{FH} H0Z;{p2} V{FH} H0Z;{p1} V{FH} H0Z" dur="{dur}s" repeatCount="indefinite"/></path>'
open(f"{OUT}/footer.svg", "w").write(f + "</svg>")

# ---------- languages ----------
REPOS = ["nexus-ai", "sentinel", "autonomous-bot", "finintel", "style-transfer-cnn", "overthinkers-assistant", "one-click-crave", "kinematics-calculator",
         "fakespotter", "auto_wordle", "murdle", "SnackSave", "credit-card"]
def langs():
    tot = {}
    tok = os.environ.get("GITHUB_TOKEN")
    for r in REPOS:
        try:
            d = json.loads(subprocess.run(["gh", "api", f"repos/aryankhanna1409/{r}/languages"], capture_output=True, text=True, check=True).stdout)
        except Exception:
            continue
        for k, v in d.items():
            if k != 'Jupyter Notebook': tot[k] = tot.get(k, 0) + v   # notebook bytes are mostly embedded outputs
    return tot
data = langs()
COL = {"Python": "#5aa2ff", "Jupyter Notebook": "#8b5cf6", "C++": "#67e8f9", "C": "#34d399", "Kotlin": "#a78bfa", "JavaScript": "#fbbf24", "HTML": "#f472b6", "CMake": "#34d399", "CSS": "#60a5fa", "Shell": "#4ade80"}
if data:
    top = sorted(data.items(), key=lambda kv: -kv[1])[:7]; total = sum(v for _, v in top)
    LW, LH = 960, 150 + 0; x = 24; bars = ""; leg = ""
    for i, (k, v) in enumerate(top):
        w = (LW - 48) * v / total; c = COL.get(k, ["#5aa2ff", "#8b5cf6", "#67e8f9", "#a78bfa", "#fbbf24", "#f472b6", "#34d399"][i % 7])
        bars += f'<rect x="{x:.1f}" y="50" width="0" height="18" fill="{c}"><animate attributeName="width" from="0" to="{max(w-2,1):.1f}" dur="1.2s" begin="{i*.15:.2f}s" fill="freeze"/></rect>'
        lx = 24 + (i % 4) * 232; ly = 100 + (i // 4) * 26
        leg += f'<circle cx="{lx}" cy="{ly}" r="6" fill="{c}"/><text x="{lx+14}" y="{ly+4}" font-size="12" fill="{INK}">{k} <tspan fill="{MUTED}">{100*v/total:.1f}%</tspan></text>'
        x += w
    open(f"{OUT}/languages.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LW} {LH}" width="100%" role="img" aria-label="Language mix"><rect width="{LW}" height="{LH}" rx="12" fill="{BG}" stroke="{DIM}"/><g font-family="{FONT}"><text x="24" y="30" font-size="12" fill="{INK}" font-weight="700" letter-spacing="2">LANGUAGE MIX</text><text x="{LW-24}" y="30" font-size="11" fill="{CYAN}" text-anchor="end">across {len(REPOS)} repositories · notebooks excluded</text>{bars}{leg}</g></svg>')
    print("langs", top)
print("ok")
