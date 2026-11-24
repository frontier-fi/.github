from pathlib import Path
from xml.sax.saxutils import escape

OUT_DIR = Path(__file__).resolve().parent.parent / "profile"

THEMES = {
    "light": {
        "node_fill": "#f6f8fa",
        "node_stroke": "#d0d7de",
        "spine_fill": "#ffffff",
        "spine_stroke": "#8c959f",
        "group_fill": "#f6f8fa",
        "group_fill_opacity": "0.5",
        "group_stroke": "#d0d7de",
        "text": "#1f2328",
        "muted": "#59636e",
        "edge_solid": "#24292f",
        "edge_dashed": "#656d76",
    },
    "dark": {
        "node_fill": "#161b22",
        "node_stroke": "#30363d",
        "spine_fill": "#161b22",
        "spine_stroke": "#6e7681",
        "group_fill": "#161b22",
        "group_fill_opacity": "0.4",
        "group_stroke": "#30363d",
        "text": "#e6edf3",
        "muted": "#8b949e",
        "edge_solid": "#c9d1d9",
        "edge_dashed": "#8b949e",
    },
}

FONT_MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
FONT_SANS = "-apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"


def render_svg(mode: str) -> str:
    t = THEMES[mode]
    W, H = 920, 480

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Frontier Finance repository architecture">',
        "<defs>",
        '  <marker id="arr-solid" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">',
        f'    <path d="M 1 1.5 L 9 5 L 1 8.5 z" fill="{t["edge_solid"]}"/>',
        "  </marker>",
        '  <marker id="arr-dashed" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">',
        f'    <path d="M 1 1.5 L 9 5 L 1 8.5 z" fill="{t["edge_dashed"]}"/>',
        "  </marker>",
        "</defs>",
    ]

    def node(x, y, w, h, label, spine=False):
        fill = t["spine_fill"] if spine else t["node_fill"]
        stroke = t["spine_stroke"] if spine else t["node_stroke"]
        sw = "1.5" if spine else "1.2"
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )
        parts.append(
            f'<text x="{x + w/2:.1f}" y="{y + h/2 + 4.5:.1f}" text-anchor="middle" '
            f'font-family="{FONT_MONO}" font-size="13" font-weight="{"600" if spine else "500"}" fill="{t["text"]}">{escape(label)}</text>'
        )

    def path_edge(d, dashed=False, arrow=True):
        stroke = t["edge_dashed"] if dashed else t["edge_solid"]
        dash_attr = ' stroke-dasharray="5 4"' if dashed else ""
        mk = f' marker-end="url(#{"arr-dashed" if dashed else "arr-solid"})"' if arrow else ""
        parts.append(
            f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"{dash_attr}{mk}/>'
        )

    def edge_label(x, y, text, anchor="middle", dashed=False):
        color = t["muted"] if dashed else t["text"]
        parts.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-family="{FONT_SANS}" font-size="11.5" fill="{color}">{escape(text)}</text>'
        )

    # --- Subtle registries container (x=52..304, y=108..220) ---
    parts.append(
        f'<rect x="52" y="108" width="252" height="112" rx="12" '
        f'fill="{t["group_fill"]}" fill-opacity="{t["group_fill_opacity"]}" '
        f'stroke="{t["group_stroke"]}" stroke-width="1.1" stroke-dasharray="4 3"/>'
    )

    # === EDGES ===

    # 1. balancer-v3-erc4626-tests -. informs .-> metadata & code-review
    path_edge("M 176 58 L 176 88", dashed=True, arrow=False)
    path_edge("M 176 88 L 124 88 Q 116 88 116 96 L 116 117", dashed=True)
    path_edge("M 176 88 L 228 88 Q 236 88 236 96 L 236 117", dashed=True)
    edge_label(185, 77, "informs", anchor="start", dashed=True)

    # 2. Registries (all 4) -. raw main .-> backend
    path_edge("M 304 168 L 469 168", dashed=True)
    edge_label(396, 160, "raw main", anchor="middle", dashed=True)

    # 3. metadata -. raw main .-> frontend (clean outer-left channel)
    path_edge("M 64 139 L 26 139 Q 18 139 18 147 L 18 440 Q 18 448 26 448 L 469 448", dashed=True)
    edge_label(220, 440, "raw main", anchor="middle", dashed=True)

    # 4. subgraphs -> backend (Ormi GraphQL)
    path_edge("M 536 58 L 536 157", dashed=False)
    edge_label(545, 112, "Ormi GraphQL", anchor="start", dashed=False)

    # 5. deployments -.-> subgraphs, backend, sdk
    path_edge("M 776 182 L 724 182", dashed=True, arrow=False)
    path_edge("M 724 182 L 724 47 Q 724 39 716 39 L 603 39", dashed=True)
    edge_label(733, 102, "manual + ABIs", anchor="start", dashed=True)
    path_edge("M 724 182 L 603 182", dashed=True)
    edge_label(662, 174, "sync-config", anchor="middle", dashed=True)
    path_edge("M 724 182 L 724 312 Q 724 320 716 320 L 603 320", dashed=True)
    edge_label(733, 258, "update:deployments", anchor="start", dashed=True)

    # 6. backend -> sdk & backend -> frontend (GraphQL + codegen)
    path_edge("M 524 204 L 524 252", dashed=False, arrow=False)
    path_edge("M 524 252 L 544 252 Q 552 252 552 260 L 552 297", dashed=False)
    # Clean gap around y=320 where maths->sdk crosses horizontally (true transparency on every theme)
    path_edge("M 524 252 L 494 252 Q 486 252 486 260 L 486 313", dashed=False, arrow=False)
    path_edge("M 486 327 L 486 417", dashed=False)
    edge_label(533, 234, "GraphQL + codegen", anchor="start", dashed=False)

    # 7. sdk -> frontend (npm)
    path_edge("M 552 340 L 552 417", dashed=False)
    edge_label(561, 383, "npm", anchor="start", dashed=False)

    # 8. maths -> backend, sdk, frontend (npm)
    path_edge("M 292 320 L 340 320", dashed=False, arrow=False)
    path_edge("M 340 320 L 340 202 Q 340 194 348 194 L 469 194", dashed=False)
    path_edge("M 340 320 L 501 320", dashed=False)
    path_edge("M 340 320 L 340 422 Q 340 430 348 430 L 469 430", dashed=False)
    edge_label(316, 311, "npm", anchor="middle", dashed=False)

    # === NODES ===
    node(52, 20, 252, 38, "balancer-v3-erc4626-tests")
    node(64, 120, 104, 38, "metadata")
    node(180, 120, 112, 38, "code-review")
    node(64, 170, 104, 38, "tokenlists")
    node(180, 170, 112, 38, "blocklist")
    node(176, 301, 116, 38, "maths")

    node(472, 20, 128, 38, "subgraphs", spine=True)
    node(472, 160, 128, 44, "backend", spine=True)
    node(504, 300, 96, 40, "sdk", spine=True)
    node(472, 420, 128, 40, "frontend", spine=True)

    node(776, 162, 124, 40, "deployments", spine=True)

    parts.append("</svg>\n")
    return "\n".join(parts)


for mode in ("light", "dark"):
    out = OUT_DIR / f"architecture-{mode}.svg"
    out.write_text(render_svg(mode))
    print(f"Wrote {out} ({out.stat().st_size} bytes)")
