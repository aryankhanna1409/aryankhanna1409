"""Render assets/contributions.svg: an animated, orange-on-black contribution heatmap.

Modes
  * GITHUB_TOKEN set  -> real contribution calendar from the GraphQL API (used by the Action)
  * otherwise         -> reads a {"YYYY-MM-DD": count} JSON file passed as argv[1]
"""
import datetime, json, os, sys, urllib.request

USER = "aryankhanna1409"
BG, EMPTY = "#0b1020", "#141c33"
LEVELS = ["#1e3a8a", "#2f6df0", "#5aa2ff", "#67e8f9"]


def fetch_calendar(token):
    q = ('{user(login:"%s"){contributionsCollection{contributionCalendar{totalContributions '
         'weeks{contributionDays{date contributionCount}}}}}}' % USER)
    req = urllib.request.Request("https://api.github.com/graphql", json.dumps({"query": q}).encode(),
                                 {"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = {d["date"]: d["contributionCount"] for w in cal["weeks"] for d in w["contributionDays"]}
    return days, cal["totalContributions"]


def level(n, mx):
    if n <= 0:
        return None
    return LEVELS[min(3, int(n / max(mx, 1) * 3.999))]


def render(days, total, out):
    today = datetime.date.today()
    start = today - datetime.timedelta(days=today.weekday() + 1 + 52 * 7)   # a Sunday, 53 columns back
    start -= datetime.timedelta(days=(start.weekday() + 1) % 7)
    mx = max(days.values() or [1])
    cell, gap, x0, y0 = 11, 3, 40, 38
    rects, months, seen = [], [], set()
    for c in range(53):
        for r in range(7):
            d = start + datetime.timedelta(days=c * 7 + r)
            if d > today:
                continue
            n = days.get(d.isoformat(), 0)
            col = level(n, mx) or EMPTY
            x, y = x0 + c * (cell + gap), y0 + r * (cell + gap)
            tip = f"<title>{n} contribution{'s' if n != 1 else ''} on {d.isoformat()}</title>"
            rects.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{col}" opacity="0">'
                         f'{tip}<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{c*0.035:.3f}s" fill="freeze"/></rect>')
            if r == 0 and d.day <= 7 and d.month not in seen:
                seen.add(d.month); months.append(f'<text x="{x}" y="{y0-10}">{d.strftime("%b").upper()}</text>')
    width = x0 + 53 * (cell + gap) + 20
    legend = "".join(f'<rect x="{width-168+i*16}" y="{y0+7*(cell+gap)+10}" width="11" height="11" rx="2.5" fill="{c}"/>'
                     for i, c in enumerate([EMPTY] + LEVELS))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 170" width="100%" role="img" aria-label="Contribution heatmap">
<rect width="{width}" height="170" rx="10" fill="{BG}"/>
<g font-family="JetBrains Mono, ui-monospace, Menlo, monospace" font-size="9" fill="#8b98b5">
<text x="14" y="16" font-size="11" fill="#e9edf2" font-weight="600">CONTRIBUTION TRACE</text>
<text x="{width-14}" y="16" font-size="11" fill="#67e8f9" text-anchor="end">{total} in the last year</text>
{''.join(months)}
<text x="14" y="{y0+1*(cell+gap)+9}">Mon</text><text x="14" y="{y0+3*(cell+gap)+9}">Wed</text><text x="14" y="{y0+5*(cell+gap)+9}">Fri</text>
<text x="{width-174}"  y="{y0+7*(cell+gap)+19}" text-anchor="end">less</text>
<text x="{width-76}" y="{y0+7*(cell+gap)+19}">more</text>
</g>
<defs><linearGradient id="beam" x1="0" x2="1"><stop offset="0" stop-color="#67e8f9" stop-opacity="0"/><stop offset="1" stop-color="#67e8f9" stop-opacity="0.35"/></linearGradient></defs>
{legend}
{''.join(rects)}
<rect x="0" y="{y0-6}" width="60" height="{7*(cell+gap)+8}" fill="url(#beam)"><animate attributeName="x" values="{x0-60};{x0+53*(cell+gap)}" dur="5s" repeatCount="indefinite"/></rect>
</svg>'''
    open(out, "w").write(svg)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "assets", "contributions.svg")
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        days, total = fetch_calendar(tok)
    else:
        days = json.load(open(sys.argv[1])); total = sum(days.values())
    render(days, total, out)
    print("wrote", out, total)
