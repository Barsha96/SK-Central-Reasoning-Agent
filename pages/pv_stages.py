"""PV Manufacturing Stages — educational overview page."""
import streamlit as st
from utils.theme import apply_theme, page_css

st.markdown(page_css(), unsafe_allow_html=True)

STAGES = [
    {
        "id": 1,
        "icon": "🧹",
        "name": "Surface Preparation",
        "subtitle": "Cleaning & Texturing the Substrate",
        "color": "#1a3a5c",
        "border": "#2a6a9c",
        "what": (
            "The manufacturing process begins with a glass substrate that must be made perfectly clean "
            "and optically rough. Chemical cleaning removes organic contaminants, metal ions, and "
            "particulates. Mechanical texturing etches a micro-pyramid structure into the surface, "
            "which traps incoming light and reduces reflection losses — a phenomenon called **light trapping**."
        ),
        "why": (
            "Even a single dust particle or oil smear at this stage causes a permanent defect in every "
            "subsequent layer deposited on top of it. Surface texture directly determines how much "
            "sunlight the finished cell can absorb."
        ),
        "metrics": [
            ("Particle Density", "particles/cm²", "Must be < 10 after cleaning"),
            ("O₂ Concentration", "ppm", "Residual oxygen causes oxidation of contact surfaces"),
            ("Engagement Status", "binary", "Safety interlock confirming chamber is sealed"),
        ],
        "key_physics": "Light trapping via total internal reflection at textured surface increases effective optical path length by ~4n² (Lambertian limit, n ≈ 3.5 for Si).",
    },
    {
        "id": 2,
        "icon": "⚗️",
        "name": "PVD Deposition",
        "subtitle": "Physical Vapor Deposition of Semiconductor Layers",
        "color": "#1a2a4a",
        "border": "#2a4a8a",
        "what": (
            "In a high-vacuum chamber (< 10⁻⁵ Torr), semiconductor source material — cadmium telluride "
            "(CdTe) or CIGS — is evaporated and condenses onto the moving substrate as a thin polycrystalline film. "
            "The CdS window layer (∼80 nm) is deposited first, followed by the CdTe absorber layer (∼3–5 µm). "
            "Substrate temperature, source temperature, and belt speed are tightly controlled."
        ),
        "why": (
            "This is the core semiconductor junction. Layer thickness, composition uniformity, "
            "and adhesion directly determine the cell's open-circuit voltage (Voc) and short-circuit "
            "current (Jsc). A vacuum leak mid-deposition can ruin an entire batch."
        ),
        "metrics": [
            ("Chamber Pressure", "Torr", "Leak detection — must stay below 10⁻⁵ Torr"),
            ("Deposition Rate", "nm/s", "Controls absorber layer thickness"),
            ("Layer Uniformity", "%", "Thickness variation across substrate width"),
            ("Layer Adhesion", "MPa", "Cohesive strength of deposited film"),
            ("Substrate Temperature", "°C", "Affects crystal grain size during deposition"),
        ],
        "key_physics": "CdTe band gap = 1.45 eV — nearly ideal for the AM1.5 solar spectrum. Deposition rate × belt speed = final film thickness.",
    },
    {
        "id": 3,
        "icon": "🔥",
        "name": "CdCl₂ Activation",
        "subtitle": "Heat Treatment to Improve the p-n Junction",
        "color": "#3a1a0a",
        "border": "#9a3a0a",
        "what": (
            "The as-deposited CdTe film has poor electronic quality. Cadmium chloride (CdCl₂) solution "
            "is applied to the surface and the substrate is heated to ∼400°C in air. This treatment "
            "causes chlorine atoms to diffuse along grain boundaries, passivating defects and promoting "
            "recrystallization. It also interdiffuses the CdS/CdTe interface, forming a graded "
            "CdS₁₋ₓTeₓ layer that improves junction quality."
        ),
        "why": (
            "Without CdCl₂ treatment, cell efficiency is typically < 5%. After treatment it rises to "
            "12–22%. This is the single most critical process step in CdTe manufacturing. "
            "Temperature uniformity across the substrate is essential — hot spots cause localized "
            "over-recrystallization while cold spots leave the junction incomplete."
        ),
        "metrics": [
            ("Temperature Uniformity ΔT", "°C", "Max allowed variation across substrate is ±2°C"),
            ("CdCl₂ Surface Coverage", "%", "Incomplete coverage = non-uniform activation"),
            ("New Defect Formation Rate", "defects/cm²/s", "Side-effect monitoring"),
            ("Temperature Stability", "°C std dev", "Oven control feedback signal"),
        ],
        "key_physics": "Cl⁻ ions at grain boundaries reduce recombination velocity from ~10⁶ cm/s to ~10³ cm/s — a 1000× improvement in minority carrier lifetime.",
    },
    {
        "id": 4,
        "icon": "🔬",
        "name": "Grain Growth",
        "subtitle": "Recrystallization for Higher Conductivity",
        "color": "#1a2a1a",
        "border": "#2a6a2a",
        "what": (
            "A controlled thermal anneal step grows the polycrystalline CdTe grains from their initial "
            "nanometer-scale size to 1–5 µm diameter. Larger grains mean fewer grain boundaries, "
            "which are the primary sites where photo-generated electron-hole pairs recombine before "
            "they can be collected as useful current. The process is monitored via in-situ X-ray "
            "diffraction or optical scattering."
        ),
        "why": (
            "Grain boundary recombination is the dominant efficiency loss mechanism in polycrystalline "
            "thin-film cells. Doubling average grain diameter can increase carrier collection efficiency "
            "by 15–20%. Too-rapid grain growth causes stress fractures in the film."
        ),
        "metrics": [
            ("Average Grain Diameter", "µm", "Target: 1–5 µm; < 0.5 µm triggers fault"),
            ("ΔT Achieved", "°C", "Anneal temperature accuracy vs. setpoint"),
            ("Grain Size Increase", "%", "Growth ratio relative to pre-anneal baseline"),
        ],
        "key_physics": "Grain growth rate ∝ exp(−Eₐ/kT), where Eₐ ≈ 1.2 eV for CdTe. Precise temperature control is essential to hit the target grain size window.",
    },
    {
        "id": 5,
        "icon": "🔩",
        "name": "Back Contact",
        "subtitle": "Metal Electrode Deposition",
        "color": "#2a1a2a",
        "border": "#6a2a6a",
        "what": (
            "A metal back contact layer — typically copper-doped zinc telluride (ZnTe:Cu) followed by "
            "a molybdenum or gold capping layer — is sputtered onto the rear surface of the CdTe. "
            "A critical concern is copper diffusion: too much Cu improves conductivity but too much "
            "migrates into the junction and acts as a deep-level recombination centre, "
            "degrading long-term stability."
        ),
        "why": (
            "The back contact forms the ohmic junction with the p-type CdTe. A poor contact "
            "creates a Schottky barrier that blocks current flow and lowers fill factor. "
            "Cu cross-contamination at this stage is invisible until the finished module "
            "shows accelerated degradation under IEC 61215 damp-heat testing."
        ),
        "metrics": [
            ("Back Contact Layer Quality", "score 0–1", "Composite adhesion + resistivity score"),
            ("Cu/Te Element Diffusion", "nm/min", "Rate of copper migration into absorber"),
            ("Current Density", "mA/cm²", "In-situ IV probe after contact deposition"),
        ],
        "key_physics": "Work function matching: CdTe valence band ≈ 5.7 eV. ZnTe back contact work function ≈ 5.8 eV — near-ideal ohmic contact with < 0.1 eV barrier.",
    },
    {
        "id": 6,
        "icon": "⚡",
        "name": "Laser Scribing",
        "subtitle": "Monolithic Interconnection of Cells",
        "color": "#2a2a0a",
        "border": "#8a7a0a",
        "what": (
            "A pulsed UV or green laser cuts precise isolation grooves (P1, P2, P3 scribes) through "
            "the layer stack to define individual cells and connect them in series — this is the "
            "monolithic integration that makes thin-film modules different from silicon wafer modules. "
            "P1 scribes through the front TCO, P2 through the CdTe absorber, and P3 isolates the "
            "back contact. Line width is typically 50–100 µm with ±5 µm positional accuracy."
        ),
        "why": (
            "Scribing errors — wavy lines, debris, or incorrect depth — create short circuits between "
            "adjacent cells, causing that entire series string to produce zero power. "
            "The dead area from scribing (inactive width between cells) directly reduces module aperture "
            "efficiency. Stress from laser pulses can propagate micro-cracks into surrounding semiconductor."
        ),
        "metrics": [
            ("Line Deviation", "µm", "Positional error from target path; fault > 5 µm"),
            ("Defect Recurrence Rate", "defects/m", "Repeated scribing errors per linear meter"),
            ("Mechanical Stress", "MPa", "Laser-induced stress in surrounding film"),
        ],
        "key_physics": "Laser fluence must exceed CdTe ablation threshold (∼0.1 J/cm²) but stay below glass damage threshold (∼10 J/cm²) — a 100× process window.",
    },
    {
        "id": 7,
        "icon": "✅",
        "name": "QA Testing",
        "subtitle": "Final Electrical Characterization",
        "color": "#0a2a1a",
        "border": "#0a6a2a",
        "what": (
            "Each finished module passes through a solar simulator (Class AAA, AM1.5G, 1000 W/m², "
            "25°C) for current-voltage (IV) curve measurement. Key parameters extracted: power "
            "conversion efficiency (η), fill factor (FF), open-circuit voltage (Voc), and "
            "short-circuit current (Isc). Electroluminescence imaging detects local shunts or "
            "broken interconnects invisible to IV measurement alone."
        ),
        "why": (
            "This is the final gate before modules ship. A module failing here has consumed "
            "all upstream processing cost. QA data feeds back to process control — a "
            "systematic shift in average η or FF triggers an investigation upstream. "
            "False negatives (passing a bad module) are caught by field returns; "
            "false positives (failing a good module) waste yield."
        ),
        "metrics": [
            ("Conversion Efficiency η", "%", "Target ≥ 15%; fault threshold < 12%"),
            ("Fill Factor FF", "0–1", "Measure of IV curve squareness; target > 0.70"),
            ("Reject Rate", "%", "Fraction of modules failing IV test"),
            ("Pmax Reduction", "%", "Degradation vs. nominal rated power"),
            ("False Negative Rate", "%", "Escaped defects that pass IV but fail field"),
        ],
        "key_physics": "FF = (Vmp × Jmp) / (Voc × Jsc). Theoretical limit ≈ 0.89 for ideal diode. Practical CdTe: 0.70–0.80. Shunts lower FF; series resistance lowers Vmp.",
    },
]

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("# ☀️ PV Manufacturing Stages")
st.markdown(
    "Solar panels are not made in a single step — they pass through seven carefully controlled "
    "manufacturing stages, each adding or refining a critical layer of the photovoltaic device. "
    "This page explains what happens at each stage, why it matters, and which sensor parameters "
    "the AI control system monitors in real time."
)

st.markdown("---")

# ── Production flow diagram ───────────────────────────────────────────────────
st.markdown("### Production Flow")
_FLOW_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: transparent; font-family: 'Segoe UI', sans-serif; padding: 8px 0; }
.flow { display: flex; align-items: center; justify-content: center; flex-wrap: nowrap; gap: 0; }
.flow-node {
  background: #1e2130; border: 1.5px solid #2d3348;
  border-radius: 8px; padding: 8px 10px; text-align: center;
  min-width: 90px; flex-shrink: 0;
}
.flow-node .ficon { font-size: 20px; }
.flow-node .fname { font-size: 9px; color: #8eb3d4; font-weight: 700; margin-top: 3px; line-height: 1.2; }
.arrow { color: #3a4060; font-size: 18px; padding: 0 4px; flex-shrink: 0; }
</style></head><body>
<div class="flow">
  <div class="flow-node"><div class="ficon">🧹</div><div class="fname">Surface<br>Prep</div></div>
  <div class="arrow">→</div>
  <div class="flow-node"><div class="ficon">⚗️</div><div class="fname">PVD<br>Deposition</div></div>
  <div class="arrow">→</div>
  <div class="flow-node"><div class="ficon">🔥</div><div class="fname">CdCl₂<br>Activation</div></div>
  <div class="arrow">→</div>
  <div class="flow-node"><div class="ficon">🔬</div><div class="fname">Grain<br>Growth</div></div>
  <div class="arrow">→</div>
  <div class="flow-node"><div class="ficon">🔩</div><div class="fname">Back<br>Contact</div></div>
  <div class="arrow">→</div>
  <div class="flow-node"><div class="ficon">⚡</div><div class="fname">Laser<br>Scribing</div></div>
  <div class="arrow">→</div>
  <div class="flow-node"><div class="ficon">✅</div><div class="fname">QA<br>Testing</div></div>
</div>
</body></html>
"""
st.components.v1.html(apply_theme(_FLOW_HTML), height=90)

st.markdown("---")

# ── Stage detail cards ────────────────────────────────────────────────────────
for stage in STAGES:
    with st.container():
        st.markdown(
            apply_theme(f"""
<div style="
  background: {stage['color']}22;
  border: 1.5px solid {stage['border']};
  border-radius: 10px;
  padding: 18px 22px 14px;
  margin-bottom: 18px;
">
  <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
    <span style="font-size:36px; line-height:1;">{stage['icon']}</span>
    <div>
      <div style="font-size:11px; color:#556677; text-transform:uppercase; letter-spacing:2px; font-weight:700;">
        Stage {stage['id']}
      </div>
      <div style="font-size:20px; font-weight:800; color:#c8d8e8;">{stage['name']}</div>
      <div style="font-size:13px; color:#8899aa; margin-top:2px;">{stage['subtitle']}</div>
    </div>
  </div>
</div>
"""),
            unsafe_allow_html=True,
        )

        col_left, col_right = st.columns([3, 2])

        with col_left:
            st.markdown("**What happens here**")
            st.markdown(stage["what"])
            st.markdown("**Why it matters**")
            st.markdown(stage["why"])
            st.markdown(
                apply_theme(
                    f"<div style='background:#0f1117; border-left:3px solid {stage['border']}; "
                    f"padding:8px 12px; border-radius:4px; font-size:12px; color:#8899aa; margin-top:8px;'>"
                    f"⚛ <em>{stage['key_physics']}</em></div>"
                ),
                unsafe_allow_html=True,
            )

        with col_right:
            st.markdown("**Monitored parameters**")
            for metric_name, unit, note in stage["metrics"]:
                st.markdown(
                    apply_theme(
                        f"<div style='background:#1a1d27; border:1px solid #2a2d3a; border-radius:6px; "
                        f"padding:7px 10px; margin-bottom:6px;'>"
                        f"<span style='font-size:12px; font-weight:700; color:#a0d4ff;'>{metric_name}</span> "
                        f"<span style='font-size:11px; color:#556677;'>({unit})</span><br>"
                        f"<span style='font-size:11px; color:#7a8a9a;'>{note}</span>"
                        f"</div>"
                    ),
                    unsafe_allow_html=True,
                )

        st.markdown("---")

# ── Footer note ───────────────────────────────────────────────────────────────
st.markdown(
    apply_theme(
        "<div style='text-align:center; color:#556677; font-size:11px; margin-top:8px;'>"
        "All sensor thresholds and stage parameters reflect the control loop design described in the "
        "research paper. Switch to the <strong>Live Demo</strong> tab to see the AI agent respond "
        "to a real-time fault injection across these stages."
        "</div>"
    ),
    unsafe_allow_html=True,
)
