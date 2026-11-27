"""Generate experience.svg (timeline) and the contact buttons for the profile README."""
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

# ---------- contact buttons (self-hosted so they never depend on a badge service) ----------
ICONS = {
    "email": f'<rect x="-9" y="-6.5" width="18" height="13" rx="2" fill="none" stroke="{CYAN}" stroke-width="1.6"/><path d="M-9 -5.5L0 1.5L9 -5.5" fill="none" stroke="{CYAN}" stroke-width="1.6"/>',
    "linkedin": f'<rect x="-9" y="-9" width="18" height="18" rx="3" fill="none" stroke="{CYAN}" stroke-width="1.6"/><text y="4.5" font-size="11" font-weight="700" fill="{CYAN}" text-anchor="middle" font-family="{SANS}">in</text>',
    "github": f'<circle r="9" fill="none" stroke="{CYAN}" stroke-width="1.6"/><path d="M-3.5 7.5V3.5C-3.5 2-2.5 1.5-1.5 1C-5 0.5-6-1.5-6-4C-6-5.5-5-6.5-5-6.5C-5.5-7.5-5-8.5-5-8.5C-5-8.5-3.5-8.5-2-7C0-7.5 0-7.5 2-7C3.5-8.5 5-8.5 5-8.5C5-8.5 5.5-7.5 5-6.5C5-6.5 6-5.5 6-4C6-1.5 5 0.5 1.5 1C2.5 1.5 3.5 2 3.5 3.5V7.5" fill="none" stroke="{CYAN}" stroke-width="1.2"/>',
}
for key, label in [("email", "EMAIL"), ("linkedin", "LINKEDIN"), ("github", "@ARYANKHANNA1409")]:
    bw = 70 + len(label) * 9.6
    open(f"{OUT}/contact-{key}.svg", "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {bw} 44" width="{bw}" height="44" role="img" aria-label="{label.title()}">'
        f'<rect x="1" y="1" width="{bw-2}" height="42" rx="21" fill="{BG}" stroke="{DIM}" stroke-width="1.5"/>'
        f'<g transform="translate(28,22)">{ICONS[key]}</g>'
        f'<text x="48" y="27" font-size="13" font-weight="700" fill="{INK}" letter-spacing="2" font-family="{FONT}">{label}</text></svg>')
print("ok")
