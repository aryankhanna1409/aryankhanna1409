"""Generate experience.svg (timeline) and research.svg (headline numbers) for the profile README."""
import os
from xml.sax.saxutils import escape as esc
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
BG, BLUE, CYAN, VIOLET, INK, MUTED, DIM = "#0b1020", "#5aa2ff", "#67e8f9", "#8b5cf6", "#e6edf3", "#8b98b5", "#25375f"
FONT = "JetBrains Mono, ui-monospace, Menlo, Consolas, monospace"
SANS = "Inter, 'Segoe UI', Helvetica, Arial, sans-serif"
GLOW = '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
NOW = 2026 + 9.7 / 12          # late Oct 2026; open-ended roles run to here

# ---------- experience timeline ----------
# (label, org, start, end or None for present, colour, kind)
ROWS = [("Research Assistant", "Symbiosis Institute of Technology", 2024 + 8/12, None, CYAN, "research"),
        ("Research Intern", "Symbiosis Centre for Applied AI", 2025 + 6/12, 2026, CYAN, "research"),
        ("Club Head · RPA Club", "Dept. of Robotics & Automation", 2025 + 2/12, 2026, VIOLET, "lead"),
        ("Student Coordinator", "Symbiosis Centre of Health Care", 2025 + 7/12, None, VIOLET, "lead"),
        ("Student Coordinator", "SymbITech 2025", 2025 + 6/12, 2025 + 9/12, VIOLET, "lead"),
        ("B.Tech · Robotics & Automation", "SIT Pune", 2023 + 5/12, 2027 + 6/12, BLUE, "edu"),
        ("Diploma · Business Admin", "SIBM Pune", 2024, 2026 + 6/12, BLUE, "edu")]
T0, T1 = 2023 + 4/12, 2027 + 7/12
W, LX, RX, TOP, RH = 960, 330, 930, 70, 40
H = TOP + len(ROWS) * RH + 40
X = lambda t: LX + (t - T0) / (T1 - T0) * (RX - LX)
s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Experience and education timeline"><defs>{GLOW}</defs>'
s += f'<rect width="{W}" height="{H}" rx="12" fill="{BG}" stroke="{DIM}"/><g font-family="{FONT}">'
s += f'<text x="24" y="32" font-size="12" fill="{INK}" font-weight="700" letter-spacing="2">SCENE 05 / TIMELINE</text>'
for i, (lab, c) in enumerate([("research", CYAN), ("leadership", VIOLET), ("education", BLUE)]):
    s += f'<rect x="{W-340+i*110}" y="23" width="10" height="10" rx="2" fill="{c}"/><text x="{W-325+i*110}" y="32" font-size="11" fill="{MUTED}">{lab}</text>'
for yr in range(2024, 2028):
    x = X(yr)
    s += f'<path d="M{x:.1f} {TOP-14}V{H-30}" stroke="{DIM}" stroke-dasharray="2 5"/><text x="{x:.1f}" y="{H-14}" font-size="11" fill="{MUTED}" text-anchor="middle">{yr}</text>'
for i, (role, org, a, b, col, _) in enumerate(ROWS):
    y = TOP + i * RH; end = b or NOW; x0, x1 = X(a), X(end)
    s += f'<text x="24" y="{y+4}" font-size="13" fill="{INK}">{esc(role)}</text><text x="24" y="{y+20}" font-size="10" fill="{MUTED}">{esc(org)}</text>'
    s += f'<rect x="{x0:.1f}" y="{y-6}" width="0" height="14" rx="7" fill="{col}" opacity=".85"><animate attributeName="width" from="0" to="{x1-x0:.1f}" dur="1.1s" begin="{.2+i*.12:.2f}s" fill="freeze"/></rect>'
    if b is None:   # still running: pulse at the leading edge
        s += f'<circle cx="{x1:.1f}" cy="{y+1}" r="5" fill="{col}" filter="url(#glow)" opacity="0"><animate attributeName="opacity" values="0;0;1" keyTimes="0;.9;1" dur="{1.3+i*.12:.2f}s" fill="freeze"/></circle>'
        s += f'<circle cx="{x1:.1f}" cy="{y+1}" r="5" fill="none" stroke="{col}"><animate attributeName="r" values="5;14" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="2s" repeatCount="indefinite"/></circle>'
nx = X(NOW)
s += f'<path d="M{nx:.1f} {TOP-18}V{H-30}" stroke="{CYAN}" stroke-width="1.5"/><text x="{nx:.1f}" y="{TOP-22}" font-size="10" fill="{CYAN}" text-anchor="middle" letter-spacing="2">NOW</text>'
open(f"{OUT}/experience.svg", "w").write(s + "</g></svg>")

# ---------- research numbers ----------
RW, RHt = 960, 190
stats = [("0.99", "R² · reward model", CYAN), ("62.5%", "personalisation gain", BLUE), ("IJCIS", "published 2025", VIOLET), ("5", "listed publications", CYAN)]
r = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {RW} {RHt}" width="100%" role="img" aria-label="Research: R squared 0.99, 62.5% personalisation gain, published in IJCIS 2025, 5 publications"><defs>{GLOW}</defs>'
r += f'<rect width="{RW}" height="{RHt}" rx="12" fill="{BG}" stroke="{DIM}"/>'
r += f'<text x="24" y="32" font-size="12" fill="{INK}" font-weight="700" letter-spacing="2" font-family="{FONT}">RESEARCH / APPLIED ML</text>'
r += f'<text x="{RW-24}" y="32" font-size="11" fill="{MUTED}" text-anchor="end" font-family="{FONT}">figures as reported in the paper</text>'
cw = (RW - 48) / len(stats)
for i, (big, small, col) in enumerate(stats):
    cx = 24 + cw * i + cw / 2
    if i: r += f'<path d="M{24+cw*i:.0f} 62V160" stroke="{DIM}"/>'
    r += (f'<text x="{cx:.0f}" y="120" font-size="54" font-weight="800" fill="{col}" text-anchor="middle" font-family="{SANS}" filter="url(#glow)" opacity="0">{big}'
          f'<animate attributeName="opacity" from="0" to="1" dur=".8s" begin="{i*.25:.2f}s" fill="freeze"/>'
          f'<animate attributeName="y" from="136" to="120" dur=".8s" begin="{i*.25:.2f}s" fill="freeze"/></text>')
    r += f'<text x="{cx:.0f}" y="152" font-size="11" fill="{MUTED}" text-anchor="middle" letter-spacing="1" font-family="{FONT}">{small.upper()}</text>'
open(f"{OUT}/research.svg", "w").write(r + "</svg>")
print("ok")
