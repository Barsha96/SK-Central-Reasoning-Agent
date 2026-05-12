"""Shared dark/light theming utilities for the PV Manufacturing app."""
from __future__ import annotations
import re
import streamlit as st

# ── Dark-to-light hex mapping ─────────────────────────────────────────────────
# All dark hex codes used across the app, mapped to their light equivalents.
# apply_theme() does a single regex pass to swap them when dark_mode is False.
_D2L: dict[str, str] = {
    # ── Introduction slide backgrounds ───────────────────────────────────
    "#0a0d14": "#f0f4fa", "#111827": "#ffffff",
    "#0f1a2a": "#edf3fb", "#0f1a1a": "#ecf8f4",
    "#1a0f1a": "#f7edfb", "#0a1020": "#e4eef8",
    "#0a120a": "#eaf6ea", "#1a1a0a": "#f8f6e4",
    "#1a0f0f": "#fdf0f0", "#0f1420": "#edf1fa",
    "#0a1a0a": "#e4f6e4",
    # ── Primary text ─────────────────────────────────────────────────────
    "#e8f0f8": "#1a2535", "#c8d8e8": "#253545",
    "#c8d8d8": "#253a3a", "#c8e8c8": "#1a4020",
    "#c8d8c8": "#1a3520", "#d8c8e8": "#3a2550",
    "#e8d0c0": "#503010", "#c8b0e8": "#4a18a0",
    "#e0e080": "#4a4a00", "#e0e0a0": "#4a4a00",
    # ── Muted / secondary text ────────────────────────────────────────────
    "#7a9ab8": "#4a6a8a", "#8ab0c8": "#2a5a70",
    "#a0b8d0": "#2a4a60", "#9a7070": "#6a2020",
    "#7a9a9a": "#2a5050", "#7a9a8a": "#2a4a3a",
    "#7a9a7a": "#2a4a2a", "#9a8ab0": "#4a2a7a",
    "#9a8070": "#4a3020", "#a07030": "#604010",
    "#a0a060": "#404010", "#a080c0": "#5020a0",
    "#5a7a9a": "#3a5a7a", "#4a6a9c": "#2a5a8a",
    # ── Accents ───────────────────────────────────────────────────────────
    "#5ab4e8": "#1a7ab8", "#50d4a0": "#0a7a50",
    "#f0a830": "#b07020", "#f0c060": "#906010",
    "#e05555": "#c02020", "#e87070": "#b03030",
    "#c080e0": "#7030b0",
    # ── Sector text ───────────────────────────────────────────────────────
    "#60a060": "#1a5a10", "#e8b060": "#9a5010",
    "#60e890": "#108040", "#60d4b8": "#087060",
    "#e09050": "#9a4010", "#c090e0": "#7030b0",
    # ── Borders ───────────────────────────────────────────────────────────
    "#1e2d45": "#c0cfe0", "#1e3a5a": "#b0cae0",
    "#1e3a5c": "#b0cae0", "#1a3a5a": "#b8d0e8",
    "#1a3a1a": "#80c080", "#3a3a0a": "#c0c060",
    "#2a6a9c": "#5090cc", "#2a7a5a": "#2a9a6a",
    "#7a3a9a": "#8a4aaa",
    # ── Small labels / badges ─────────────────────────────────────────────
    "#2a5a8a": "#2a6aa0", "#2a6a4a": "#2a7a4a",
    "#6a3a8a": "#7a4a98", "#3a6a9a": "#2a6aaa",
    "#3a8a5a": "#2a8a5a", "#3a6a8a": "#2a5a8a",
    "#4a6a8a": "#2a5a7a", "#4a6a4a": "#2a5020",
    "#2a4060": "#6a7a90", "#2a4a6a": "#8aa0b8",
    # ── Alpha / shadow ────────────────────────────────────────────────────
    "#f0a83066": "#b0702044", "#5ab4e888": "#1a7ab888",
    # ── Main app background (all non-intro pages) ─────────────────────────
    "#0f1117": "#f4f7fc",
    # ── Common text / label colors ────────────────────────────────────────
    "#556677": "#4a5a6a",
    "#8899aa": "#4a5568",
    "#7a8a9a": "#4a5568",
    "#7eb3d4": "#1a5a8a",
    "#8eb3d4": "#1a5a8a",
    "#a0d4ff": "#1a7ab8",
    "#888888": "#4a5a6a",
    # ── Metric pills / info cards ─────────────────────────────────────────
    "#1a1d27": "#f4f7fc",
    "#2a2d3a": "#c0cce0",
    # ── Flow diagram / sequence diagram nodes ─────────────────────────────
    "#1e2130": "#f0f4fa",
    "#2d3348": "#c0cce0",
    "#3a4060": "#8090a8",
    "#2a3050": "#c8d4e8",
    "#2a5020": "#c8e8c0",
    "#2a4a7a": "#4a7ab8",
    "#6a4a0a": "#8a6a1a",
    "#6a2a8a": "#8a4ab8",
    # ── SK / Agent architecture boxes ─────────────────────────────────────
    "#0f1f35": "#e8f2fa",
    "#0f1f0f": "#ecf8ec",
    "#1a2a0a": "#eaf6ea",
    "#1a1f0a": "#f4f8ec",
    "#1a0f1f": "#f7edfb",
    "#1f1a0a": "#f8f4ec",
    "#2a1a0a": "#f8f0e4",
    "#7a4a0a": "#9a6a1a",
    "#d4a060": "#9a5010",
    "#90d490": "#1a7a2a",
    "#4a6a0a": "#4a6a1a",
    "#a0d4a0": "#1a8a2a",
    "#8eb3b4": "#2a6a6a",
    "#4a2a6a": "#6a4a9a",
    # ── Stage-specific card colors (pv_stages.py) ─────────────────────────
    "#1a3a5c": "#b0cae0",
    "#1a2a4a": "#e0e8f8",
    "#2a4a8a": "#4070b8",
    "#3a1a0a": "#f8eae4",
    "#9a3a0a": "#c84a10",
    "#1a2a1a": "#eaf6ea",
    "#2a6a2a": "#2a8a2a",
    "#2a1a2a": "#f8eaf8",
    "#6a2a6a": "#8a4a8a",
    "#2a2a0a": "#f8f8e4",
    "#8a7a0a": "#706010",
    "#0a2a1a": "#e4f6f0",
    "#0a6a2a": "#1a8a3a",
    # ── Synthetic data ────────────────────────────────────────────────────
    "#2a5a2a": "#2a8a2a",
}


def apply_theme(html: str) -> str:
    """Replace dark hex codes with light equivalents when dark_mode is False."""
    if st.session_state.get("dark_mode", False):
        return html

    def _replace(m: re.Match) -> str:
        return _D2L.get(m.group(0).lower(), m.group(0))

    return re.sub(r'#[0-9a-fA-F]{8}|#[0-9a-fA-F]{6}', _replace, html, flags=re.IGNORECASE)


def page_css(extra: str = "") -> str:
    """Return the standard themed CSS block for a page."""
    dark = st.session_state.get("dark_mode", False)
    bg      = "#0f1117" if dark else "#f4f7fc"
    heading = "#7eb3d4" if dark else "#1a5a8a"

    light_overrides = "" if dark else """
    /* ── Light mode: fix Streamlit dark-theme text & input colors ── */

    /* Body text — paragraphs and list items everywhere */
    p, li { color: #1a2535 !important; }

    /* Streamlit markdown containers */
    .stMarkdown p, .stMarkdown li,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li { color: #1a2535 !important; }

    /* Expanders */
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] li { color: #1a2535 !important; }

    /* Chat message content */
    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] li { color: #1a2535 !important; }

    /* Tabs */
    .stTabs p, .stTabs li { color: #1a2535 !important; }

    /* Labels on form inputs */
    label { color: #1a2535 !important; }

    /* Selectbox dropdown */
    .stSelectbox > div > div,
    .stSelectbox > div > div > div { background-color: #ffffff !important; color: #1a2535 !important; }

    /* st.info / st.success / st.warning / st.error */
    [data-testid="stNotification"] div { color: #1a2535 !important; }

    /* Caption */
    .stCaption p, [data-testid="stCaptionContainer"] p { color: #4a5568 !important; }
    """

    return f"""
<style>
.stApp {{ background-color: {bg}; }}
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}
h1, h2, h3 {{ color: {heading} !important; }}
.block-container {{ padding-top: 1rem !important; }}
{light_overrides}
{extra}
</style>
"""


def plotly_colors() -> tuple[str, str, str]:
    """Return (background, gridcolor, font_color) for the current theme."""
    dark = st.session_state.get("dark_mode", False)
    if dark:
        return "#0f1117", "#1a1d27", "#a0aec0"
    return "#f4f7fc", "#dde4f0", "#4a5568"


def heatmap_colorscale() -> list[list]:
    """Return Plotly colorscale for the metric-fault heatmap."""
    dark = st.session_state.get("dark_mode", False)
    if dark:
        return [
            [0.0,  "#0f1117"],
            [0.01, "#1a2a3a"],
            [0.3,  "#1a5276"],
            [0.6,  "#d4a017"],
            [1.0,  "#c0392b"],
        ]
    return [
        [0.0,  "#f4f7fc"],
        [0.01, "#d0e4f8"],
        [0.3,  "#6abaeb"],
        [0.6,  "#d4a017"],
        [1.0,  "#c0392b"],
    ]
