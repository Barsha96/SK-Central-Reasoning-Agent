"""Architecture Forum slide deck — Near-Closed Loop Control with Centralized Reasoning Agent."""
import streamlit as st
from utils.ppt_exporter import generate_intro_ppt
from utils.theme import _D2L, apply_theme, page_css
from datetime import datetime

# ── Theme ─────────────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "intro_slide" not in st.session_state:
    st.session_state.intro_slide = 0

dark = st.session_state.dark_mode
APP_BG = "#0a0d14" if dark else "#f0f4fa"

st.markdown(page_css(f"""
.stApp {{ background-color: {APP_BG} !important; }}
.block-container {{ padding-top: 1.5rem !important; padding-bottom: 0.5rem !important; }}
div[data-testid="stHorizontalBlock"] {{ gap: 6px; }}
"""), unsafe_allow_html=True)

TOTAL_SLIDES = 7


def go(delta: int) -> None:
    st.session_state.intro_slide = max(0, min(TOTAL_SLIDES - 1, st.session_state.intro_slide + delta))


# ── Slide definitions ─────────────────────────────────────────────────────────
SLIDES = [

    # ── 0: TITLE & AGENDA ────────────────────────────────────────────────────
    dict(
        bg="#0a0d14",
        html="""
<div style="min-height:460px;display:flex;flex-direction:column;justify-content:center;padding:22px 60px;">

  <div style="font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#4a6a9c;font-weight:700;margin-bottom:14px;">
    Architecture Forum · May 2026
  </div>

  <div style="font-size:36px;font-weight:900;color:#e8f0f8;line-height:1.15;margin-bottom:8px;">
    Near-Closed Loop Control with<br>
    <span style="color:#5ab4e8;">Centralized Reasoning Agent</span>
  </div>

  <div style="font-size:15px;color:#7a9ab8;margin-bottom:30px;font-weight:400;">
    A Multi-Agent AI System for Solar PV Manufacturing &nbsp;·&nbsp; Semantic Kernel + Claude Sonnet 4.6
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;max-width:960px;margin-bottom:28px;">

    <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:14px 16px;">
      <div style="font-size:11px;font-weight:800;color:#5ab4e8;text-transform:uppercase;letter-spacing:1px;">01</div>
      <div style="font-size:13px;font-weight:700;color:#c8d8e8;margin-top:3px;">Project Overview</div>
      <div style="font-size:10px;color:#5a7a9a;margin-top:3px;">Problem statement &amp; motivation</div>
    </div>

    <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:14px 16px;">
      <div style="font-size:11px;font-weight:800;color:#5ab4e8;text-transform:uppercase;letter-spacing:1px;">02</div>
      <div style="font-size:13px;font-weight:700;color:#c8d8e8;margin-top:3px;">System Architecture</div>
      <div style="font-size:10px;color:#5a7a9a;margin-top:3px;">Components, layers &amp; data flow</div>
    </div>

    <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:14px 16px;">
      <div style="font-size:11px;font-weight:800;color:#5ab4e8;text-transform:uppercase;letter-spacing:1px;">03</div>
      <div style="font-size:13px;font-weight:700;color:#c8d8e8;margin-top:3px;">Expert Agent Catalog</div>
      <div style="font-size:10px;color:#5a7a9a;margin-top:3px;">12 specialist domain agents</div>
    </div>

    <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:14px 16px;">
      <div style="font-size:11px;font-weight:800;color:#f0a830;text-transform:uppercase;letter-spacing:1px;">04</div>
      <div style="font-size:13px;font-weight:700;color:#c8d8e8;margin-top:3px;">Expert Selection &amp; Routing</div>
      <div style="font-size:10px;color:#5a7a9a;margin-top:3px;">How the triage agent decides</div>
    </div>

    <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:14px 16px;">
      <div style="font-size:11px;font-weight:800;color:#f0a830;text-transform:uppercase;letter-spacing:1px;">05</div>
      <div style="font-size:13px;font-weight:700;color:#c8d8e8;margin-top:3px;">Reasoning Chain</div>
      <div style="font-size:10px;color:#5a7a9a;margin-top:3px;">Triage → Expert → Cross-check</div>
    </div>

    <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:14px 16px;">
      <div style="font-size:11px;font-weight:800;color:#50d4a0;text-transform:uppercase;letter-spacing:1px;">06</div>
      <div style="font-size:13px;font-weight:700;color:#c8d8e8;margin-top:3px;">Live Demo</div>
      <div style="font-size:10px;color:#5a7a9a;margin-top:3px;">7-stage PV line fault detection</div>
    </div>

    <div style="background:#111827;border:1px solid #1e3a3a;border-left:3px solid #50d4a0;border-radius:8px;padding:14px 16px;grid-column:span 3;">
      <div style="font-size:11px;font-weight:800;color:#50d4a0;text-transform:uppercase;letter-spacing:1px;">07</div>
      <div style="font-size:13px;font-weight:700;color:#c8d8e8;margin-top:3px;">Routes Forward</div>
      <div style="font-size:10px;color:#5a7a9a;margin-top:3px;">Integration opportunities · First Solar context · Expert review</div>
    </div>

  </div>

  <div style="font-size:11px;color:#2a4a6a;">Barsha Upadhyaya &nbsp;·&nbsp; First Solar</div>
</div>
"""),

    # ── 1: SYSTEM ARCHITECTURE ────────────────────────────────────────────────
    dict(
        bg="#0a0d14",
        html="""
<div style="min-height:460px;display:flex;flex-direction:column;justify-content:center;padding:14px 52px 10px;">

  <div style="font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#4a6a9c;font-weight:700;margin-bottom:6px;">02 · System Architecture</div>
  <div style="font-size:26px;font-weight:900;color:#e8f0f8;line-height:1.2;margin-bottom:3px;">
    How the System is Designed
  </div>
  <div style="font-size:11px;color:#5a7a9a;margin-bottom:12px;">Four layers — UI, orchestration, reasoning, and domain expertise — with a live data feed from the simulator</div>

  <div style="display:grid;grid-template-columns:2fr 1fr;gap:14px;align-items:start;">

    <!-- Architecture flow diagram -->
    <div style="display:flex;flex-direction:column;gap:0;">

      <!-- Layer 2: SK -->
      <div style="background:#0f1f0f;border:1.5px solid #2a7a5a;border-radius:8px;padding:7px 14px;text-align:center;">
        <div style="font-size:9px;font-weight:800;color:#50d4a0;text-transform:uppercase;letter-spacing:2px;margin-bottom:1px;">Orchestration Layer</div>
        <div style="font-size:12px;font-weight:700;color:#c8d8e8;">Semantic Kernel (v1.5+)</div>
        <div style="font-size:9px;color:#4a8a6a;margin-top:1px;">AnthropicChatCompletion connector · Plugin registry · Streaming API</div>
      </div>

      <div style="text-align:center;font-size:14px;color:#2a7a5a;line-height:1.1;">↕</div>

      <!-- Layer 3: Central Reasoning Agent -->
      <div style="background:#1a0f1f;border:1.5px solid #7a3a9a;border-radius:8px;padding:7px 14px;display:flex;gap:12px;align-items:center;">
        <div style="flex:1;text-align:center;">
          <div style="font-size:9px;font-weight:800;color:#c080e0;text-transform:uppercase;letter-spacing:2px;margin-bottom:1px;">Reasoning Layer</div>
          <div style="font-size:12px;font-weight:700;color:#c8d8e8;">Central Reasoning Agent</div>
          <div style="font-size:9px;color:#7a4a9a;margin-top:1px;">Claude Sonnet 4.6 · Fault assessment · Expert routing</div>
        </div>
        <div style="display:flex;flex-direction:column;gap:3px;min-width:120px;">
          <div style="font-size:8px;background:#2a1a2a;border:1px solid #5a2a7a;border-radius:4px;padding:3px 7px;color:#c080e0;text-align:center;">## Fault Assessment</div>
          <div style="font-size:8px;background:#2a1a2a;border:1px solid #5a2a7a;border-radius:4px;padding:3px 7px;color:#c080e0;text-align:center;">## Why This Expert?</div>
          <div style="font-size:8px;background:#2a1a2a;border:1px solid #5a2a7a;border-radius:4px;padding:3px 7px;color:#c080e0;text-align:center;">## Initial Hypothesis</div>
        </div>
      </div>

      <div style="text-align:center;font-size:14px;color:#7a3a9a;line-height:1.1;">↕</div>

      <!-- Layer 4: Expert Agents -->
      <div style="background:#1f1a0a;border:1.5px solid #6a4a0a;border-radius:8px;padding:7px 14px;">
        <div style="font-size:9px;font-weight:800;color:#f0a830;text-transform:uppercase;letter-spacing:2px;margin-bottom:5px;text-align:center;">Expert Agent Pool</div>
        <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:4px;">
          <div style="background:#2a1a0a;border:1px solid #4a3a0a;border-radius:4px;padding:5px 4px;font-size:8px;color:#d4a060;text-align:center;line-height:1.3;">Defect<br>Reduction</div>
          <div style="background:#2a1a0a;border:1px solid #4a3a0a;border-radius:4px;padding:5px 4px;font-size:8px;color:#d4a060;text-align:center;line-height:1.3;">Efficiency</div>
          <div style="background:#2a1a0a;border:1px solid #4a3a0a;border-radius:4px;padding:5px 4px;font-size:8px;color:#d4a060;text-align:center;line-height:1.3;">Grain<br>Optimization</div>
          <div style="background:#2a1a0a;border:1px solid #4a3a0a;border-radius:4px;padding:5px 4px;font-size:8px;color:#d4a060;text-align:center;line-height:1.3;">Uniformity<br>Correction</div>
          <div style="background:#2a1a0a;border:1px solid #4a3a0a;border-radius:4px;padding:5px 4px;font-size:8px;color:#d4a060;text-align:center;line-height:1.3;">Contamination<br>Control</div>
          <div style="background:#2a1a0a;border:1px solid #4a3a0a;border-radius:4px;padding:5px 4px;font-size:8px;color:#d4a060;text-align:center;line-height:1.3;">Temp<br>Stabilization</div>
          <div style="background:#2a1a0a;border:1px solid #4a3a0a;border-radius:4px;padding:5px 4px;font-size:8px;color:#90d490;text-align:center;line-height:1.3;">Pressure<br>Calibration</div>
          <div style="background:#2a1a0a;border:1px solid #4a3a0a;border-radius:4px;padding:5px 4px;font-size:8px;color:#90d490;text-align:center;line-height:1.3;">Activation<br>Completion</div>
          <div style="background:#2a1a0a;border:1px solid #4a3a0a;border-radius:4px;padding:5px 4px;font-size:8px;color:#90d490;text-align:center;line-height:1.3;">Maintenance<br>(HITL)</div>
          <div style="background:#2a1a0a;border:1px solid #4a3a0a;border-radius:4px;padding:5px 4px;font-size:8px;color:#90d490;text-align:center;line-height:1.3;">Throughput<br>&amp; Yield</div>
          <div style="background:#2a1a0a;border:1px solid #4a3a0a;border-radius:4px;padding:5px 4px;font-size:8px;color:#90d490;text-align:center;line-height:1.3;">Cross-<br>Process</div>
          <div style="background:#2a1a0a;border:1px solid #4a3a0a;border-radius:4px;padding:5px 4px;font-size:8px;color:#90d490;text-align:center;line-height:1.3;">Quality<br>Control</div>
        </div>
      </div>

    </div>

    <!-- Right: Tech stack + data flow note -->
    <div style="display:flex;flex-direction:column;gap:7px;">

      <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:9px 12px;">
        <div style="font-size:9px;font-weight:800;color:#5ab4e8;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Technology Stack</div>
        <div style="display:flex;flex-direction:column;gap:4px;font-size:10px;">
          <div style="display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid #1e2d45;">
            <span style="color:#5a7a9a;">Language</span>
            <span style="color:#c8d8e8;font-weight:600;">Python 3.11+</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid #1e2d45;">
            <span style="color:#5a7a9a;">Orchestration</span>
            <span style="color:#50d4a0;font-weight:600;">Semantic Kernel 1.5+</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid #1e2d45;">
            <span style="color:#5a7a9a;">LLM</span>
            <span style="color:#c080e0;font-weight:600;">Claude Sonnet 4.6</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid #1e2d45;">
            <span style="color:#5a7a9a;">Expert agents</span>
            <span style="color:#f0a830;font-weight:600;">12 specialists</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:3px 0;">
            <span style="color:#5a7a9a;">Report</span>
            <span style="color:#c8d8e8;font-weight:600;">python-docx</span>
          </div>
        </div>
      </div>

      <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:9px 12px;">
        <div style="font-size:9px;font-weight:800;color:#5ab4e8;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Data Flow</div>
        <div style="font-size:9px;color:#5a7a9a;line-height:1.6;">
          <span style="color:#c8d8e8;">①</span> Simulator generates 50-metric snapshot<br>
          <span style="color:#c8d8e8;">②</span> Fault threshold crossed → agent triggered<br>
          <span style="color:#c8d8e8;">③</span> SK passes snapshot to triage agent<br>
          <span style="color:#c8d8e8;">④</span> Triage selects 1–2 expert agents<br>
          <span style="color:#c8d8e8;">⑤</span> Experts stream analysis to operator<br>
          <span style="color:#c8d8e8;">⑥</span> Report generated &amp; offered for download
        </div>
      </div>

      <div style="background:#0f1a2a;border-left:3px solid #f0a830;border-radius:0 6px 6px 0;padding:7px 10px;">
        <div style="font-size:9px;color:#7a8a5a;line-height:1.5;">
          <strong style="color:#f0a830;">Near-closed loop:</strong> AI diagnoses and recommends — human approves before line intervention.
        </div>
      </div>

    </div>

  </div>
</div>
"""),

    # ── 3: EXPERT AGENT CATALOG ───────────────────────────────────────────────
    dict(
        bg="#0a0d14",
        html="""
<div style="min-height:460px;display:flex;flex-direction:column;justify-content:center;padding:14px 52px 10px;">

  <div style="font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#4a6a9c;font-weight:700;margin-bottom:6px;">03 · Expert Agent Catalog</div>
  <div style="font-size:26px;font-weight:900;color:#e8f0f8;line-height:1.2;margin-bottom:3px;">
    12 Specialist Domain Agents
  </div>
  <div style="font-size:11px;color:#5a7a9a;margin-bottom:10px;">Each agent carries a focused system prompt covering exactly one control loop from the PV research literature</div>

  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-bottom:8px;">

    <div style="background:#0f1f35;border:1px solid #1e3a5a;border-radius:8px;padding:7px 10px;">
      <div style="font-size:11px;font-weight:800;color:#5ab4e8;margin-bottom:3px;">Defect Reduction Expert</div>
      <div style="font-size:10px;color:#4a6a8a;line-height:1.5;">Tracks defect propagation across stages. Identifies pinhole, delamination, and patterning defects that originate upstream and manifest downstream.</div>
    </div>

    <div style="background:#0f1f35;border:1px solid #1e3a5a;border-radius:8px;padding:7px 10px;">
      <div style="font-size:11px;font-weight:800;color:#5ab4e8;margin-bottom:3px;">Efficiency Expert</div>
      <div style="font-size:10px;color:#4a6a8a;line-height:1.5;">Diagnoses low conversion efficiency. Analyzes Voc, Jsc, and fill-factor deviations to isolate whether the root cause is optical, electrical, or process-related.</div>
    </div>

    <div style="background:#0f1f35;border:1px solid #1e3a5a;border-radius:8px;padding:7px 10px;">
      <div style="font-size:11px;font-weight:800;color:#5ab4e8;margin-bottom:3px;">Grain Optimization Expert</div>
      <div style="font-size:10px;color:#4a6a8a;line-height:1.5;">Handles CdTe grain growth failures. Correlates grain diameter readings with deposition temperature and pressure to prescribe recipe adjustments.</div>
    </div>

    <div style="background:#0f1f35;border:1px solid #1e3a5a;border-radius:8px;padding:7px 10px;">
      <div style="font-size:11px;font-weight:800;color:#5ab4e8;margin-bottom:3px;">Uniformity Correction Expert</div>
      <div style="font-size:10px;color:#4a6a8a;line-height:1.5;">Handles deposition non-uniformity. Uses thickness and composition variance metrics to recommend scan-speed and source adjustments.</div>
    </div>

    <div style="background:#0f1f35;border:1px solid #1e3a5a;border-radius:8px;padding:7px 10px;">
      <div style="font-size:11px;font-weight:800;color:#5ab4e8;margin-bottom:3px;">Contamination Control Expert</div>
      <div style="font-size:10px;color:#4a6a8a;line-height:1.5;">Handles particle and chemical contamination events. Assesses cleanroom metrics, particle counts, and chemical traces to isolate source.</div>
    </div>

    <div style="background:#0f1f35;border:1px solid #1e3a5a;border-radius:8px;padding:7px 10px;">
      <div style="font-size:11px;font-weight:800;color:#5ab4e8;margin-bottom:3px;">Temperature Stabilization Expert</div>
      <div style="font-size:10px;color:#4a6a8a;line-height:1.5;">Handles thermal process deviations. Assesses substrate and zone temperatures across deposition and annealing stages for drift and overshoot.</div>
    </div>

    <div style="background:#1a2a0a;border:1px solid #2a5020;border-radius:8px;padding:7px 10px;">
      <div style="font-size:11px;font-weight:800;color:#90d490;margin-bottom:3px;">Pressure Calibration Expert</div>
      <div style="font-size:10px;color:#4a6a4a;line-height:1.5;">Handles vacuum and gas pressure anomalies. Distinguishes sensor drift from real chamber leaks and recommends calibration or maintenance action.</div>
    </div>

    <div style="background:#1a2a0a;border:1px solid #2a5020;border-radius:8px;padding:7px 10px;">
      <div style="font-size:11px;font-weight:800;color:#90d490;margin-bottom:3px;">Activation Completion Expert</div>
      <div style="font-size:10px;color:#4a6a4a;line-height:1.5;">Handles CdCl₂ activation problems (Stage 3). Assesses activation efficiency and correlates incomplete activation with downstream efficiency loss.</div>
    </div>

    <div style="background:#1a2a0a;border:1px solid #2a5020;border-radius:8px;padding:7px 10px;">
      <div style="font-size:11px;font-weight:800;color:#90d490;margin-bottom:3px;">Maintenance Expert (HITL)</div>
      <div style="font-size:10px;color:#4a6a4a;line-height:1.5;">Escalates equipment and human-factor issues. Generates structured handoff reports when physical inspection or manual intervention is required.</div>
    </div>

    <div style="background:#1a2a0a;border:1px solid #2a5020;border-radius:8px;padding:7px 10px;">
      <div style="font-size:11px;font-weight:800;color:#90d490;margin-bottom:3px;">Throughput &amp; Yield Expert</div>
      <div style="font-size:10px;color:#4a6a4a;line-height:1.5;">Handles production rate and yield loss events. Identifies bottleneck stages and correlates throughput drops with specific process deviations.</div>
    </div>

    <div style="background:#1a2a0a;border:1px solid #2a5020;border-radius:8px;padding:7px 10px;">
      <div style="font-size:11px;font-weight:800;color:#90d490;margin-bottom:3px;">Cross-Process Optimization Expert</div>
      <div style="font-size:10px;color:#4a6a4a;line-height:1.5;">Handles multi-stage systemic faults that span more than one process zone. Synthesizes patterns across the full 7-stage snapshot.</div>
    </div>

    <div style="background:#1a2a0a;border:1px solid #2a5020;border-radius:8px;padding:7px 10px;">
      <div style="font-size:11px;font-weight:800;color:#90d490;margin-bottom:3px;">Quality Control Expert</div>
      <div style="font-size:10px;color:#4a6a4a;line-height:1.5;">Runs the end-to-end quality audit. Acts as the final gate that confirms or rejects a module based on all upstream findings and current QA metrics.</div>
    </div>

  </div>

  <div style="background:#0f1420;border-left:3px solid #5ab4e8;border-radius:0 6px 6px 0;padding:9px 14px;font-size:10px;color:#4a6a8a;">
    <strong style="color:#5ab4e8;">Design principle:</strong> Each agent's system prompt is scoped to its domain only — it does not see instructions for other experts. This keeps context focused, prevents cross-contamination of reasoning, and makes individual agent behavior explainable and auditable.
  </div>

</div>
"""),

    # ── 4: EXPERT SELECTION & ROUTING ─────────────────────────────────────────
    dict(
        bg="#0a0d14",
        html="""
<div style="min-height:460px;display:flex;flex-direction:column;justify-content:center;padding:14px 52px 10px;">

  <div style="font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#f0a830;font-weight:700;margin-bottom:6px;">04 · Expert Selection &amp; Routing</div>
  <div style="font-size:26px;font-weight:900;color:#e8f0f8;line-height:1.2;margin-bottom:3px;">
    How the Triage Agent Decides
  </div>
  <div style="font-size:11px;color:#5a7a9a;margin-bottom:10px;">The Central Reasoning Agent does not pick experts randomly — it reasons over the fault data and explains its choice</div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">

    <!-- Left: Triage reasoning process -->
    <div>
      <div style="font-size:9px;font-weight:800;color:#f0a830;text-transform:uppercase;letter-spacing:2px;margin-bottom:7px;">Triage Reasoning Process</div>

      <div style="display:flex;flex-direction:column;gap:5px;">

        <div style="display:flex;gap:8px;align-items:flex-start;background:#1a1f0a;border:1px solid #3a3a1a;border-radius:6px;padding:7px 10px;">
          <div style="background:#3a3a0a;border-radius:50%;width:20px;height:20px;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;color:#f0a830;min-width:20px;">1</div>
          <div>
            <div style="font-size:10px;font-weight:700;color:#e0e080;">Receive full sensor snapshot</div>
            <div style="font-size:9px;color:#a0a060;margin-top:1px;">All 50 metrics passed simultaneously, pre-flagged with direction and deviation magnitude.</div>
          </div>
        </div>

        <div style="display:flex;gap:8px;align-items:flex-start;background:#1a1f0a;border:1px solid #3a3a1a;border-radius:6px;padding:7px 10px;">
          <div style="background:#3a3a0a;border-radius:50%;width:20px;height:20px;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;color:#f0a830;min-width:20px;">2</div>
          <div>
            <div style="font-size:10px;font-weight:700;color:#e0e080;">Perform fault assessment</div>
            <div style="font-size:9px;color:#a0a060;margin-top:1px;">Explains what each anomalous reading means physically — not just numbers, but the process implication.</div>
          </div>
        </div>

        <div style="display:flex;gap:8px;align-items:flex-start;background:#1a1f0a;border:1px solid #3a3a1a;border-radius:6px;padding:7px 10px;">
          <div style="background:#3a3a0a;border-radius:50%;width:20px;height:20px;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;color:#f0a830;min-width:20px;">3</div>
          <div>
            <div style="font-size:10px;font-weight:700;color:#e0e080;">Select primary + secondary expert</div>
            <div style="font-size:9px;color:#a0a060;margin-top:1px;">Picks the most relevant primary and cross-check secondary from 12 experts, with explicit justification.</div>
          </div>
        </div>

        <div style="display:flex;gap:8px;align-items:flex-start;background:#1a1f0a;border:1px solid #3a3a1a;border-radius:6px;padding:7px 10px;">
          <div style="background:#3a3a0a;border-radius:50%;width:20px;height:20px;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;color:#f0a830;min-width:20px;">4</div>
          <div>
            <div style="font-size:10px;font-weight:700;color:#e0e080;">State initial hypothesis</div>
            <div style="font-size:9px;color:#a0a060;margin-top:1px;">Commits to a root-cause theory before experts run — visible to the operator, revisable by experts.</div>
          </div>
        </div>

      </div>
    </div>

    <!-- Right: Routing logic example + expert map -->
    <div style="display:flex;flex-direction:column;gap:8px;">

      <div style="background:#0f1a2a;border:1px solid #1e3a5a;border-radius:8px;padding:9px 12px;">
        <div style="font-size:9px;font-weight:800;color:#5ab4e8;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Triage Response Structure</div>
        <div style="font-size:9px;color:#5a7a9a;line-height:1.6;">
          The triage agent formats its response as:<br>
          <span style="color:#c8d8e8;font-weight:700;">## Fault Assessment</span> — anomalous metrics and their physical meaning<br>
          <span style="color:#c8d8e8;font-weight:700;">## Why This Expert?</span> — explicit routing justification<br>
          <span style="color:#c8d8e8;font-weight:700;">## Initial Hypothesis</span> — root-cause theory before experts run
        </div>
      </div>

      <div style="background:#0f1a2a;border:1px solid #1e3a5a;border-radius:8px;padding:9px 12px;">
        <div style="font-size:9px;font-weight:800;color:#5ab4e8;text-transform:uppercase;letter-spacing:1px;margin-bottom:5px;">Why Two Experts?</div>
        <div style="font-size:9px;color:#5a7a9a;line-height:1.6;">
          The secondary expert independently reviews the same snapshot and confirms or challenges the primary's findings — mirroring peer review to reduce hallucination risk before any corrective action is recommended.
        </div>
      </div>

    </div>

  </div>
</div>
"""),

    # ── 5: REASONING CHAIN ────────────────────────────────────────────────────
    dict(
        bg="#0a0d14",
        html="""
<div style="min-height:460px;display:flex;flex-direction:column;justify-content:center;padding:14px 52px 10px;">

  <div style="font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#f0a830;font-weight:700;margin-bottom:6px;">05 · Reasoning Chain</div>
  <div style="font-size:26px;font-weight:900;color:#e8f0f8;line-height:1.2;margin-bottom:3px;">
    From Sensor Anomaly to Diagnostic Report
  </div>
  <div style="font-size:11px;color:#5a7a9a;margin-bottom:12px;">Three sequential reasoning phases, each with a distinct system prompt — streamed live to the operator</div>

  <!-- Phase flow -->
  <div style="display:grid;grid-template-columns:1fr 28px 1fr 28px 1fr;gap:0;margin-bottom:10px;align-items:stretch;">

    <!-- Phase 1 -->
    <div style="background:#1a0f1f;border:1.5px solid #7a3a9a;border-radius:8px;padding:9px 12px;">
      <div style="font-size:8px;font-weight:800;color:#c080e0;text-transform:uppercase;letter-spacing:2px;margin-bottom:4px;">Phase 1</div>
      <div style="font-size:11px;font-weight:800;color:#e8f0f8;margin-bottom:2px;">Central Triage Agent</div>
      <div style="font-size:8px;color:#7a4a9a;margin-bottom:6px;">Claude Sonnet 4.6 · ~600 tokens</div>
      <div style="font-size:9px;color:#9a7ab8;line-height:1.5;">
        • Receives 50-metric snapshot<br>
        • Identifies anomalous readings<br>
        • Explains physical meaning<br>
        • Selects primary + secondary expert<br>
        • States initial hypothesis<br>
        • Streams response to UI
      </div>
      <div style="margin-top:6px;background:#2a1a2a;border-radius:4px;padding:4px 7px;font-size:8px;color:#c080e0;font-style:italic;">
        "Routing to Pressure Calibration Expert — 0.3 mTorr deviation at Stage 2 with elevated particle counts is consistent with a partial seal failure…"
      </div>
    </div>

    <div style="display:flex;align-items:center;justify-content:center;font-size:18px;color:#3a3060;">→</div>

    <!-- Phase 2 -->
    <div style="background:#0f1a2a;border:1.5px solid #2a6a9c;border-radius:8px;padding:9px 12px;">
      <div style="font-size:8px;font-weight:800;color:#5ab4e8;text-transform:uppercase;letter-spacing:2px;margin-bottom:4px;">Phase 2</div>
      <div style="font-size:11px;font-weight:800;color:#e8f0f8;margin-bottom:2px;">Primary Expert Agent</div>
      <div style="font-size:8px;color:#3a6a9a;margin-bottom:6px;">Claude Sonnet 4.6 · ~1200 tokens</div>
      <div style="font-size:9px;color:#5a8ab8;line-height:1.5;">
        • Receives same sensor snapshot<br>
        • Applies domain-specific prompt<br>
        • Focused root-cause analysis<br>
        • Quantifies deviation severity<br>
        • Prescribes corrective actions<br>
        • Streams response to UI
      </div>
      <div style="margin-top:6px;background:#1a2a3a;border-radius:4px;padding:4px 7px;font-size:8px;color:#5ab4e8;font-style:italic;">
        "0.3 mTorr overpressure + 12% particle count elevation → vacuum seal degradation. Recommend: halt Stage 2, inspect gate valve O-ring…"
      </div>
    </div>

    <div style="display:flex;align-items:center;justify-content:center;font-size:18px;color:#3a3060;">→</div>

    <!-- Phase 3 -->
    <div style="background:#1a1f0a;border:1.5px solid #4a6a0a;border-radius:8px;padding:9px 12px;">
      <div style="font-size:8px;font-weight:800;color:#a0d4a0;text-transform:uppercase;letter-spacing:2px;margin-bottom:4px;">Phase 3</div>
      <div style="font-size:11px;font-weight:800;color:#e8f0f8;margin-bottom:2px;">Cross-Check Expert</div>
      <div style="font-size:8px;color:#4a6a2a;margin-bottom:6px;">Claude Sonnet 4.6 · ~1200 tokens</div>
      <div style="font-size:9px;color:#6a9a6a;line-height:1.5;">
        • Independent analysis of same data<br>
        • Applies different domain lens<br>
        • Confirms or challenges Phase 2<br>
        • Surfaces any missed signals<br>
        • Adds complementary perspective<br>
        • Streams response to UI
      </div>
      <div style="margin-top:6px;background:#1a2a0a;border-radius:4px;padding:4px 7px;font-size:8px;color:#a0d4a0;font-style:italic;">
        "Corroborating: particle elevation is consistent with mechanical seal wear, not chemical contamination. Profile matches O-ring debris…"
      </div>
    </div>

  </div>

  <!-- Output -->
  <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:9px 14px;display:flex;gap:12px;align-items:center;">
    <div style="font-size:20px;">📄</div>
    <div style="flex:1;">
      <div style="font-size:10px;font-weight:800;color:#c8d8e8;margin-bottom:1px;">Output: Autonomous Diagnostic Report (.docx)</div>
      <div style="font-size:9px;color:#5a7a9a;line-height:1.5;">
        All three phases compiled into a Word document: fault summary, triage assessment, expert analysis, cross-check findings, sensor snapshot, and corrective actions — generated without any human writing a single line.
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:3px;min-width:150px;">
      <div style="font-size:8px;background:#1e2d45;border-radius:4px;padding:3px 7px;color:#5ab4e8;">✓ Root cause identified</div>
      <div style="font-size:8px;background:#1e2d45;border-radius:4px;padding:3px 7px;color:#5ab4e8;">✓ Corrective actions listed</div>
      <div style="font-size:8px;background:#1e2d45;border-radius:4px;padding:3px 7px;color:#5ab4e8;">✓ Full sensor snapshot</div>
      <div style="font-size:8px;background:#1e2d45;border-radius:4px;padding:3px 7px;color:#5ab4e8;">✓ Cross-check validation</div>
    </div>
  </div>

</div>
"""),

    # ── 6: LIVE DEMO ──────────────────────────────────────────────────────────
    dict(
        bg="#0a0d14",
        html="""
<div style="min-height:460px;display:flex;flex-direction:column;justify-content:center;padding:22px 60px;">

  <div style="font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#50d4a0;font-weight:700;margin-bottom:8px;">06 · Live Demo</div>
  <div style="font-size:28px;font-weight:900;color:#e8f0f8;line-height:1.2;margin-bottom:4px;">
    See It in Action: <span style="color:#f0a830;">Solar PV Manufacturing Line</span>
  </div>
  <div style="font-size:12px;color:#5a7a9a;margin-bottom:14px;">From sensor anomaly to downloadable diagnostic report — in under 60 seconds</div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:12px;">

    <!-- What happens -->
    <div>
      <div style="font-size:10px;font-weight:800;color:#50d4a0;text-transform:uppercase;letter-spacing:2px;margin-bottom:7px;">What to Watch For</div>
      <div style="display:flex;flex-direction:column;gap:5px;">
        <div style="display:flex;gap:10px;align-items:flex-start;background:#0f1a2a;border:1px solid #1e3a5a;border-radius:6px;padding:6px 10px;">
          <div style="font-size:16px;min-width:22px;">🏭</div>
          <div style="font-size:11px;color:#7a9ab8;line-height:1.5;"><strong style="color:#5ab4e8;">Conveyor runs normally</strong> for ~20 seconds — all 7 stages green, metrics within range.</div>
        </div>
        <div style="display:flex;gap:10px;align-items:flex-start;background:#0f1a2a;border:1px solid #1e3a5a;border-radius:6px;padding:6px 10px;">
          <div style="font-size:16px;min-width:22px;">⚠️</div>
          <div style="font-size:11px;color:#7a9ab8;line-height:1.5;"><strong style="color:#e05555;">A random fault auto-injects</strong> into one stage — chosen from 10 pre-defined fault scenarios across the 7-stage line.</div>
        </div>
        <div style="display:flex;gap:10px;align-items:flex-start;background:#0f1a2a;border:1px solid #1e3a5a;border-radius:6px;padding:6px 10px;">
          <div style="font-size:16px;min-width:22px;">🧠</div>
          <div style="font-size:11px;color:#7a9ab8;line-height:1.5;"><strong style="color:#5ab4e8;">The triage agent activates</strong> and streams its fault assessment, expert selection, and hypothesis live to the screen.</div>
        </div>
        <div style="display:flex;gap:10px;align-items:flex-start;background:#0f1a2a;border:1px solid #1e3a5a;border-radius:6px;padding:6px 10px;">
          <div style="font-size:16px;min-width:22px;">👨‍🔬</div>
          <div style="font-size:11px;color:#7a9ab8;line-height:1.5;"><strong style="color:#5ab4e8;">Expert agents respond</strong> sequentially — primary analysis, then cross-check — each streamed as it is generated.</div>
        </div>
        <div style="display:flex;gap:10px;align-items:flex-start;background:#0f1a2a;border:1px solid #1e3a5a;border-radius:6px;padding:6px 10px;">
          <div style="font-size:16px;min-width:22px;">📄</div>
          <div style="font-size:11px;color:#7a9ab8;line-height:1.5;"><strong style="color:#50d4a0;">A .docx report is generated</strong> automatically and offered for download when analysis completes.</div>
        </div>
      </div>
    </div>

    <!-- System stats -->
    <div>
      <div style="font-size:10px;font-weight:800;color:#50d4a0;text-transform:uppercase;letter-spacing:2px;margin-bottom:7px;">System at a Glance</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px;">
        <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:8px;text-align:center;">
          <div style="font-size:22px;font-weight:900;color:#5ab4e8;">7</div>
          <div style="font-size:9px;color:#5a7a9a;margin-top:1px;">Production stages</div>
        </div>
        <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:8px;text-align:center;">
          <div style="font-size:22px;font-weight:900;color:#5ab4e8;">50</div>
          <div style="font-size:9px;color:#5a7a9a;margin-top:1px;">Sensor metrics</div>
        </div>
        <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:8px;text-align:center;">
          <div style="font-size:22px;font-weight:900;color:#f0a830;">12</div>
          <div style="font-size:9px;color:#5a7a9a;margin-top:1px;">Expert agents</div>
        </div>
        <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:8px;text-align:center;">
          <div style="font-size:22px;font-weight:900;color:#50d4a0;">&lt;60s</div>
          <div style="font-size:9px;color:#5a7a9a;margin-top:1px;">Detection to report</div>
        </div>
      </div>

      <div style="background:linear-gradient(135deg,#1a1a0a,#0f1a2a);border:1px solid #3a5a3a;border-radius:10px;padding:10px 14px;">
        <div style="font-size:11px;font-weight:800;color:#f0c060;margin-bottom:4px;">Ready to see it live?</div>
        <div style="font-size:10px;color:#7a9a7a;line-height:1.5;">
          Switch to the <strong style="color:#e0e0a0;">PV Stages</strong> tab to understand the manufacturing process, then open <strong style="color:#e0e0a0;">Live Demo</strong> to watch the agent detect and diagnose a real-time fault injection.
        </div>
      </div>
    </div>

  </div>

</div>
"""),

    # ── 7: ROUTES FORWARD ─────────────────────────────────────────────────────
    dict(
        bg="#0a0d14",
        html="""
<div style="min-height:460px;display:flex;flex-direction:column;justify-content:center;padding:14px 52px 10px;">

  <div style="font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#50d4a0;font-weight:700;margin-bottom:6px;">07 · Routes Forward</div>
  <div style="font-size:26px;font-weight:900;color:#e8f0f8;line-height:1.2;margin-bottom:3px;">
    Where Can We Take This?
  </div>
  <div style="font-size:11px;color:#5a7a9a;margin-bottom:10px;">An open conversation — not a product roadmap. What would make this meaningful at First Solar?</div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">

    <!-- Why we're sharing -->
    <div style="background:#0f1f35;border:1px solid #1e3a5a;border-left:3px solid #5ab4e8;border-radius:8px;padding:9px 12px;">
      <div style="font-size:10px;font-weight:800;color:#5ab4e8;margin-bottom:4px;">💡 Why We're Sharing This</div>
      <div style="font-size:9px;color:#5a7a9a;line-height:1.6;">
        This is a proof-of-concept to <span style="color:#c8d8e8;font-weight:600;">trigger thinking</span> — not a finished system. The goal is to explore what a centralized AI reasoning layer could mean in the context of First Solar's manufacturing operations. No commitment, just questions worth asking out loud.
      </div>
    </div>

    <!-- Integration -->
    <div style="background:#1a1f0a;border:1px solid #3a3a1a;border-left:3px solid #f0a830;border-radius:8px;padding:9px 12px;">
      <div style="font-size:10px;font-weight:800;color:#f0a830;margin-bottom:4px;">🔗 Integration with Existing Systems</div>
      <div style="font-size:9px;color:#7a7a5a;line-height:1.6;">
        First Solar already has fault management tooling —&nbsp;<span style="color:#e0e080;font-weight:600;">Incidents</span>, <span style="color:#e0e080;font-weight:600;">Jarvis</span>, <span style="color:#e0e080;font-weight:600;">SPC Incidents</span>. Rather than replacing these, could this architecture plug in as a reasoning layer on top? What additional value would it provide to an already integrated system?
      </div>
    </div>

    <!-- Knowledge scoping -->
    <div style="background:#1a0f1f;border:1px solid #3a1a3a;border-left:3px solid #c080e0;border-radius:8px;padding:9px 12px;">
      <div style="font-size:10px;font-weight:800;color:#c080e0;margin-bottom:4px;">🔒 Scoping to First Solar Knowledge</div>
      <div style="font-size:9px;color:#8a7a9a;line-height:1.6;">
        Currently, the agent reasons from <span style="color:#d8c8e8;font-weight:600;">public domain knowledge</span> it was trained on. How do we constrain it to First Solar's process recipes, tolerance specs, and institutional knowledge? RAG over internal documentation? Fine-tuning? Structured tool calls to internal systems?
      </div>
    </div>

    <!-- Next steps -->
    <div style="background:#0f1a1a;border:1px solid #1a3a3a;border-left:3px solid #50d4a0;border-radius:8px;padding:9px 12px;">
      <div style="font-size:10px;font-weight:800;color:#50d4a0;margin-bottom:4px;">✅ If We Move Forward: First Step</div>
      <div style="font-size:9px;color:#5a8a7a;line-height:1.5;margin-bottom:6px;">
        A structured review with domain experts who can validate whether the agent's reasoning is grounded in First Solar's actual process reality.
      </div>
      <div style="display:flex;flex-direction:column;gap:3px;">
        <div style="font-size:9px;background:#0a2a2a;border:1px solid #1a4a4a;border-radius:4px;padding:4px 8px;color:#60d4b8;">🔬 Quality &amp; Reliability Experts</div>
        <div style="font-size:9px;background:#0a2a2a;border:1px solid #1a4a4a;border-radius:4px;padding:4px 8px;color:#60d4b8;">🧪 Research &amp; Development Experts</div>
        <div style="font-size:9px;background:#0a2a2a;border:1px solid #1a4a4a;border-radius:4px;padding:4px 8px;color:#60d4b8;">🏗️ Manufacturing (Semicon) Experts</div>
      </div>
    </div>

  </div>
</div>
"""),

]

# ── Navigation bar (top) ──────────────────────────────────────────────────────
st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
idx   = st.session_state.intro_slide
slide = SLIDES[idx]
bg    = slide["bg"] if dark else _D2L.get(slide["bg"], slide["bg"])
html_content = apply_theme(slide["html"])

nav_left, nav_dots, nav_right = st.columns([1, 4, 1])

with nav_left:
    if idx > 0:
        if st.button("← Back", use_container_width=True):
            go(-1)
            st.rerun()

with nav_dots:
    LABELS = [
        "Agenda", "Architecture", "Expert Agents",
        "Expert Selection", "Reasoning Chain", "Live Demo", "Routes Forward",
    ]
    active_color   = "#1a7ab8" if not dark else "#5ab4e8"
    inactive_color = "#c0c8d8" if not dark else "#2a3050"
    label_color    = "#1a7ab8" if not dark else "#5ab4e8"
    counter_color  = "#6a8aaa" if not dark else "#2a3a5a"
    dots_html = "<div style='display:flex;justify-content:center;align-items:center;gap:10px;padding:4px 0;'>"
    for i, label in enumerate(LABELS):
        if i == idx:
            dots_html += (
                f"<div style='display:flex;align-items:center;gap:6px;'>"
                f"<div style='width:10px;height:10px;border-radius:50%;background:{active_color};box-shadow:0 0 6px {active_color}88;'></div>"
                f"<span style='font-size:11px;font-weight:700;color:{label_color};'>{label}</span>"
                f"</div>"
            )
        else:
            dots_html += f"<div style='width:7px;height:7px;border-radius:50%;background:{inactive_color};'></div>"
    dots_html += "</div>"
    dots_html += f"<div style='text-align:center;font-size:10px;color:{counter_color};margin-top:1px;'>Slide {idx + 1} of {TOTAL_SLIDES}</div>"
    st.markdown(dots_html, unsafe_allow_html=True)

with nav_right:
    if idx < TOTAL_SLIDES - 1:
        if st.button("Next →", use_container_width=True):
            go(1)
            st.rerun()

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ── Render current slide ───────────────────────────────────────────────────────
st.components.v1.html(f"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  background: {bg};
  font-family: 'Segoe UI', -apple-system, sans-serif;
  min-height: 510px;
}}
</style></head>
<body>{html_content}</body></html>
""", height=560, scrolling=False)

# ── Download button ────────────────────────────────────────────────────────────
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
_, col_dl, _ = st.columns([2, 3, 2])
with col_dl:
    ppt_bytes = generate_intro_ppt()
    fname = f"CRA_Architecture_Forum_{datetime.now().strftime('%Y%m%d')}.pptx"
    st.download_button(
        label="⬇ Download Slides (.pptx)",
        data=ppt_bytes,
        file_name=fname,
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        use_container_width=True,
    )
