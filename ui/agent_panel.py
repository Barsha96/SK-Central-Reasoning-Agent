"""
Agent thought-process panel.
Streams the triage + expert reasoning into styled Streamlit chat bubbles.
"""
from __future__ import annotations

import streamlit as st
from data.simulator import SensorSnapshot
from agents.triage_agent import TriageAgent


SPEAKER_CONFIG = {
    "system":           {"avatar": "⚙️",  "label": "System",                    "color": "#334"},
    "triage":           {"avatar": "🤖",  "label": "Central Reasoning Agent",   "color": "#1a3a5c"},
    "expert_primary":   {"avatar": "👨‍🔬", "label": "Primary Expert",            "color": "#1a3a1a"},
    "expert_secondary": {"avatar": "🔍",  "label": "Cross-Check Expert",        "color": "#3a2a1a"},
}


def render_agent_panel(snapshot: SensorSnapshot, scenario: dict) -> dict | None:
    """
    Stream the full triage + expert analysis into the Streamlit UI.
    Returns the full analysis dict once streaming is complete (for report generation).
    """
    st.markdown("---")
    st.markdown("## 🤖 Centralized Reasoning Agent")
    st.caption(
        f"Fault scenario: **{scenario['display_name']}** — "
        f"Stage {scenario['stage']}: {scenario['stage_name']}"
    )

    agent = TriageAgent()

    # Track full text per speaker for report
    full_texts: dict[str, str] = {
        "triage": "",
        "expert_primary": "",
        "expert_secondary": "",
    }
    primary_name   = ""
    secondary_name = ""

    # We stream into separate containers per speaker
    current_speaker = None
    current_container = None
    current_placeholder = None
    current_buffer = ""

    for speaker, chunk in agent.analyze_stream(snapshot, scenario):
        if speaker == "system":
            # Flush current buffer first
            if current_placeholder and current_buffer:
                current_placeholder.markdown(current_buffer)
                current_buffer = ""
            st.markdown(chunk, unsafe_allow_html=True)
            current_speaker = None
            current_container = None
            current_placeholder = None
            continue

        # New speaker — open a new chat message container
        if speaker != current_speaker:
            if current_placeholder and current_buffer:
                current_placeholder.markdown(current_buffer)
                current_buffer = ""

            cfg = SPEAKER_CONFIG.get(speaker, SPEAKER_CONFIG["triage"])

            if speaker == "expert_primary":
                primary_name = _get_expert_display_name(scenario.get("primary_expert", "quality_control"))
                label = f"**{primary_name}**"
            elif speaker == "expert_secondary":
                secondary_name = _get_expert_display_name(scenario.get("secondary_expert", "quality_control"))
                label = f"**{secondary_name}** (cross-check)"
            else:
                label = f"**{cfg['label']}**"

            current_container = st.chat_message(cfg["avatar"])
            with current_container:
                st.caption(label)
                current_placeholder = st.empty()

            current_speaker = speaker
            current_buffer = ""

        # Accumulate chunk
        current_buffer += chunk
        if full_texts.get(speaker) is not None:
            full_texts[speaker] += chunk

        # Update the placeholder live
        if current_placeholder:
            with current_container:
                current_placeholder.markdown(current_buffer + "▌")

    # Final flush
    if current_placeholder and current_buffer:
        with current_container:
            current_placeholder.markdown(current_buffer)

    return {
        "triage": full_texts["triage"],
        "expert_primary_name": primary_name or _get_expert_display_name(scenario.get("primary_expert", "")),
        "expert_primary_text": full_texts["expert_primary"],
        "expert_secondary_name": secondary_name or _get_expert_display_name(scenario.get("secondary_expert", "")),
        "expert_secondary_text": full_texts["expert_secondary"],
        "faulty_steps": _get_faulty_steps_cached(snapshot),
        "scenario": scenario,
        "snapshot": snapshot,
    }


def _get_expert_display_name(key: str) -> str:
    from agents.triage_agent import EXPERT_MAP
    cls = EXPERT_MAP.get(key)
    if cls:
        return cls.display_name
    return key.replace("_", " ").title()


def _get_faulty_steps_cached(snapshot: SensorSnapshot) -> list:
    from data.simulator import get_faulty_steps
    return get_faulty_steps(snapshot)
