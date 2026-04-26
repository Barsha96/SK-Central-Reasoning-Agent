"""
Synthetic Data Documentation Page
Accessible at /synthetic_data in the Streamlit app.
"""
import json
import random
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
import streamlit as st

# ── Global style ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background-color: #0f1117; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }
h1, h2, h3 { color: #7eb3d4 !important; }
.block-container { padding-top: 1rem !important; }
.disclaimer-box {
    background: #1a2a1a; border: 1px solid #2a5a2a;
    border-radius: 8px; padding: 14px 18px; margin-bottom: 16px;
}
.stage-chip {
    display: inline-block; padding: 2px 10px;
    border-radius: 12px; font-size: 11px; font-weight: 600;
    background: #1a3a5c; color: #7eb3d4; margin-right: 6px;
}
</style>
""", unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────────────────────
CONFIG_DIR = Path(__file__).parent.parent / "config"

@st.cache_data
def load_configs():
    with open(CONFIG_DIR / "metrics.json", encoding="utf-8") as f:
        metrics = json.load(f)
    with open(CONFIG_DIR / "fault_scenarios.json", encoding="utf-8") as f:
        scenarios = json.load(f)
    return metrics, scenarios

METRICS, SCENARIOS = load_configs()

STAGE_NAMES = {
    1: "Surface Preparation",
    2: "PVD Deposition",
    3: "CdCl₂ Activation",
    4: "Grain Growth",
    5: "Back Contact",
    6: "Laser Scribing",
    7: "QA Testing",
}

STAGE_COLORS = {
    1: "#2ecc71", 2: "#3498db", 3: "#e67e22",
    4: "#9b59b6", 5: "#1abc9c", 6: "#e74c3c", 7: "#f39c12",
}

SEVERITY_COLOR = {"High": "#e74c3c", "Medium": "#f39c12", "Low": "#27ae60"}


def generate_normal_samples(meta: dict, n: int = 300) -> np.ndarray:
    lo, hi = meta["normal_min"], meta["normal_max"]
    if lo == hi:
        return np.full(n, lo, dtype=float)
    mid  = (lo + hi) / 2
    std  = (hi - lo) / 5
    samples = np.random.normal(mid, std, n)
    return np.clip(samples, lo - std * 0.5, hi + std * 0.5)


def step_label(key: str) -> str:
    meta = METRICS[key]
    return f"{key.replace('step_','Step ')} · {meta['name']}"


# ── Header ───────────────────────────────────────────────────────────────────
st.title("📊 Synthetic Data Documentation")

st.markdown("""
<div class="disclaimer-box">
<strong>⚠️ This is entirely synthetic data.</strong><br>
All sensor readings shown in this system are <em>artificially generated</em> to simulate a CdTe/CIGS
solar panel manufacturing line. No real manufacturing equipment or production data is used.
The data is designed to be physically plausible — parameter ranges, units, and fault thresholds
are grounded in published PV manufacturing literature — but it does <strong>not</strong> represent
any real facility or product.
</div>
""", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Metrics Catalog",
    "📈 Distributions",
    "⚡ Fault Scenarios",
    "🔗 Metric–Fault Mapping",
    "🧪 Injected Data Samples",
])


# ═══════════════════════════════════════════════════════════════════════════
# TAB 1 — METRICS CATALOG
# ═══════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## Metrics Catalog")
    st.markdown(
        "The simulation tracks **50 sensor parameters** across 7 manufacturing stages. "
        "Each metric has a defined normal operating range and a fault threshold — "
        "exceeding the threshold triggers the centralized reasoning agent."
    )

    stage_filter = st.selectbox(
        "Filter by stage",
        options=["All stages"] + [f"Stage {i}: {STAGE_NAMES[i]}" for i in range(1, 8)],
        key="catalog_stage_filter",
    )
    selected_stage = None
    if stage_filter != "All stages":
        selected_stage = int(stage_filter.split(":")[0].replace("Stage ", "").strip())

    rows = []
    for key, meta in METRICS.items():
        if selected_stage and meta["stage"] != selected_stage:
            continue
        normal_range = (
            f"{meta['normal_min']} – {meta['normal_max']}"
            if meta["normal_min"] != meta["normal_max"]
            else str(meta["normal_min"])
        )
        fault_cond = (
            f"> {meta['fault_threshold']}"
            if meta["fault_direction"] == "above"
            else f"< {meta['fault_threshold']}"
        )
        rows.append({
            "Step":        key.replace("step_", ""),
            "Stage":       f"{meta['stage']} · {STAGE_NAMES[meta['stage']]}",
            "Parameter":   meta["name"],
            "Unit":        meta["unit"],
            "Normal Range":normal_range,
            "Fault if":    fault_cond,
            "What it means": meta["plain_english"],
            "Fault type":  meta["error_type"],
        })

    import pandas as pd
    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Step":          st.column_config.TextColumn(width="small"),
            "Stage":         st.column_config.TextColumn(width="medium"),
            "Parameter":     st.column_config.TextColumn(width="medium"),
            "Unit":          st.column_config.TextColumn(width="small"),
            "Normal Range":  st.column_config.TextColumn(width="medium"),
            "Fault if":      st.column_config.TextColumn(width="small"),
            "What it means": st.column_config.TextColumn(width="large"),
            "Fault type":    st.column_config.TextColumn(width="medium"),
        },
    )

    st.caption(f"Showing {len(rows)} of 50 metrics.")


# ═══════════════════════════════════════════════════════════════════════════
# TAB 2 — DISTRIBUTIONS
# ═══════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("## Data Distributions")
    st.markdown(
        "Each chart shows **300 simulated normal readings** (blue) for a metric. "
        "The red dashed line marks the **fault threshold**. "
        "Orange markers show where **fault-injected values** land relative to the normal distribution."
    )

    selected_stage_dist = st.radio(
        "Select manufacturing stage",
        options=[f"Stage {i}: {STAGE_NAMES[i]}" for i in range(1, 8)],
        horizontal=True,
        key="dist_stage",
    )
    stage_num_dist = int(selected_stage_dist.split(":")[0].replace("Stage ", "").strip())

    stage_metrics = {k: v for k, v in METRICS.items() if v["stage"] == stage_num_dist}

    # Gather all fault values for metrics in this stage across all scenarios
    fault_overlay: dict[str, list[tuple[str, float]]] = {k: [] for k in stage_metrics}
    for sc in SCENARIOS:
        for step_key, val in sc["injected_faults"].items():
            if step_key in fault_overlay:
                fault_overlay[step_key].append((sc["display_name"], val))

    n_metrics = len(stage_metrics)
    cols_per_row = 3
    rows_needed  = (n_metrics + cols_per_row - 1) // cols_per_row

    keys_list = list(stage_metrics.keys())
    for row_i in range(rows_needed):
        cols = st.columns(cols_per_row)
        for col_i in range(cols_per_row):
            idx = row_i * cols_per_row + col_i
            if idx >= n_metrics:
                break
            step_key = keys_list[idx]
            meta     = stage_metrics[step_key]

            samples = generate_normal_samples(meta, 300)
            lo, hi  = meta["normal_min"], meta["normal_max"]
            threshold = meta["fault_threshold"]

            fig = go.Figure()

            # Normal distribution histogram
            fig.add_trace(go.Histogram(
                x=samples,
                nbinsx=30,
                marker_color=STAGE_COLORS[stage_num_dist],
                opacity=0.75,
                name="Normal readings",
                showlegend=False,
            ))

            # Fault threshold line
            fig.add_vline(
                x=threshold,
                line_dash="dash",
                line_color="#e74c3c",
                line_width=2,
                annotation_text="Fault threshold",
                annotation_font_color="#e74c3c",
                annotation_font_size=9,
            )

            # Normal range shading
            fig.add_vrect(
                x0=lo, x1=hi,
                fillcolor="rgba(100,200,100,0.07)",
                line_width=0,
                annotation_text="Normal range",
                annotation_font_size=8,
                annotation_font_color="#5a9",
            )

            # Fault-injected overlays
            for sc_name, fault_val in fault_overlay.get(step_key, []):
                fig.add_vline(
                    x=fault_val,
                    line_dash="dot",
                    line_color="#f39c12",
                    line_width=1.5,
                    annotation_text=sc_name[:14],
                    annotation_font_color="#f39c12",
                    annotation_font_size=7,
                    annotation_position="top right",
                )

            fig.update_layout(
                title=dict(text=f"{meta['name']}<br><sup>{meta['unit']}</sup>", font_size=11),
                height=200,
                margin=dict(l=30, r=10, t=45, b=30),
                paper_bgcolor="#0f1117",
                plot_bgcolor="#0f1117",
                font_color="#a0aec0",
                xaxis=dict(showgrid=True, gridcolor="#1a1d27"),
                yaxis=dict(showgrid=True, gridcolor="#1a1d27", title="Count"),
            )

            with cols[col_i]:
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                st.caption(f"_{meta['plain_english']}_")


# ═══════════════════════════════════════════════════════════════════════════
# TAB 3 — FAULT SCENARIOS
# ═══════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("## Fault Scenarios")
    st.markdown(
        "The simulation randomly selects one of **10 pre-defined fault scenarios** "
        "and injects it after ~20 seconds of normal operation. Each scenario represents "
        "a real failure mode observed in CdTe/CIGS solar panel manufacturing."
    )

    for sc in SCENARIOS:
        severity_color = SEVERITY_COLOR.get(sc.get("severity", "Medium"), "#f39c12")
        with st.expander(
            f"⚡ **{sc['display_name']}** — Stage {sc['stage']}: {sc['stage_name']}",
            expanded=False,
        ):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**Plain English:** {sc['plain_english']}")
                st.markdown(f"**Technical Description:** {sc['description']}")

                st.markdown("**Metrics injected out of range:**")
                for step_key, val in sc["injected_faults"].items():
                    meta = METRICS.get(step_key, {})
                    direction = "above" if meta.get("fault_direction") == "above" else "below"
                    st.markdown(
                        f"- `{step_key}` **{meta.get('name', step_key)}**: "
                        f"injected as **{val} {meta.get('unit','')}** "
                        f"(fault threshold: {direction} {meta.get('fault_threshold','')})"
                    )

                st.markdown(
                    f"**Primary expert consulted:** {sc['primary_expert'].replace('_', ' ').title()}"
                )
                if sc.get("secondary_expert"):
                    st.markdown(
                        f"**Cross-check expert:** {sc['secondary_expert'].replace('_', ' ').title()}"
                    )

            with col_b:
                st.markdown(
                    f"<div style='text-align:center; padding: 16px; background:#1a1d27; "
                    f"border-radius:8px; border: 2px solid {severity_color};'>"
                    f"<div style='font-size:11px; color:#888; text-transform:uppercase; letter-spacing:1px;'>Severity</div>"
                    f"<div style='font-size:22px; font-weight:800; color:{severity_color};'>"
                    f"{sc.get('severity','Medium')}</div>"
                    f"<div style='font-size:11px; color:#888; margin-top:8px;'>Stage</div>"
                    f"<div style='font-size:16px; font-weight:700; color:#7eb3d4;'>{sc['stage']}</div>"
                    f"<div style='font-size:10px; color:#7eb3d4;'>{sc['stage_name']}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )


# ═══════════════════════════════════════════════════════════════════════════
# TAB 4 — METRIC–FAULT MAPPING
# ═══════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## Metric–Fault Mapping")
    st.markdown(
        "This matrix shows which **sensor metrics are involved in each fault scenario**. "
        "A filled cell means that metric is directly injected out of range when that fault occurs. "
        "Use this to understand why the reasoning agent consults specific experts."
    )

    # Build matrix: rows = metrics that appear in at least one scenario, cols = scenarios
    involved_steps = set()
    for sc in SCENARIOS:
        involved_steps.update(sc["injected_faults"].keys())

    involved_steps = sorted(involved_steps, key=lambda k: int(k.replace("step_", "")))
    scenario_names = [sc["display_name"] for sc in SCENARIOS]

    # Build z matrix (1 = metric injected in this scenario, 0 = not)
    z = []
    y_labels = []
    for step_key in involved_steps:
        meta = METRICS[step_key]
        row = []
        for sc in SCENARIOS:
            row.append(1 if step_key in sc["injected_faults"] else 0)
        z.append(row)
        y_labels.append(f"{step_key.replace('step_','S')} · {meta['name']}")

    # Custom colors per scenario severity
    z_color = []
    for step_key in involved_steps:
        row = []
        for sc in SCENARIOS:
            if step_key in sc["injected_faults"]:
                sev = sc.get("severity", "Medium")
                row.append({"High": 1.0, "Medium": 0.6, "Low": 0.3}.get(sev, 0.6))
            else:
                row.append(0.0)
        z_color.append(row)

    fig_map = go.Figure(go.Heatmap(
        z=z_color,
        x=scenario_names,
        y=y_labels,
        colorscale=[
            [0.0,  "#0f1117"],
            [0.01, "#1a2a3a"],
            [0.3,  "#1a5276"],
            [0.6,  "#d4a017"],
            [1.0,  "#c0392b"],
        ],
        showscale=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Fault scenario: <b>%{x}</b><br>"
            "<extra></extra>"
        ),
    ))

    fig_map.update_layout(
        height=max(320, len(involved_steps) * 28),
        margin=dict(l=10, r=10, t=20, b=120),
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font_color="#a0aec0",
        font_size=10,
        xaxis=dict(
            tickangle=-40,
            tickfont_size=10,
            side="bottom",
        ),
        yaxis=dict(
            tickfont_size=10,
            autorange="reversed",
        ),
    )

    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("""
**Legend:**
- 🔴 **Red cell** = metric is directly injected as a fault value in this scenario (High severity)
- 🟡 **Yellow cell** = metric injected in a Medium severity scenario
- 🔵 **Blue cell** = metric injected in a Low severity scenario
- ⬛ **Empty cell** = metric is not part of this fault scenario
""")

    # Also show expert routing table
    st.markdown("### Expert Routing per Scenario")
    st.markdown("When a fault is detected, the triage agent routes to these specialist experts:")

    routing_rows = []
    for sc in SCENARIOS:
        routing_rows.append({
            "Fault Scenario":     sc["display_name"],
            "Stage":              f"{sc['stage']}: {sc['stage_name']}",
            "Primary Expert":     sc["primary_expert"].replace("_", " ").title(),
            "Cross-Check Expert": sc.get("secondary_expert", "—").replace("_", " ").title(),
            "Severity":           sc.get("severity", "—"),
        })

    import pandas as pd
    st.dataframe(
        pd.DataFrame(routing_rows),
        use_container_width=True,
        hide_index=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# TAB 5 — INJECTED DATA SAMPLES
# ═══════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("## Injected Data Samples")
    st.markdown(
        "This tab shows **exactly how a fault is injected** into the sensor stream. "
        "Select a scenario below to see the before/after: "
        "what the metric normally reads, what the fault-injected value is, "
        "and how far it deviates from the normal range."
    )

    scenario_names_sel = [sc["display_name"] for sc in SCENARIOS]
    selected_sc_name   = st.selectbox("Select a fault scenario", scenario_names_sel, key="inj_sc")
    sc = next(s for s in SCENARIOS if s["display_name"] == selected_sc_name)

    # Header card
    sev_col = SEVERITY_COLOR.get(sc.get("severity", "Medium"), "#f39c12")
    st.markdown(
        f"<div style='background:#1a1d27; border:1.5px solid {sev_col}; border-radius:8px; "
        f"padding:14px 18px; margin-bottom:12px;'>"
        f"<strong style='color:{sev_col}; font-size:16px;'>{sc['display_name']}</strong>"
        f"<span style='float:right; background:{sev_col}; color:white; font-size:11px; "
        f"font-weight:700; padding:2px 10px; border-radius:12px;'>{sc.get('severity','')}</span>"
        f"<br><span style='color:#888; font-size:12px;'>Stage {sc['stage']}: {sc['stage_name']}</span>"
        f"<br><br><span style='color:#c0c0c0;'>{sc['plain_english']}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Per-metric comparison
    comparison_rows = []
    for step_key, injected_val in sc["injected_faults"].items():
        meta   = METRICS.get(step_key, {})
        lo, hi = meta.get("normal_min", 0), meta.get("normal_max", 1)
        mid    = (lo + hi) / 2
        std    = max((hi - lo) / 5, 0.001)
        normal_sample = round(float(np.random.normal(mid, std)), 4)
        normal_sample = max(lo, min(hi, normal_sample))

        threshold  = meta.get("fault_threshold", 0)
        direction  = meta.get("fault_direction", "above")
        is_fault   = (
            (direction == "above" and injected_val > threshold) or
            (direction == "below" and injected_val < threshold)
        )

        if lo != hi:
            deviation_pct = round(abs(injected_val - mid) / ((hi - lo) / 2) * 100, 1)
        else:
            deviation_pct = 0.0

        comparison_rows.append({
            "step_key":      step_key,
            "name":          meta.get("name", step_key),
            "unit":          meta.get("unit", ""),
            "normal_range":  f"{lo} – {hi}",
            "normal_sample": normal_sample,
            "injected_val":  injected_val,
            "threshold":     f"{'>' if direction == 'above' else '<'} {threshold}",
            "is_fault":      is_fault,
            "deviation_pct": deviation_pct,
            "plain_english": meta.get("plain_english", ""),
        })

    # Bar chart: normal sample vs injected value
    fig_inj = go.Figure()
    x_labels = [f"{r['step_key'].replace('step_','S')} {r['name']}" for r in comparison_rows]

    fig_inj.add_trace(go.Bar(
        name="Normal sample",
        x=x_labels,
        y=[r["normal_sample"] for r in comparison_rows],
        marker_color="#3498db",
        opacity=0.8,
    ))
    fig_inj.add_trace(go.Bar(
        name="Fault-injected value",
        x=x_labels,
        y=[r["injected_val"] for r in comparison_rows],
        marker_color="#e74c3c",
        opacity=0.9,
    ))

    fig_inj.update_layout(
        barmode="group",
        height=320,
        margin=dict(l=10, r=10, t=30, b=80),
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font_color="#a0aec0",
        legend=dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(tickangle=-30, tickfont_size=10, gridcolor="#1a1d27"),
        yaxis=dict(gridcolor="#1a1d27"),
        title="Normal Readings vs Fault-Injected Values",
    )

    st.plotly_chart(fig_inj, use_container_width=True)

    # Detailed table
    st.markdown("### Detailed Comparison")
    import pandas as pd

    table_rows = []
    for r in comparison_rows:
        table_rows.append({
            "Parameter":        r["name"],
            "Unit":             r["unit"],
            "Normal Range":     r["normal_range"],
            "Normal Sample":    r["normal_sample"],
            "Injected Value":   r["injected_val"],
            "Fault Threshold":  r["threshold"],
            "Deviation":        f"{r['deviation_pct']}%",
            "Status":           "🔴 FAULT" if r["is_fault"] else "⚠️ WARNING",
            "What it measures": r["plain_english"],
        })

    df_comparison = pd.DataFrame(table_rows)
    st.dataframe(df_comparison, use_container_width=True, hide_index=True)

    # Narrative explanation
    st.markdown("### How the Fault is Detected")
    fault_step_names = [r["name"] for r in comparison_rows if r["is_fault"]]
    st.info(
        f"When this scenario activates, the simulator replaces the normal readings for "
        f"**{', '.join(fault_step_names)}** with the injected fault values shown above. "
        f"The simulator continuously checks all 50 metrics against their thresholds. "
        f"As soon as any metric crosses its threshold, the fault flag is raised and the "
        f"centralized reasoning agent is triggered automatically."
    )
