"""Write light-mode twins of every profile SVG into assets/light/ (and project banners into assets/light/banners/).

The dark SVGs stay the source of truth; this remaps their palette so the README can serve
the right one through <picture> + prefers-color-scheme. Re-run after any build_*.py script.
"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.join(os.path.dirname(__file__), "..", "assets")
LIGHT = os.path.join(ROOT, "light")

PALETTE = {
    # surfaces
    "#0b1020": "#ffffff", "#070a14": "#eef2f8", "#16244d": "#dde8fb", "#101a33": "#eef2f7",
    "#141c33": "#ebedf0", "#25375f": "#d0d7de", "#1b2a4d": "#d8dee4", "#2a3d6b": "#c3cfe0",
    "#1e2b52": "#c9d6ea", "#2a4fb0": "#bfdbfe", "#000": "#cbd5e1",
    # text
    "#e6edf3": "#1f2328", "#e9edf2": "#1f2328", "#8b98b5": "#57606a",
    # accents, deepened so they hold contrast on white
    "#5aa2ff": "#1f6feb", "#67e8f9": "#0e7490", "#8b5cf6": "#7c3aed",
    "#1e3a8a": "#bfdbfe", "#2f6df0": "#60a5fa",
    # name gradient: white -> pale blue becomes navy -> blue
    "#ffffff": "#0b1020", "#fff": "#0b1020", "#9cc4ff": "#1f6feb",
}
HEX = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")


def lighten(svg):
    svg = HEX.sub(lambda m: PALETTE.get(m.group(0).lower(), m.group(0)), svg)
    return svg.replace('stdDeviation="3"', 'stdDeviation="1.2"').replace('stdDeviation="2.5"', 'stdDeviation="1"')  # softer glow on white


def main():
    os.makedirs(os.path.join(LIGHT, "banners"), exist_ok=True)
    n = 0
    for path in glob.glob(os.path.join(ROOT, "*.svg")):
        open(os.path.join(LIGHT, os.path.basename(path)), "w").write(lighten(open(path).read())); n += 1
    from build_banners import MOTIFS, banner
    for repo in MOTIFS:
        open(os.path.join(LIGHT, "banners", f"{repo}.svg"), "w").write(lighten(banner(repo))); n += 1
    print("light svgs", n)


if __name__ == "__main__":
    main()
