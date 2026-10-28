"""Generate one animated, on-theme SVG banner per project (and a 1280x640 social preview source)."""
import math, random, os, sys, json
BG, BLUE, CYAN, VIOLET, INK, MUTED, DIM = "#0b1020", "#5aa2ff", "#67e8f9", "#8b5cf6", "#e6edf3", "#8b98b5", "#25375f"
GREEN, RED = "#4ade80", "#f87171"
FONT = "JetBrains Mono, ui-monospace, Menlo, Consolas, monospace"
SANS = "Inter, 'Segoe UI', Helvetica, Arial, sans-serif"
W, H = 960, 260

def an(attr, values, dur, begin=0, extra=""):
    return f'<animate attributeName="{attr}" values="{values}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite" {extra}/>'
def rot(cx, cy, dur, frm=0, to=360, extra=""):
    return f'<animateTransform attributeName="transform" type="rotate" from="{frm} {cx} {cy}" to="{to} {cx} {cy}" dur="{dur}s" repeatCount="indefinite" {extra}/>'

# ---------------- motifs: drawn in a 360x220 box, origin top-left ----------------
def m_sentinel():
    cx, cy, R = 180, 110, 100; random.seed(3); o = ""
    for r in (33, 66, 100): o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{DIM}"/>'
    o += f'<path d="M{cx-R} {cy}H{cx+R}M{cx} {cy-R}V{cy+R}" stroke="#1b2a4d"/>'
    for i in range(34):
        a, r = random.uniform(0, 360), random.uniform(25, 95); x, y = cx+r*math.cos(math.radians(a)), cy+r*math.sin(math.radians(a))
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="1.6" fill="{INK}" opacity="0">{an("opacity","0;1;.5;0",6,a/360*6,"keyTimes=\"0;.02;.45;1\"")}</circle>'
    w = "".join(f'<path d="M{cx} {cy}L{cx+R*math.cos(math.radians(-4*(i+1))):.1f} {cy+R*math.sin(math.radians(-4*(i+1))):.1f}A{R} {R} 0 0 1 {cx+R*math.cos(math.radians(-4*i)):.1f} {cy+R*math.sin(math.radians(-4*i)):.1f}Z" fill="{BLUE}" opacity="{.35*(1-i/12):.3f}"/>' for i in range(12))
    o += f'<g>{rot(cx,cy,6)}{w}<line x1="{cx}" y1="{cy}" x2="{cx+R}" y2="{cy}" stroke="{CYAN}" stroke-width="1.6"/></g>'
    o += f'<g opacity="0"><rect x="{cx+30}" y="{cy-6}" width="30" height="44" fill="none" stroke="{CYAN}" stroke-width="1.5"/><text x="{cx+30}" y="{cy-11}" font-size="8" fill="{CYAN}">PERSON 0.91</text>{an("opacity","0;1;1;0",6,1.0,"keyTimes=\"0;.03;.7;1\"")}</g>'
    return o
def m_bot():
    o = ""; cs = 28
    for gx in range(12):
        for gy in range(7): o += f'<rect x="{gx*cs}" y="{gy*cs+5}" width="{cs-2}" height="{cs-2}" rx="3" fill="#101a33"/>'
    for gx, gy in [(3,1),(3,2),(3,3),(6,3),(6,4),(6,5),(8,0),(8,1),(9,4),(10,4)]: o += f'<rect x="{gx*cs}" y="{gy*cs+5}" width="{cs-2}" height="{cs-2}" rx="3" fill="#1e2b52"/>'
    p = "M15 20 L15 80 L75 80 L75 140 L165 140 L165 50 L225 50 L225 110 L315 110 L315 170"
    o += f'<path d="{p.replace("L","L")}" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="6 5"><animate attributeName="stroke-dashoffset" from="0" to="-22" dur="1s" repeatCount="indefinite"/></path>'
    o += f'<circle cx="315" cy="170" r="8" fill="none" stroke="{CYAN}" stroke-width="2"><animate attributeName="r" values="6;16" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="2s" repeatCount="indefinite"/></circle><circle cx="315" cy="170" r="4" fill="{CYAN}"/>'
    o += f'<g><animateMotion dur="7s" repeatCount="indefinite" path="{p}"/><circle r="8" fill="{BG}" stroke="{CYAN}" stroke-width="2"/><circle cx="3" r="2.5" fill="{CYAN}"/></g>'
    return f'<g transform="translate(0,5)">{o}</g>'
def m_finintel():
    random.seed(5); N = [(70,60),(160,35),(255,70),(120,120),(220,135),(310,115),(60,170),(170,190),(285,185),(180,95)]
    E = [(0,1),(1,2),(0,3),(3,9),(9,4),(2,5),(4,5),(3,6),(7,4),(7,3),(4,8),(1,9),(5,8)]
    o = "".join(f'<path id="e{i}" d="M{N[a][0]} {N[a][1]}L{N[b][0]} {N[b][1]}" stroke="{DIM}" stroke-width="1.3"/>' for i,(a,b) in enumerate(E))
    o += "".join(f'<circle r="2.6" fill="{CYAN}"><animateMotion dur="{2+i%3}s" begin="{i*.4}s" repeatCount="indefinite" path="M{N[a][0]} {N[a][1]}L{N[b][0]} {N[b][1]}"/></circle>' for i,(a,b) in enumerate(E))
    for i,(x,y) in enumerate(N): o += f'<circle cx="{x}" cy="{y}" r="9" fill="{BG}" stroke="{BLUE if i%3 else VIOLET}" stroke-width="2"><animate attributeName="r" values="8;11;8" dur="{3+i%3}s" begin="{i*.3}s" repeatCount="indefinite"/></circle>'
    for (x,y),t in zip([N[9],N[0],N[5]],["RAG","10-K","8-K"]): o += f'<text x="{x}" y="{y+22}" font-size="9" fill="{MUTED}" text-anchor="middle">{t}</text>'
    return o
def m_style():
    o = f'<defs><filter id="bl"><feGaussianBlur stdDeviation="16"/></filter></defs><g filter="url(#bl)">'
    for i,(c,x,y,r) in enumerate([(BLUE,110,90,60),(VIOLET,230,120,64),(CYAN,170,70,44),("#f472b6",250,60,38),(BLUE,120,160,40)]):
        o += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity=".75">{an("cx",f"{x};{x+40};{x-30};{x}",9+i,i)}{an("cy",f"{y};{y-30};{y+30};{y}",11+i,i)}</circle>'
    o += '</g>'
    for k,(x,lab) in enumerate([(20,"content"),(250,"style")]): o += f'<rect x="{x}" y="165" width="80" height="40" rx="6" fill="none" stroke="{MUTED}" stroke-dasharray="3 3"/><text x="{x+40}" y="190" font-size="10" fill="{MUTED}" text-anchor="middle">{lab}</text>'
    return o
def m_tree():
    o = ""; root = (30,110); opts = [(150,50),(150,170)]
    leaves = {0:[(290,15,GREEN),(290,55,GREEN),(290,95,RED)], 1:[(290,130,GREEN),(290,170,RED),(290,205,RED)]}
    def edge(x1,y1,x2,y2,col,d):
        return f'<path d="M{x1} {y1}C{(x1+x2)/2} {y1} {(x1+x2)/2} {y2} {x2} {y2}" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="200" stroke-dashoffset="200"><animate attributeName="stroke-dashoffset" values="200;0;0;200" keyTimes="0;.25;.85;1" dur="8s" begin="{d}s" repeatCount="indefinite"/></path>'
    o += f'<rect x="{root[0]-26}" y="{root[1]-14}" width="86" height="28" rx="8" fill="#16244d" stroke="{BLUE}"/><text x="{root[0]+17}" y="{root[1]+4}" font-size="10" fill="{INK}" text-anchor="middle">tea or coffee</text>'
    for i,(x,y) in enumerate(opts):
        o += edge(root[0]+60,root[1],x-30,y,BLUE,0)+f'<rect x="{x-30}" y="{y-13}" width="60" height="26" rx="8" fill="#16244d" stroke="{BLUE}"/><text x="{x}" y="{y+4}" font-size="10" fill="{INK}" text-anchor="middle">{["coffee","tea"][i]}</text>'
        for j,(lx,ly,c) in enumerate(leaves[i]):
            o += edge(x+30,y,lx-6,ly,c,1+j*.3)+f'<circle cx="{lx}" cy="{ly}" r="6" fill="{c}" opacity="0">{an("opacity","0;0;1;1;0",8,1+j*.3,"keyTimes=\"0;.2;.3;.85;1\"")}</circle>'
    return o
def m_crave():
    o = f'<g transform="translate(180,110)"><g>{rot(0,0,6)}<rect x="-44" y="-44" width="88" height="88" rx="16" fill="#16244d" stroke="{BLUE}" stroke-width="2"/>'
    for px,py in [(-22,-22),(22,-22),(0,0),(-22,22),(22,22)]: o += f'<circle cx="{px}" cy="{py}" r="6" fill="{CYAN}"/>'
    o += '</g></g>'
    for i in range(5): o += f'<g transform="translate(180,110)"><g>{rot(0,0,8+i*2,i*72,i*72+360)}<circle cx="{95+i*6}" cy="0" r="{7-i*.6}" fill="{[BLUE,VIOLET,CYAN,"#f472b6",BLUE][i]}"/></g></g>'
    return o
def m_kin():
    bx, by = 60, 170; o = f'<path d="M{bx} {by}m-130 0a130 130 0 0 1 260 0" fill="none" stroke="{DIM}" stroke-dasharray="3 5" transform="translate(70 0)"/>'
    o += f'<rect x="{bx-22}" y="{by}" width="44" height="12" rx="3" fill="{DIM}"/>'
    o += f'<g transform="translate({bx},{by})"><g>{an_tr(-70,-20,0,5)}<line x2="110" stroke="{BLUE}" stroke-width="8" stroke-linecap="round"/><circle r="8" fill="{BG}" stroke="{CYAN}" stroke-width="2.5"/><g transform="translate(110,0)"><g>{an_tr(20,70,0,5)}<line x2="95" stroke="{CYAN}" stroke-width="6" stroke-linecap="round"/><circle r="6" fill="{BG}" stroke="{CYAN}" stroke-width="2.5"/><circle cx="95" r="5" fill="{VIOLET}"/></g></g></g></g>'
    return o
def an_tr(a, b, _c, dur):
    return f'<animateTransform attributeName="transform" type="rotate" values="{a};{b};{a}" dur="{dur}s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" keyTimes="0;.5;1"/>'
def m_fake():
    o = ""; rows = [("authentic?", .78, CYAN), ("legit batch", .55, CYAN), ("total scam", .86, VIOLET), ("QC pics", .4, CYAN), ("worth it", .65, CYAN)]
    for i,(t,v,c) in enumerate(rows):
        y = 12+i*40; o += f'<rect x="10" y="{y}" width="340" height="30" rx="10" fill="#101a33"/><text x="24" y="{y+19}" font-size="11" fill="{INK}">{t}</text><rect x="170" y="{y+11}" width="160" height="8" rx="4" fill="#1b2a4d"/><rect x="170" y="{y+11}" width="0" height="8" rx="4" fill="{c}"><animate attributeName="width" values="0;{v*160:.0f};{v*160:.0f};0" keyTimes="0;.3;.85;1" dur="6s" begin="{i*.5}s" repeatCount="indefinite"/></rect>'
        o += f'<text x="335" y="{y+19}" font-size="9" fill="{c}" text-anchor="end">{"POS" if c==CYAN else "NEG"}</text>'
    return o
def m_wordle():
    o = ""; cols = [CYAN, "#2a3350", VIOLET, CYAN, "#2a3350"]
    for rrow, word in enumerate(["CRANE", "SOLVE"]):
        for i,ch in enumerate(word):
            x, y = 10+i*68, 30+rrow*84; c = cols[(i+rrow*2)%5]
            o += f'<g transform="translate({x+30},{y+30})"><g><animateTransform attributeName="transform" type="scale" values="1 1;1 0.05;1 1;1 1" keyTimes="0;.12;.24;1" dur="5s" begin="{i*.25+rrow*1.2}s" repeatCount="indefinite"/><rect x="-30" y="-30" width="60" height="60" rx="8" fill="{c}"/><text y="10" font-size="28" font-weight="800" fill="{BG if c==CYAN else INK}" text-anchor="middle" font-family="{SANS}">{ch}</text></g></g>'
    return o
def m_murdle():
    o = ""; random.seed(2)
    for i in range(6):
        y = 20+i*30; o += f'<rect x="20" y="{y}" width="{random.randint(150,300)}" height="12" rx="6" fill="#16244d"/>'
    o += f'<text x="330" y="40" font-size="26" fill="{VIOLET}" opacity=".7">?</text>'
    o += f'<g><animateMotion dur="6s" repeatCount="indefinite" path="M60 50 C 160 20 260 80 300 70 C 200 150 120 140 60 50"/><circle r="30" fill="#67e8f91a" stroke="{CYAN}" stroke-width="4"/><line x1="21" y1="21" x2="48" y2="48" stroke="{CYAN}" stroke-width="7" stroke-linecap="round"/></g>'
    return o
def m_snack():
    o = f'<rect x="110" y="0" width="140" height="215" rx="22" fill="#0f1730" stroke="{BLUE}" stroke-width="2"/><rect x="160" y="8" width="40" height="6" rx="3" fill="{DIM}"/>'
    for i,(c,t) in enumerate([(CYAN,"coffee"),(VIOLET,"snack"),(BLUE,"cab"),(CYAN,"boba")]):
        y = 30+i*44; o += f'<rect x="124" y="{y}" width="112" height="34" rx="8" fill="#16244d"/><text x="134" y="{y+14}" font-size="9" fill="{INK}">{t}</text><rect x="134" y="{y+21}" width="92" height="5" rx="2.5" fill="#1b2a4d"/><rect x="134" y="{y+21}" width="20" height="5" rx="2.5" fill="{c}"><animate attributeName="width" values="20;{60+i*8};{60+i*8};20" keyTimes="0;.4;.85;1" dur="5s" begin="{i*.4}s" repeatCount="indefinite"/></rect>'
    for i in range(7): o += f'<circle cx="{30+i*48}" cy="-10" r="6" fill="{CYAN}" opacity="0"><animate attributeName="cy" values="-10;220" dur="{3+i%3}s" begin="{i*.5}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.9;.9;0" dur="{3+i%3}s" begin="{i*.5}s" repeatCount="indefinite"/></circle>' if not 100 < 30+i*48 < 260 else ""
    return o
def m_card():
    o = f'<defs><linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><clipPath id="cc"><rect x="40" y="25" width="280" height="170" rx="18"/></clipPath><linearGradient id="cg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1e3a8a"/><stop offset="1" stop-color="#5b21b6"/></linearGradient></defs>'
    o += f'<g><animateTransform attributeName="transform" type="rotate" values="-3 180 110;3 180 110;-3 180 110" dur="6s" repeatCount="indefinite"/><rect x="40" y="25" width="280" height="170" rx="18" fill="url(#cg)" stroke="{BLUE}"/><rect x="62" y="62" width="44" height="32" rx="6" fill="{CYAN}" opacity=".85"/><text x="62" y="140" font-size="17" fill="{INK}" letter-spacing="3">4000 •••• •••• 2026</text><text x="62" y="172" font-size="10" fill="{MUTED}">REWARD POINTS</text>'
    o += f'<g clip-path="url(#cc)"><rect x="-80" y="25" width="80" height="170" fill="url(#sh)" transform="skewX(-20)"><animate attributeName="x" values="-80;420" dur="3.2s" repeatCount="indefinite"/></rect></g></g>'
    return o
def m_nexus():
    o = f'<rect x="0" y="10" width="360" height="200" rx="10" fill="#101a33"/>'
    o += "".join(f'<path d="M20 {y}H340" stroke="#1b2a4d"/>' for y in (50, 100, 150, 190))
    o += f'<path d="M150 30V195" stroke="#fbbf24" stroke-opacity=".6" stroke-dasharray="3 4"/><text x="150" y="25" font-size="8" fill="#fbbf24" text-anchor="middle">DEPLOY 2.4.1</text>'
    o += f'<path d="M262 30V195" stroke="{GREEN}" stroke-opacity=".6" stroke-dasharray="3 4"/><text x="262" y="25" font-size="8" fill="{GREEN}" text-anchor="middle">ROLLBACK</text>'
    draw = lambda d, col, b: f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="320" stroke-dashoffset="320"><animate attributeName="stroke-dashoffset" values="320;0;0;320" keyTimes="0;.3;.9;1" dur="8s" begin="{b}s" repeatCount="indefinite"/></path>'
    o += draw("M20 180 L60 178 L100 181 L150 179 C175 175 200 110 230 70 L262 62", RED, 0)
    o += draw("M262 62 C272 120 282 176 300 179 L340 180", GREEN, 2.4)
    o += f'<g opacity="0"><rect x="196" y="120" width="110" height="34" rx="8" fill="{BG}" stroke="{CYAN}"/><text x="251" y="134" font-size="9" fill="{INK}" text-anchor="middle">roll back pgw-1?</text><text x="251" y="147" font-size="9" fill="{CYAN}" text-anchor="middle">[y/N] y</text>{an("opacity","0;0;1;1;0;0",8,0,"keyTimes=\"0;.22;.25;.32;.35;1\"")}</g>'
    o += f'<g opacity="0"><rect x="186" y="48" width="34" height="18" rx="9" fill="none" stroke="{VIOLET}"/><text x="203" y="60" font-size="9" fill="{VIOLET}" text-anchor="middle">E3</text>{an("opacity","0;0;1;1;0",8,0,"keyTimes=\"0;.18;.22;.88;1\"")}</g>'
    return o
def m_dish():
    o = f'<path d="M78 40V28H96M264 28H282V40M282 182V194H264M96 194H78V182" fill="none" stroke="{CYAN}" stroke-width="2"/>'
    o += f'<line x1="84" x2="276" y1="40" y2="40" stroke="{CYAN}" stroke-opacity=".7"><animate attributeName="y1" values="40;188;40" dur="4s" repeatCount="indefinite"/><animate attributeName="y2" values="40;188;40" dur="4s" repeatCount="indefinite"/></line>'
    for i, x in enumerate((150, 180, 210)):
        o += f'<path d="M{x} 104c-8-10 8-16 0-26s8-16 0-24" fill="none" stroke="{MUTED}" stroke-width="2" stroke-linecap="round" opacity="0">{an("opacity","0;.8;0",3,i*.7)}<animateTransform attributeName="transform" type="translate" values="0 6;0 -6" dur="3s" begin="{i*.7}s" repeatCount="indefinite"/></path>'
    o += f'<path d="M96 118A84 62 0 0 0 264 118Z" fill="#16244d" stroke="{BLUE}" stroke-width="2"/><ellipse cx="180" cy="118" rx="84" ry="12" fill="#101a33" stroke="{BLUE}" stroke-width="2"/>'
    o += "".join(f'<path d="M{118+k*14} 118q4 -6 8 0t8 0" fill="none" stroke="{CYAN}" stroke-width="1.6"/>' for k in range(9))
    o += f'<rect x="150" y="176" width="60" height="8" rx="4" fill="{DIM}"/>'
    for i, (t, y, c) in enumerate([("khao soi · 0.86", 46, CYAN), ("gluten · egg · fish?", 72, VIOLET), ("umami 4 · spicy 3", 98, BLUE)]):
        w = 18 + len(t) * 6.4
        kt = f'keyTimes="0;{.15+i*.12:.2f};{.2+i*.12:.2f};.9;1"'
        o += f'<g opacity="0"><rect x="{350-w:.0f}" y="{y-14}" width="{w:.0f}" height="20" rx="10" fill="{BG}" stroke="{c}"/><text x="{350-w/2:.0f}" y="{y}" font-size="9.5" fill="{INK}" text-anchor="middle">{t}</text>{an("opacity","0;0;1;1;0",6,0,kt)}</g>'
    return o
def m_og():
    pts = [(180, 24), (282, 78), (244, 142), (116, 142), (78, 78)]
    labels = ["OBSERVE", "ANALYZE", "ACT", "VERIFY", "CLOSE"]
    loop = "M" + " L".join(f"{x} {y}" for x, y in pts) + " Z"
    o = f'<path d="{loop}" fill="none" stroke="{DIM}" stroke-width="1.5"/>'
    o += f'<path d="{loop}" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="8 8"><animate attributeName="stroke-dashoffset" from="0" to="-32" dur="1.4s" repeatCount="indefinite"/></path>'
    for i, ((x, y), t) in enumerate(zip(pts, labels)):
        c = "#fbbf24" if t == "ACT" else (GREEN if t == "CLOSE" else BLUE)
        o += f'<circle cx="{x}" cy="{y}" r="15" fill="{BG}" stroke="{c}" stroke-width="2">{an("r", "15;18;15;15", 8, i * 1.6, "keyTimes=\"0;.06;.12;1\"")}</circle>'
        o += f'<text x="{x}" y="{y + (-21 if y < 100 else 30)}" font-size="9" fill="{MUTED}" text-anchor="middle" letter-spacing="1">{t}</text>'
    o += f'<g><animateMotion dur="8s" repeatCount="indefinite" path="{loop}"/><circle r="5" fill="{CYAN}"/></g>'
    o += f'<text x="180" y="84" font-size="10" fill="{INK}" text-anchor="middle">INC-2026-001</text><text x="180" y="100" font-size="9" fill="{CYAN}" text-anchor="middle">RCA 85% · 12 tool calls</text>'
    o += f'<g opacity="0"><rect x="262" y="100" width="92" height="20" rx="10" fill="{BG}" stroke="#fbbf24"/><text x="308" y="114" font-size="9" fill="#fbbf24" text-anchor="middle">approval gate</text>{an("opacity", "0;0;1;1;0;0", 8, 0, "keyTimes=\"0;.38;.42;.55;.58;1\"")}</g>'
    for k in range(6):
        x = 42 + k * 48
        o += f'<g opacity="0"><rect x="{x}" y="190" width="34" height="16" rx="3" fill="#16244d" stroke="{VIOLET}"/><text x="{x + 17}" y="201" font-size="8" fill="{INK}" text-anchor="middle">#{k + 1}</text>{an("opacity", "0;0;1;1;0", 8, 0, f"keyTimes=\"0;{.1 + k * .12:.2f};{.12 + k * .12:.2f};.95;1\"")}</g>'
        if k: o += f'<path d="M{x - 14} 198H{x}" stroke="{VIOLET}" stroke-opacity=".7"/>'
    return o
MOTIFS = { "dishdecoded": ("DishDecoded", "Snap a dish or menu: what it is and how to make it", ["Next.js", "TypeScript", "Claude vision", "Zod"], m_dish),
 "nexus-og": ("nexus-og", "The full original: C analytics, AI RCA, a gated agent", ["C11", "FastAPI", "React", "hash-chained audit"], m_og),
 "nexus-ai": ("nexus-ai", "Call logs in C, Claude RCA with cited evidence, gated fixes", ["C11", "Claude", "KPI anomalies", "approval gate"], m_nexus),
 "sentinel": ("Sentinel", "Occlusion-aware human detection for search and rescue", ["YOLO11", "ONNX", "OpenCV", "RGB · NIR · Thermal"], m_sentinel),
 "autonomous-bot": ("autonomous-bot", "ROS 2 robot: SLAM, Nav2, an IoT dashboard and a swarm auction", ["ROS 2", "Nav2", "ESKF", "OpenRMF"], m_bot),
 "finintel": ("finintel", "Financial RAG: filings to grounded, citation-backed advice", ["Hybrid RAG", "GraphRAG", "Claude agent", "Pydantic"], m_finintel),
 "style-transfer-cnn": ("Style Transfer", "Neural style transfer on VGG-19", ["PyTorch", "VGG-19", "Gradio"], m_style),
 "overthinkers-assistant": ("Overthinker's Assistant", "Turn a decision into a tree of pros and cons", ["Flask", "Graphviz", "markovify"], m_tree),
 "one-click-crave": ("One Click Crave", "A meal picker that learns what you actually eat", ["Streamlit", "scikit-learn", "Swiggy links"], m_crave),
 "kinematics-calculator": ("Kinematics Calculator", "Forward and inverse kinematics for 1 to 6 DOF arms", ["NumPy", "Matplotlib", "PPO"], m_kin),
 "fakespotter": ("fakespotter", "Reddit sentiment on counterfeit goods, via DistilBERT", ["PRAW", "Transformers", "pandas"], m_fake),
 "auto_wordle": ("auto_wordle", "A bot that reads the tiles and solves today's Wordle", ["Playwright", "Python"], m_wordle),
 "murdle": ("Murdle", "A terminal whodunit with an insufferable AI assistant", ["Python", "OpenAI", "CLI"], m_murdle),
 "snacksave": ("SnackSave", "An Android app that stops the unnecessary coffee", ["Kotlin", "Compose"], m_snack),
 "credit-card": ("credit-card", "Spending-habit segmentation and reward modelling", ["scikit-learn", "Jupyter", "RF · XGBoost"], m_card),
}
LOCAL = {"nexus-ai", "nexus-og"}  # banners served from this repo (assets/banners/) instead of the project repo

def banner(repo):
    title, tag, chips, motif = MOTIFS[repo]; random.seed(hash(repo) % 999)
    stars = "".join(f'<circle cx="{random.uniform(0,W):.0f}" cy="{random.uniform(0,H):.0f}" r="{random.choice([.6,.9,1.3])}" fill="{random.choice([INK,CYAN,BLUE])}" opacity="0">{an("opacity",f"0;{random.uniform(.4,.9):.2f};0",random.uniform(2.5,6),random.uniform(0,5))}</circle>' for _ in range(55))
    grid = "".join(f'<path d="M{x} 0V{H}" stroke="#101a33"/>' for x in range(0,W,40)) + "".join(f'<path d="M0 {y}H{W}" stroke="#101a33"/>' for y in range(0,H,40))
    cx, fs = 50, 46 if len(title) < 16 else 36
    chip_svg, x = "", 50
    for c in chips:
        w = 14 + len(c)*7.2; chip_svg += f'<rect x="{x}" y="196" width="{w:.0f}" height="24" rx="12" fill="none" stroke="{BLUE}" stroke-opacity=".6"/><text x="{x+w/2:.0f}" y="212" font-size="11" fill="{CYAN}" text-anchor="middle">{c}</text>'; x += w + 8
    gl = lambda dly: f'{an("opacity","0;0;.7;0;.5;0;0",6,dly,"keyTimes=\"0;.9;.915;.93;.945;.96;1\"")}'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{title}: {tag}">
<defs><radialGradient id="bgg" cx=".75" cy=".5" r=".75"><stop offset="0" stop-color="#16244d"/><stop offset=".6" stop-color="{BG}"/><stop offset="1" stop-color="#070a14"/></radialGradient><linearGradient id="ng" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#9cc4ff"/></linearGradient>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".12"/></pattern></defs>
<rect width="{W}" height="{H}" rx="14" fill="url(#bgg)"/>{grid}{stars}
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{DIM}"/>
<g font-family="{FONT}"><text x="52" y="58" font-size="11" fill="{MUTED}" letter-spacing="3">PROJECT / {repo.upper().replace("-","_")}</text>
<text x="{cx}" y="124" font-size="{fs}" font-weight="800" fill="url(#ng)" filter="url(#glow)" font-family="{SANS}">{title}</text>
<text x="{cx}" y="124" font-size="{fs}" font-weight="800" fill="{CYAN}" opacity="0" font-family="{SANS}">{title}{gl(0)}<animate attributeName="x" values="50;50;44;56;50;50" keyTimes="0;.9;.915;.93;.95;1" dur="6s" repeatCount="indefinite"/></text>
<text x="52" y="160" font-size="14" fill="{INK}" opacity=".85">{tag}</text>{chip_svg}</g>
<g transform="translate(570,20)" font-family="{FONT}" filter="url(#glow)">{motif()}</g>
<rect width="{W}" height="{H}" rx="14" fill="url(#scan)"/></svg>'''

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "/home/claude"
    for repo in MOTIFS:
        d = f"{root}/{repo}/assets"; os.makedirs(d, exist_ok=True); open(f"{d}/banner.svg", "w").write(banner(repo))
    print("banners", len(MOTIFS))
