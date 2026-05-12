"""Live Demo page — solar panel conveyor + agent reasoning."""
import time
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from data.simulator import PVSimulator
from ui.conveyor_panel import render_conveyor, build_stage_statuses, build_stage_metrics_for_ui
from ui.agent_panel import render_agent_panel
from utils.report_exporter import generate_report
from utils.theme import page_css

st.markdown(page_css("""
.stDownloadButton > button {
    background: #1a5276; color: white;
    border: none; font-weight: 600;
    width: 100%; margin-top: 12px;
}
"""), unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "simulator"    not in st.session_state:
    st.session_state.simulator    = PVSimulator(fault_delay_range=(18, 25))
if "running"      not in st.session_state:
    st.session_state.running      = False
if "fault_shown"  not in st.session_state:
    st.session_state.fault_shown  = False
if "analysis"     not in st.session_state:
    st.session_state.analysis     = None
if "snapshot"     not in st.session_state:
    st.session_state.snapshot     = None
if "report_bytes" not in st.session_state:
    st.session_state.report_bytes = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ☀️ PV Control System")
    st.markdown("**Agentic AI Demo**")
    st.markdown("---")

    if not st.session_state.running:
        if st.button("▶ Start Simulation", use_container_width=True, type="primary"):
            st.session_state.simulator    = PVSimulator(fault_delay_range=(18, 25))
            st.session_state.running      = True
            st.session_state.fault_shown  = False
            st.session_state.analysis     = None
            st.session_state.report_bytes = None
            st.rerun()
    else:
        if st.button("⏹ Reset", use_container_width=True):
            st.session_state.simulator.reset()
            st.session_state.running      = False
            st.session_state.fault_shown  = False
            st.session_state.analysis     = None
            st.session_state.report_bytes = None
            st.rerun()

    st.markdown("---")
    st.markdown("**How it works**")
    st.markdown(
        "1. Start the simulation\n"
        "2. Watch the conveyor run normally for ~20 seconds\n"
        "3. A random fault auto-injects into one stage\n"
        "4. The AI agent activates and analyzes the fault\n"
        "5. Download the full diagnostic report"
    )
    st.markdown("---")
    st.caption("LLM: Claude Sonnet 4.6")
    st.caption("Orchestrator: Semantic Kernel")
    st.caption("12 Expert Sub-agents")

# ── Main content ──────────────────────────────────────────────────────────────
st.markdown("# ☀️ Near-Closed-Loop PV Manufacturing Control")
st.markdown(
    "A centralized LLM reasoning agent monitors the solar panel production line "
    "and autonomously diagnoses faults using 12 specialist expert agents."
)

conveyor_placeholder = st.empty()

if not st.session_state.running:
    _idle_sim = PVSimulator()
    _idle_sim.start()
    _idle_snap = _idle_sim.get_snapshot()
    with conveyor_placeholder.container():
        render_conveyor(
            stage_statuses=build_stage_statuses(_idle_snap),
            stage_metrics=build_stage_metrics_for_ui(_idle_snap),
            fault_stage=None,
            running=False,
        )
    col_c = st.columns([1, 2, 1])[1]
    with col_c:
        if st.button("▶ Start Simulation", use_container_width=True, type="primary", key="main_start"):
            st.session_state.simulator    = PVSimulator(fault_delay_range=(18, 25))
            st.session_state.running      = True
            st.session_state.fault_shown  = False
            st.session_state.analysis     = None
            st.session_state.report_bytes = None
            st.rerun()
    st.info("Click **▶ Start Simulation** above (or in the sidebar) to begin the demo.")

else:
    sim: PVSimulator = st.session_state.simulator
    snapshot = sim.get_snapshot()
    st.session_state.snapshot = snapshot

    stage_statuses = build_stage_statuses(snapshot)
    stage_metrics  = build_stage_metrics_for_ui(snapshot)
    fault_stage    = snapshot.fault_scenario["stage"] if snapshot.fault_active else None

    with conveyor_placeholder.container():
        render_conveyor(
            stage_statuses=stage_statuses,
            stage_metrics=stage_metrics,
            fault_stage=fault_stage,
            running=True,
        )

    if not snapshot.fault_active:
        elapsed  = snapshot.elapsed_seconds
        delay    = sim._fault_delay
        progress = min(elapsed / delay, 0.95)
        st.progress(progress, text=f"Line running normally… fault injection in ~{max(0, int(delay - elapsed))}s")
        time.sleep(1.5)
        st.rerun()

    elif not st.session_state.fault_shown:
        st.session_state.fault_shown = True
        scenario = snapshot.fault_scenario

        st.error(
            f"⚠️ **Fault Detected at Stage {scenario['stage']}: {scenario['stage_name']}**  \n"
            f"{scenario['plain_english']}"
        )

        analysis = render_agent_panel(snapshot, scenario)
        st.session_state.analysis = analysis

        st.success("✅ Analysis complete. Generating report...")
        try:
            report_bytes = generate_report(analysis)
            st.session_state.report_bytes = report_bytes
            from datetime import datetime
            fname = f"fault_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            st.download_button(
                label="📄 Download Fault Analysis Report (.docx)",
                data=report_bytes,
                file_name=fname,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary",
            )
        except Exception as e:
            st.error(f"Report generation error: {e}")

    elif st.session_state.fault_shown and st.session_state.analysis:
        scenario = snapshot.fault_scenario
        st.error(
            f"⚠️ **Fault: {scenario['display_name']}**  \n"
            f"Stage {scenario['stage']}: {scenario['stage_name']}"
        )
        st.success("✅ Analysis complete. The centralized reasoning agent has completed its diagnosis.")

        col1, col2 = st.columns([2, 1])
        with col1:
            with st.expander("📋 View Full Analysis", expanded=False):
                analysis = st.session_state.analysis
                if analysis.get("triage"):
                    st.markdown("### 🤖 Central Reasoning Agent")
                    st.markdown(analysis["triage"])
                if analysis.get("expert_primary_text"):
                    st.markdown(f"### 👨‍🔬 {analysis.get('expert_primary_name', 'Primary Expert')}")
                    st.markdown(analysis["expert_primary_text"])
                if analysis.get("expert_secondary_text"):
                    st.markdown(f"### 🔍 {analysis.get('expert_secondary_name', 'Cross-Check Expert')}")
                    st.markdown(analysis["expert_secondary_text"])
        with col2:
            if st.session_state.report_bytes:
                from datetime import datetime
                fname = f"fault_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
                st.download_button(
                    label="📄 Download Report (.docx)",
                    data=st.session_state.report_bytes,
                    file_name=fname,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            else:
                if st.button("Regenerate Report"):
                    try:
                        st.session_state.report_bytes = generate_report(st.session_state.analysis)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Report error: {e}")
