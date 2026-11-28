"""One animated theme per repo, each in dark and light.

Every repo gets its own palette and its own animated scene (SMIL, so it
plays inside GitHub READMEs). Writes banner + footer (or loop) SVGs.

    python themes.py OUT_ROOT          # writes OUT_ROOT/<repo>/assets/...
"""
import os
import sys

W = 880
FONT = "'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, monospace"

# name: (title, tagline, kicker, dark palette, light palette)
# palette = (bg1, bg2, accent, accent2, ink, muted)
REPOS = {
    "sentinel": ("sentinel", "Search-and-rescue vision: YOLO11 finds people who are hidden or in the dark, across RGB, near-infrared and thermal views.", "THERMAL SCAN",
                 ("#0b0507", "#1d0a0a", "#ff6a00", "#ffd23f", "#fff3e6", "#c99a7c"), ("#fff6ef", "#ffe6d4", "#d14800", "#b07b00", "#2a1208", "#8a5a44")),
    "autonomous-bot": ("autonomous-bot", "A ROS 2 robot that maps, localises and navigates on its own, with an IoT dashboard and a swarm auction.", "SLAM · NAV2 · SWARM",
                       ("#03140f", "#06261c", "#2ef2a0", "#7cf7ff", "#e8fff6", "#7fb8a4"), ("#effcf6", "#d6f5e8", "#0a8f5c", "#0b7a8a", "#06261c", "#4f7f6e")),
    "finintel": ("finintel", "A financial RAG system that writes grounded, citation-backed advisory reports from SEC filings.", "RAG · CITED · SEC",
                 ("#060b1a", "#0e1a36", "#f5c542", "#5aa2ff", "#eef3ff", "#8fa0c7"), ("#f7f9ff", "#e6ecfb", "#a87900", "#1f5fd6", "#0e1a36", "#56648a")),
    "nexus": ("nexus", "Network intelligence and a policy-gated DevSecOps agent: it finds the root cause, proposes the fix and waits for approval.", "RCA · DEVSECOPS",
              ("#0c0618", "#1b0d33", "#b26bff", "#22d3ee", "#f4ecff", "#a493c7"), ("#faf6ff", "#ece2fc", "#7a2fd6", "#0b8ea8", "#1b0d33", "#6a5a8c")),
    "a.t.h.e.n.a": ("A.T.H.E.N.A.", "Agentic Telemetry, Healing & Network Assurance: detects telecom faults, explains them and heals the network behind a policy gate.", "DETECT · EXPLAIN · HEAL",
                    ("#04110f", "#0a1f2e", "#34d399", "#818cf8", "#eafff8", "#86a9a2"), ("#f1fbf8", "#dcefee", "#0b8a5e", "#4f46e5", "#0a1f2e", "#4f6f6a")),
    "dishdecoded": ("dishdecoded", "Snap a dish or a menu and get its story, allergens and a recipe.", "SNAP · DECODE · COOK",
                    ("#170907", "#2a100b", "#ff5a3c", "#ffc06b", "#fff1e8", "#c99c88"), ("#fff8f2", "#ffe9dc", "#d63a1c", "#b86e00", "#2a100b", "#8a5c4c")),
    "one-click-crave": ("One Click Crave", "An AI meal assistant, shaped by six months of testing with blind, deaf and elderly users.", "ONE TAP · ACCESSIBLE",
                        ("#16070f", "#2b0d1e", "#ff6fa8", "#ffb36b", "#fff0f6", "#c896ad"), ("#fff6fa", "#ffe4ef", "#d1306f", "#b8670a", "#2b0d1e", "#8a5a70")),
    "SnackSave": ("SnackSave", "An Android app that taps you on the shoulder before an unnecessary coffee.", "SAVE · SIP · SMILE",
                  ("#071410", "#10241c", "#5eead4", "#e0a96d", "#ecfffa", "#8fb3a8"), ("#f2fdf9", "#dcf5ec", "#0d8f7a", "#9a5a1c", "#10241c", "#52786d")),
    "overthinkers-assistant": ("Overthinker's Assistant", "Type a decision. Get pros, cons, sarcasm and a flowchart.", "PROS · CONS · SPIRALS",
                               ("#0d0a1c", "#1d1838", "#c4b5fd", "#f9a8d4", "#f5f2ff", "#a59fc7"), ("#f9f7ff", "#ebe6ff", "#6d4fd6", "#c0307a", "#1d1838", "#625c88")),
    "murdle": ("Murdle", "A terminal whodunit where your AI assistant knows the answer and is insufferable about it.", "WHODUNIT · NOIR",
               ("#0a0606", "#1c0b0b", "#e11d48", "#f5e6c8", "#f7efe6", "#a38d86"), ("#fbf7f2", "#efe4d6", "#b0122f", "#6b4a1c", "#1c0b0b", "#6e5c56")),
    "kinematics-calculator": ("Kinematics Calculator", "Forward and inverse kinematics for robot arms of 1 to 6 degrees of freedom, with 3D animation.", "FK · IK · DH",
                              ("#05101c", "#0c2036", "#38bdf8", "#fb923c", "#eaf6ff", "#88a3bf"), ("#f3f9ff", "#dfeefc", "#0369a1", "#c2410c", "#0c2036", "#4f6a85")),
    "credit-card": ("credit-card", "Spending-habit segmentation and reward modelling on Indian credit-card data. Published, IJCIS 2025.", "SEGMENT · REWARD",
                    ("#06120a", "#0f2416", "#4ade80", "#facc15", "#eefff2", "#8db39a"), ("#f3fdf5", "#ddf5e3", "#15803d", "#a16207", "#0f2416", "#517a5e")),
    "auto_wordle": ("auto_wordle", "A bot that opens today's Wordle, reads the tiles and solves it for you.", "GUESS · READ · SOLVE",
                    ("#0e0f10", "#1c1f22", "#6aaa64", "#c9b458", "#f3f4f5", "#9aa0a6"), ("#fafafa", "#ececec", "#4c8c46", "#a8922e", "#1c1f22", "#5f6368")),
    "fakespotter": ("fakespotter", "Tracks how Reddit talks about counterfeit goods and scores the sentiment of every thread.", "SCRAPE · SCORE · SPOT",
                    ("#120803", "#24120a", "#ff7a1a", "#60a5fa", "#fff3ea", "#c2a08a"), ("#fff9f4", "#ffebdc", "#d25400", "#2563eb", "#24120a", "#7f5d48")),
}
REPOS["A.E.T.H.E.R"] = ("AETHER", "A local, private, neuro-symbolic assistant.", "LOCAL · PRIVATE",
                        ("#0a040e", "#1a0824", "#ff2fa0", "#f5c542", "#fff0fa", "#b893ad"), ("#fff7fc", "#fbe3f2", "#c2127a", "#a87900", "#1a0824", "#7c5a72"))
OWN_BRAND = {"A.E.T.H.E.R"}  # already has its own hero; only shown in the profile mosaic
LOOP_REPOS = {"autonomous-bot", "sentinel", "finintel", "nexus", "dishdecoded"}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def wrap(text, n):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return out + [cur]


def anim(attr, values, dur, extra=""):
    return f'<animate attributeName="{attr}" values="{values}" dur="{dur}s" repeatCount="indefinite" {extra}/>'


# --------------------------------------------------------------- scenes
# Each scene draws into a 300x220 box. p = palette.
def scene(name, p):
    bg1, bg2, a, b, ink, mu = p
    s = ""
    if name == "sentinel":  # thermal blob + scan brackets + radar sweep
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        s += f'<g><ellipse cx="150" cy="120" rx="46" ry="62" fill="url(#heat)">{anim("rx","46;50;46",2.4)}</ellipse>'
        s += f'<circle cx="150" cy="58" r="20" fill="url(#heat)"/></g>'
        for x, y, dx, dy in [(96, 38, 1, 1), (204, 38, -1, 1), (96, 196, 1, -1), (204, 196, -1, -1)]:
            s += f'<path d="M{x} {y+dy*18} V{y} H{x+dx*18}" fill="none" stroke="{b}" stroke-width="3">{anim("opacity","1;.3;1",1.2)}</path>'
        s += f'<rect x="10" y="10" width="280" height="2" fill="{a}" opacity=".8">{anim("y","10;206;10",3)}</rect>'
        s += f'<rect x="180" y="18" width="104" height="20" rx="4" fill="{bg2}" stroke="{b}"/><text x="232" y="32" font-family="{MONO}" font-size="11" fill="{b}" text-anchor="middle">PERSON 0.94</text>'
        s += f'<g transform="translate(40,180)"><circle r="26" fill="none" stroke="{a}" stroke-opacity=".5"/><circle r="14" fill="none" stroke="{a}" stroke-opacity=".3"/>'
        s += f'<path d="M0 0 L26 0 A26 26 0 0 0 18 -18z" fill="{a}" opacity=".5"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="2.5s" repeatCount="indefinite"/></path></g>'
    elif name == "autonomous-bot":  # grid map, path, robot with lidar
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        for i in range(1, 10):
            s += f'<line x1="{i*30}" y1="0" x2="{i*30}" y2="220" stroke="{a}" stroke-opacity=".08"/>'
        for i in range(1, 8):
            s += f'<line x1="0" y1="{i*28}" x2="300" y2="{i*28}" stroke="{a}" stroke-opacity=".08"/>'
        s += f'<rect x="120" y="30" width="60" height="40" fill="{mu}" opacity=".35"/><rect x="200" y="130" width="70" height="30" fill="{mu}" opacity=".35"/>'
        path = "M30 190 H100 V100 H220 V50 H270"
        s += f'<path d="{path}" fill="none" stroke="{b}" stroke-width="2" stroke-dasharray="6 5">{anim("stroke-dashoffset","22;0",1)}</path>'
        s += (f'<g><animateMotion path="{path}" dur="7s" repeatCount="indefinite" rotate="auto"/>'
              f'<path d="M0 0 L60 -22 A64 64 0 0 1 60 22z" fill="{a}" opacity=".22"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="1.6s" repeatCount="indefinite"/></path>'
              f'<rect x="-11" y="-9" width="22" height="18" rx="4" fill="{a}"/><circle r="4" fill="{bg1}"/></g>')
    elif name == "finintel":  # candles + citation chips
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        vals = [120, 100, 110, 80, 90, 60, 70, 45]
        for i, v in enumerate(vals):
            x = 30 + i * 30
            up = i % 2 == 1
            col = a if up else b
            s += f'<line x1="{x+7}" y1="{v-14}" x2="{x+7}" y2="{v+44}" stroke="{col}" stroke-width="2" opacity="0">{anim("opacity",f"0;0;1;1",6,f"keyTimes=\"0;{i/10:.2f};{i/10+.05:.2f};1\"")}</line>'
            s += f'<rect x="{x}" y="{v}" width="14" height="30" rx="2" fill="{col}" opacity="0">{anim("opacity",f"0;0;1;1",6,f"keyTimes=\"0;{i/10:.2f};{i/10+.05:.2f};1\"")}</rect>'
        s += f'<path d="M30 160 C90 150 130 120 170 110 S250 70 280 60" fill="none" stroke="{ink}" stroke-opacity=".5" stroke-width="2" stroke-dasharray="300" stroke-dashoffset="300">{anim("stroke-dashoffset","300;0;0",6)}</path>'
        for i, t in enumerate(["[1] 10-K", "[2] 13F", "[3] call"]):
            s += f'<g opacity="0"><rect x="{24+i*90}" y="182" width="78" height="24" rx="12" fill="{bg2}" stroke="{a}"/><text x="{63+i*90}" y="198" font-family="{MONO}" font-size="11" fill="{a}" text-anchor="middle">{t}</text>{anim("opacity","0;0;1;1",6,f"keyTimes=\"0;{.6+i*.08:.2f};{.65+i*.08:.2f};1\"")}</g>'
    elif name in ("nexus", "a.t.h.e.n.a"):
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        if name == "nexus":  # node graph with pulse and alert
            nodes = [(50, 60), (150, 40), (250, 70), (90, 150), (200, 160), (150, 105)]
            edges = [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (0, 3), (2, 4), (0, 1), (1, 2)]
            for i, j in edges:
                (x1, y1), (x2, y2) = nodes[i], nodes[j]
                s += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{b}" stroke-opacity=".35"/>'
            for k, (i, j) in enumerate(edges[:5]):
                (x1, y1), (x2, y2) = nodes[i], nodes[j]
                s += f'<circle r="3" fill="{b}"><animateMotion path="M{x1} {y1} L{x2} {y2}" dur="{1.4+k*.3:.1f}s" repeatCount="indefinite"/></circle>'
            for k, (x, y) in enumerate(nodes):
                alert = k == 4
                s += f'<circle cx="{x}" cy="{y}" r="{14 if k==5 else 10}" fill="{bg2}" stroke="{a if not alert else "#ff4d6d"}" stroke-width="2.5">'
                if alert:
                    s += anim("stroke", f"#ff4d6d;#ff4d6d;{a};{a}", 5, 'keyTimes="0;.5;.55;1" calcMode="discrete"')
                s += '</circle>'
            s += f'<g opacity="0">{anim("opacity","0;0;1;1;0",5,"keyTimes=\"0;.25;.3;.5;.55\"")}<rect x="180" y="190" width="104" height="22" rx="6" fill="{bg2}" stroke="{a}"/><text x="232" y="205" font-family="{MONO}" font-size="11" fill="{a}" text-anchor="middle">approve? y/N</text></g>'
        else:  # KPI line with spike that heals, shield
            spike = "M10 130 L60 128 L100 132 L130 126 L150 40 L170 132 L210 128 L250 130 L290 127"
            flat = "M10 130 L60 128 L100 132 L130 126 L150 128 L170 132 L210 128 L250 130 L290 127"
            s += f'<path fill="none" stroke="{a}" stroke-width="3" d="{spike}"><animate attributeName="d" values="{spike};{spike};{flat};{flat}" keyTimes="0;.45;.6;1" dur="6s" repeatCount="indefinite"/></path>'
            s += f'<circle cx="150" cy="40" r="16" fill="none" stroke="#ff4d6d" stroke-width="2">{anim("opacity","1;1;0;0",6,"keyTimes=\"0;.45;.5;1\"")}{anim("r","10;20;10",1)}</circle>'
            s += f'<g transform="translate(150,172)"><path d="M0 -28 L22 -20 V2 C22 16 10 24 0 28 C-10 24 -22 16 -22 2 V-20z" fill="{bg2}" stroke="{b}" stroke-width="2.5"/>'
            s += f'<path d="M-9 0 l6 7 l12 -14" fill="none" stroke="{a}" stroke-width="3" opacity="0">{anim("opacity","0;0;1;1",6,"keyTimes=\"0;.6;.62;1\"")}</path></g>'
            for i, t in enumerate(["DETECT", "EXPLAIN", "HEAL"]):
                s += f'<text x="{40+i*110}" y="24" font-family="{MONO}" font-size="11" fill="{mu}" text-anchor="middle">{t}<animate attributeName="fill" values="{mu};{b};{mu}" dur="6s" begin="{i*2}s" repeatCount="indefinite"/></text>'
    elif name == "dishdecoded":  # plate, steam, scanning ring
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        s += f'<circle cx="150" cy="120" r="66" fill="{bg2}" stroke="{ink}" stroke-opacity=".3" stroke-width="3"/><circle cx="150" cy="120" r="46" fill="none" stroke="{ink}" stroke-opacity=".2"/>'
        s += f'<circle cx="138" cy="114" r="16" fill="{a}"/><circle cx="164" cy="128" r="12" fill="{b}"/><circle cx="150" cy="140" r="9" fill="{a}" opacity=".7"/>'
        s += f'<circle cx="150" cy="120" r="80" fill="none" stroke="{b}" stroke-width="2.5" stroke-dasharray="10 10"><animateTransform attributeName="transform" type="rotate" from="0 150 120" to="360 150 120" dur="10s" repeatCount="indefinite"/></circle>'
        for i in range(3):
            x = 125 + i * 25
            s += f'<path d="M{x} 46 q-8 -10 0 -20 q8 -10 0 -20" fill="none" stroke="{ink}" stroke-opacity=".5" stroke-width="2">{anim("opacity","0;.8;0",2.4,f"begin=\"{i*.6}s\"")}<animateTransform attributeName="transform" type="translate" values="0 6;0 -6" dur="2.4s" begin="{i*.6}s" repeatCount="indefinite"/></path>'
        for i, t in enumerate(["story", "allergens", "recipe"]):
            s += f'<g opacity="0">{anim("opacity","0;1;1;0",6,f"begin=\"{i*2}s\" keyTimes=\"0;.1;.3;.35\"")}<rect x="196" y="{20+i*0}" width="90" height="22" rx="11" fill="{a}"/><text x="241" y="35" font-family="{MONO}" font-size="11" fill="{bg1}" text-anchor="middle">{t}</text></g>'
    elif name == "one-click-crave":  # big pulsing button + ripples + bowl
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        for i in range(3):
            s += f'<circle cx="150" cy="105" r="40" fill="none" stroke="{a}" stroke-width="2">{anim("r","40;100",3,f"begin=\"{i}s\"")}{anim("opacity",".8;0",3,f"begin=\"{i}s\"")}</circle>'
        s += f'<circle cx="150" cy="105" r="42" fill="{a}">{anim("r","42;38;42",1.5)}</circle>'
        s += f'<path d="M128 100 h44 a22 22 0 0 1 -44 0z" fill="{bg1}"/><path d="M140 92 q4 -10 0 -16 M152 92 q4 -10 0 -16 M164 92 q4 -10 0 -16" stroke="{bg1}" stroke-width="2.5" fill="none"/>'
        s += f'<text x="150" y="190" font-family="{FONT}" font-size="14" font-weight="700" fill="{b}" text-anchor="middle">what should I eat?<animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></text>'
    elif name == "SnackSave":  # coffee cup, coins dropping in jar
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        s += f'<path d="M50 90 h70 v60 a25 25 0 0 1 -25 25 h-20 a25 25 0 0 1 -25 -25z" fill="{b}"/><path d="M120 105 a16 16 0 0 1 0 32" fill="none" stroke="{b}" stroke-width="6"/>'
        s += f'<line x1="40" y1="80" x2="140" y2="190" stroke="#ff4d6d" stroke-width="6" stroke-linecap="round" opacity="0">{anim("opacity","0;0;1;1;0",4,"keyTimes=\"0;.3;.35;.8;.85\"")}</line>'
        s += f'<rect x="190" y="90" width="70" height="90" rx="10" fill="none" stroke="{a}" stroke-width="3"/><rect x="200" y="78" width="50" height="14" rx="3" fill="{a}"/>'
        for i in range(3):
            s += f'<circle cx="225" r="9" fill="{a}" stroke="{bg1}" stroke-width="2"><animate attributeName="cy" values="40;{165-i*14};{165-i*14}" keyTimes="0;.3;1" dur="4s" begin="{i*.5}s" repeatCount="indefinite"/></circle>'
        s += f'<text x="225" y="208" font-family="{MONO}" font-size="12" fill="{a}" text-anchor="middle">+ ₹180 saved</text>'
    elif name == "overthinkers-assistant":  # branching decision tree drawing itself
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        segs = [("M150 30 L80 90", 0), ("M150 30 L220 90", 0), ("M80 90 L40 150", 1), ("M80 90 L120 150", 1), ("M220 90 L180 150", 1), ("M220 90 L260 150", 1),
                ("M40 150 L25 200", 2), ("M40 150 L60 200", 2), ("M120 150 L105 200", 2), ("M120 150 L140 200", 2), ("M180 150 L165 200", 2), ("M180 150 L200 200", 2), ("M260 150 L245 200", 2), ("M260 150 L280 200", 2)]
        for d, lvl in segs:
            t0 = .1 + lvl * .22
            s += f'<path d="{d}" stroke="{a if lvl<2 else b}" stroke-width="2.5" fill="none" stroke-dasharray="80" stroke-dashoffset="80"><animate attributeName="stroke-dashoffset" values="80;80;0;0" keyTimes="0;{t0:.2f};{t0+.15:.2f};1" dur="6s" repeatCount="indefinite"/></path>'
        s += f'<rect x="110" y="16" width="80" height="26" rx="13" fill="{a}"/><text x="150" y="34" font-family="{FONT}" font-size="12" font-weight="700" fill="{bg1}" text-anchor="middle">should I?</text>'
        s += f'<text x="80" y="82" font-family="{MONO}" font-size="11" fill="{ink}" text-anchor="middle">pros</text><text x="220" y="82" font-family="{MONO}" font-size="11" fill="{ink}" text-anchor="middle">cons</text>'
    elif name == "murdle":  # noir: magnifier sweeping over suspects
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        for i, x in enumerate([60, 120, 180, 240]):
            s += f'<circle cx="{x}" cy="90" r="16" fill="{mu}" opacity=".6"/><rect x="{x-20}" y="108" width="40" height="50" rx="12" fill="{mu}" opacity=".6"/>'
            s += f'<text x="{x}" y="180" font-family="{MONO}" font-size="11" fill="{mu}" text-anchor="middle">#{i+1}</text>'
        s += (f'<g><animateTransform attributeName="transform" type="translate" values="60 100;120 100;180 100;240 100;180 100;180 100;60 100" keyTimes="0;.15;.3;.45;.6;.9;1" dur="8s" repeatCount="indefinite"/>'
              f'<circle r="30" fill="{b}" fill-opacity=".12" stroke="{b}" stroke-width="4"/><line x1="22" y1="22" x2="44" y2="44" stroke="{b}" stroke-width="8" stroke-linecap="round"/></g>')
        s += f'<text x="150" y="40" font-family="{MONO}" font-size="13" fill="{a}" text-anchor="middle" opacity="0">it was #3, obviously.{anim("opacity","0;0;1;1;0",8,"keyTimes=\"0;.6;.62;.9;.92\"")}</text>'
    elif name == "kinematics-calculator":  # 2-link arm rotating with trace
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        s += f'<circle cx="150" cy="150" r="110" fill="none" stroke="{a}" stroke-opacity=".12" stroke-dasharray="4 6"/>'
        s += f'<rect x="125" y="175" width="50" height="20" rx="4" fill="{mu}" opacity=".5"/>'
        s += (f'<g transform="translate(150,165)"><g><animateTransform attributeName="transform" type="rotate" values="-150;-30;-150" dur="6s" repeatCount="indefinite"/>'
              f'<rect x="0" y="-6" width="70" height="12" rx="6" fill="{a}"/><circle r="9" fill="{bg2}" stroke="{a}" stroke-width="3"/>'
              f'<g transform="translate(70,0)"><g><animateTransform attributeName="transform" type="rotate" values="40;-70;40" dur="3s" repeatCount="indefinite"/>'
              f'<rect x="0" y="-5" width="55" height="10" rx="5" fill="{b}"/><circle r="7" fill="{bg2}" stroke="{b}" stroke-width="3"/>'
              f'<path d="M55 -8 l10 -6 M55 8 l10 6" stroke="{b}" stroke-width="3"/></g></g></g></g>')
        s += f'<text x="20" y="30" font-family="{MONO}" font-size="11" fill="{mu}">θ1, θ2 → (x, y, z)</text>'
    elif name == "credit-card":  # card with shine + cluster dots
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        s += f'<g transform="translate(30,40) rotate(-6)"><rect width="150" height="94" rx="10" fill="{a}"/><rect x="14" y="24" width="24" height="18" rx="3" fill="{b}"/>'
        s += f'<text x="14" y="70" font-family="{MONO}" font-size="12" fill="{bg1}">•••• 2025</text>'
        s += f'<clipPath id="cc"><rect width="150" height="94" rx="10"/></clipPath><g clip-path="url(#cc)"><rect x="-60" y="0" width="30" height="94" fill="#fff" opacity=".35" transform="skewX(-20)">{anim("x","-60;200",2.5)}</rect></g></g>'
        import random
        rnd = random.Random(7)
        for cx, cy, col in [(230, 60, a), (250, 150, b), (180, 170, ink)]:
            for k in range(7):
                x, y = cx + rnd.randint(-22, 22), cy + rnd.randint(-18, 18)
                s += f'<circle cx="{x}" cy="{y}" r="4" fill="{col}" opacity=".85">{anim("r","3;5;3",2+k*.2)}</circle>'
        s += f'<text x="30" y="200" font-family="{MONO}" font-size="11" fill="{mu}">K-Means · XGBoost · RF</text>'
    elif name == "auto_wordle":  # tiles flipping
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        rows = [("CRANE", "xyxxg"), ("SLATE", "xxgxg"), ("MOUSE", "ggggg")]
        for r, (word, res) in enumerate(rows):
            for c, (ch, st) in enumerate(zip(word, res)):
                x, y = 40 + c * 46, 30 + r * 56
                col = {"g": a, "y": b, "x": mu}[st]
                t0 = (r * 5 + c) / 18
                s += (f'<g transform="translate({x+20},{y+22})"><g><animateTransform attributeName="transform" type="scale" values="1 1;1 1;1 0;1 1;1 1" keyTimes="0;{t0:.2f};{t0+.03:.2f};{t0+.06:.2f};1" dur="7s" repeatCount="indefinite"/>'
                      f'<rect x="-20" y="-22" width="40" height="44" rx="4" fill="none" stroke="{mu}" stroke-width="2"/>'
                      f'<rect x="-20" y="-22" width="40" height="44" rx="4" fill="{col}" opacity="0"><animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{t0+.03:.2f};{t0+.031:.3f};1" dur="7s" repeatCount="indefinite"/></rect>'
                      f'<text y="8" font-family="{FONT}" font-size="22" font-weight="800" fill="{ink}" text-anchor="middle">{ch}</text></g></g>')
    elif name == "A.E.T.H.E.R":  # voice orb + waveform
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        s += f'<circle cx="150" cy="95" r="44" fill="{a}" opacity=".18">{anim("r","40;54;40",2)}</circle><circle cx="150" cy="95" r="30" fill="{a}">{anim("r","28;33;28",2)}</circle>'
        for i in range(21):
            x = 50 + i * 10
            hgt = 6 + (i * 7) % 22
            s += f'<rect x="{x}" y="170" width="5" height="{hgt}" rx="2" fill="{b}"><animate attributeName="height" values="{hgt};{4+(i*11)%28};{hgt}" dur="{0.8+(i%4)*.2:.1f}s" repeatCount="indefinite"/></rect>'
    elif name == "fakespotter":  # thread bubbles with sentiment bars
        s += f'<rect width="300" height="220" rx="14" fill="{bg1}" stroke="{a}" stroke-opacity=".4"/>'
        for i, (w, sc) in enumerate([(150, .8), (190, .3), (130, .6), (170, .15)]):
            y = 22 + i * 48
            s += f'<g opacity="0">{anim("opacity","0;0;1;1",6,f"keyTimes=\"0;{i*.15:.2f};{i*.15+.05:.2f};1\"")}<rect x="20" y="{y}" width="{w}" height="34" rx="10" fill="{bg2}" stroke="{mu}" stroke-opacity=".5"/>'
            s += f'<rect x="32" y="{y+10}" width="{w-60}" height="5" rx="2" fill="{mu}" opacity=".6"/><rect x="32" y="{y+20}" width="{w-90}" height="5" rx="2" fill="{mu}" opacity=".4"/></g>'
            col = a if sc > .5 else b
            s += f'<rect x="230" y="{y+12}" width="0" height="10" rx="5" fill="{col}"><animate attributeName="width" values="0;0;{int(56*sc)+4};{int(56*sc)+4}" keyTimes="0;{i*.15+.05:.2f};{i*.15+.2:.2f};1" dur="6s" repeatCount="indefinite"/></rect>'
        s += f'<text x="258" y="214" font-family="{MONO}" font-size="10" fill="{mu}" text-anchor="middle">sentiment</text>'
    return s


def defs(p):
    bg1, bg2, a, b, ink, mu = p
    return (f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></linearGradient>'
            f'<radialGradient id="glow" cx=".8" cy=".2" r=".7"><stop offset="0" stop-color="{a}" stop-opacity=".22"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="heat"><stop offset="0" stop-color="#fff7b0"/><stop offset=".35" stop-color="#ffd23f"/><stop offset=".7" stop-color="#ff6a00"/><stop offset="1" stop-color="#b3001b" stop-opacity=".6"/></radialGradient>'
            f'<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>')


def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(label)}">'
            f'{body}</svg>')


def banner(name, p):
    title, tag, kick, *_ = REPOS[name]
    bg1, bg2, a, b, ink, mu = p
    h = 300
    body = defs(p) + f'<rect width="{W}" height="{h}" rx="18" fill="url(#bg)"/><rect width="{W}" height="{h}" rx="18" fill="url(#glow)"/>'
    # drifting particles in the accent colour
    for i in range(14):
        x, y = (i * 61) % 540 + 10, (i * 37) % 260 + 20
        body += f'<circle cx="{x}" cy="{y}" r="{1.5 + i % 3}" fill="{a if i%2 else b}" opacity=".35">{anim("cy",f"{y};{y-14};{y}",4+i%5)}</circle>'
    body += f'<text x="44" y="70" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{a}">{esc(kick)}</text>'
    fs = 50 if len(title) <= 14 else 38
    body += f'<text x="42" y="{70+fs+8}" font-family="{FONT}" font-size="{fs}" font-weight="800" fill="{ink}">{esc(title)}</text>'
    for i, ln in enumerate(wrap(tag, 50)[:4]):
        body += f'<text x="44" y="{168+i*22}" font-family="{FONT}" font-size="16" fill="{mu}">{esc(ln)}</text>'
    body += f'<rect x="44" y="{h-34}" width="0" height="4" rx="2" fill="url(#bar)">{anim("width","0;180;180",3,"keyTimes=\"0;.5;1\"")}</rect>'
    body += f'<g transform="translate(556,40)">{scene(name, p)}</g>'
    return svg(W, h, body, f"{title}: {tag}")


def footer(name, p, loop=False):
    title = REPOS[name][0]
    bg1, bg2, a, b, ink, mu = p
    h = 96
    body = defs(p) + f'<rect width="{W}" height="{h}" rx="16" fill="url(#bg)"/>'
    # a travelling pulse along a line, in the repo palette
    body += f'<line x1="40" y1="64" x2="{W-40}" y2="64" stroke="{a}" stroke-opacity=".25" stroke-width="2"/>'
    body += f'<circle cy="64" r="5" fill="{a}">{anim("cx",f"40;{W-40}",5)}</circle><circle cy="64" r="10" fill="{a}" opacity=".25">{anim("cx",f"40;{W-40}",5)}</circle>'
    if loop:
        stops = ["MOVE", "SEE", "KNOW", "ACT", "SHIP"]
        cur = ["autonomous-bot", "sentinel", "finintel", "nexus", "dishdecoded"].index(name)
        for i, sname in enumerate(stops):
            x = 88 + i * 176
            on = i == cur
            body += f'<circle cx="{x}" cy="64" r="{9 if on else 6}" fill="{a if on else bg2}" stroke="{a}" stroke-width="2"/>'
            body += f'<text x="{x}" y="38" font-family="{MONO}" font-size="12" font-weight="{700 if on else 400}" fill="{ink if on else mu}" text-anchor="middle">0{i+1} {sname}</text>'
        label = f"{title} is one stop in a loop: move, see, know, act, ship"
    else:
        body += f'<text x="{W/2}" y="40" font-family="{FONT}" font-size="15" fill="{ink}" text-anchor="middle">{esc(title)} · part of Aryan Khanna\'s portfolio</text>'
        label = f"{title}, part of Aryan Khanna's portfolio"
    return svg(W, h, body, label)


def mosaic(theme):
    """Hybrid hero for the profile: every repo's scene in its own palette."""
    names = [n for n in REPOS if n != "nexus"]  # A.T.H.E.N.A. replaces nexus
    cols, gap = 5, 12
    cw = (W - 80 - (cols - 1) * gap) / cols
    ch = cw * 220 / 300
    rows = (len(names) + cols - 1) // cols
    h = int(140 + rows * (ch + 26) + 10)
    dark = theme == "dark"
    bg = ("#070a14", "#111a2e") if dark else ("#f6f8fc", "#e6ecf6")
    ink, mu = ("#eef3ff", "#93a2c4") if dark else ("#0e1a36", "#56648a")
    body = (f'<defs><linearGradient id="hb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{bg[0]}"/><stop offset="1" stop-color="{bg[1]}"/></linearGradient>'
            f'<linearGradient id="rb" x1="0" x2="1">' + "".join(
                f'<stop offset="{i/(len(names)-1):.2f}" stop-color="{REPOS[n][3 if dark else 4][2]}"/>' for i, n in enumerate(names)) + '</linearGradient>'
            f'<radialGradient id="heat"><stop offset="0" stop-color="#fff7b0"/><stop offset=".35" stop-color="#ffd23f"/><stop offset=".7" stop-color="#ff6a00"/><stop offset="1" stop-color="#b3001b" stop-opacity=".6"/></radialGradient></defs>')
    body += f'<rect width="{W}" height="{h}" rx="18" fill="url(#hb)"/>'
    body += f'<text x="40" y="66" font-family="{FONT}" font-size="44" font-weight="800" fill="{ink}">Aryan Khanna</text>'
    body += f'<text x="42" y="98" font-family="{FONT}" font-size="16" fill="{mu}">Robotics → AI → systems · incoming FDE intern at Incedo · Pune, IN</text>'
    body += f'<rect x="42" y="112" width="0" height="5" rx="2.5" fill="url(#rb)">{anim("width","0;796;796",4,'keyTimes="0;.6;1"')}</rect>'
    for i, n in enumerate(names):
        r, c = divmod(i, cols)
        x = 40 + c * (cw + gap)
        y = 134 + r * (ch + 26)
        p = REPOS[n][3 if dark else 4]
        body += f'<svg x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" viewBox="0 0 300 220" overflow="hidden">{scene(n, p)}</svg>'
        body += f'<text x="{x+cw/2:.1f}" y="{y+ch+16:.1f}" font-family="{MONO}" font-size="11" fill="{p[2]}" text-anchor="middle">{esc(REPOS[n][0])}</text>'
    return svg(W, h, body, "Aryan Khanna: every project in its own colours and motion, robotics to AI to systems")


def write(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(s)


if __name__ == "__main__":
    out = sys.argv[1]
    for n, (title, tag, kick, dark, light) in REPOS.items():
        if n in OWN_BRAND:
            continue
        loop = n in LOOP_REPOS
        base = os.path.join(out, n, "assets")
        write(f"{base}/banner.svg", banner(n, dark))
        write(f"{base}/banner-light.svg", banner(n, light))
        fn = "loop" if loop else "footer"
        write(f"{base}/{fn}.svg", footer(n, dark, loop))
        write(f"{base}/{fn}-light.svg", footer(n, light, loop))
    write(f"{out}/_profile/hero.svg", mosaic("dark"))
    write(f"{out}/_profile/hero-light.svg", mosaic("light"))
    print("done")
