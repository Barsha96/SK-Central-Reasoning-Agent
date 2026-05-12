"""How Semantic Kernel Works — technical deep-dive with diagrams and code."""
import streamlit as st
from utils.theme import apply_theme, page_css

st.markdown(page_css(), unsafe_allow_html=True)

st.markdown("# ⚙️ How Semantic Kernel Works")
st.markdown(
    "Semantic Kernel (SK) is Microsoft's open-source SDK for building AI orchestration pipelines. "
    "This page explains how SK is used in this system — from registering Claude as an AI service, "
    "to configuring an expert agent, to the exact message flow between the central reasoning agent "
    "and the specialist experts."
)
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — SK core concepts
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 1 · Semantic Kernel Core Concepts")

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown(
        "Semantic Kernel has three fundamental building blocks:\n\n"
        "**Kernel** — the central service container. It holds registered AI services and plugins, "
        "and is the entry point for all inference calls.\n\n"
        "**AI Services** — adapters for LLM providers. SK ships with connectors for OpenAI, Azure, "
        "Anthropic, Google, Hugging Face, and others. Swapping providers means changing one line — "
        "the rest of the pipeline is provider-agnostic.\n\n"
        "**Plugins** — collections of `@kernel_function`-decorated Python methods that the Kernel "
        "can invoke. A plugin is what SK calls an 'expert': a named, callable unit of capability "
        "that the Kernel can discover and execute. In this system, each of the 12 expert agents "
        "is a SK Plugin."
    )
with col2:
    _SK_ARCH_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: transparent; font-family: 'Segoe UI', sans-serif; padding: 8px; }
.sk-arch { display: flex; flex-direction: column; align-items: center; gap: 0; }
.sk-box {
  border-radius: 8px; padding: 10px 16px; text-align: center;
  font-size: 12px; font-weight: 700; width: 260px;
}
.sk-kernel { background: #0f1f35; border: 2px solid #2a6a9c; color: #a0d4ff; }
.sk-row { display: flex; gap: 8px; margin: 6px 0; }
.sk-service { background: #1a2a0a; border: 1.5px solid #2a6a2a; color: #90d490; font-size: 11px; padding: 8px 10px; border-radius: 6px; flex: 1; text-align: center; }
.sk-plugin  { background: #2a1a0a; border: 1.5px solid #7a4a0a; color: #d4a060; font-size: 11px; padding: 8px 10px; border-radius: 6px; flex: 1; text-align: center; }
.sk-plugin sub, .sk-service sub { display: block; font-size: 9px; opacity: 0.7; font-weight: 400; margin-top: 2px; }
.arrow { color: #3a4060; font-size: 14px; text-align: center; margin: 2px 0; }
.label { font-size: 9px; color: #556677; text-align: center; margin-bottom: 2px; }
</style></head><body>
<div class="sk-arch">
  <div class="sk-box sk-kernel">🧠 Kernel<br><span style="font-size:10px;font-weight:400;color:#7eb3d4;">Service container &amp; orchestrator</span></div>
  <div class="arrow">↙ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ↘</div>
  <div class="sk-row" style="width:280px">
    <div class="sk-service">AI Services<sub>AnthropicChatCompletion<br>OpenAI · Azure · HuggingFace</sub></div>
    <div class="sk-plugin">Plugins<sub>Expert Agent classes<br>@kernel_function methods</sub></div>
  </div>
  <div class="arrow">↓</div>
  <div class="sk-box" style="background:#1a0f1f;border:1.5px solid #6a2a8a;color:#c090e0;width:260px;font-size:11px;padding:8px;">
    Claude Sonnet 4.6 API<br>
    <span style="font-size:9px;font-weight:400;opacity:0.7;">api.anthropic.com/v1/messages</span>
  </div>
</div>
</body></html>
"""
    st.components.v1.html(apply_theme(_SK_ARCH_HTML), height=310)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Kernel setup
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 2 · Registering Claude with the Kernel")
st.markdown(
    "`agents/kernel_setup.py` is the entry point. It creates a `Kernel` instance and registers "
    "Claude Sonnet 4.6 as the `AnthropicChatCompletion` service. Any component in the pipeline "
    "that needs to call Claude does so through this kernel — the API key and model ID are "
    "configured once here and nowhere else."
)

st.code("""# agents/kernel_setup.py
import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.anthropic import AnthropicChatCompletion

load_dotenv()

def build_kernel() -> Kernel:
    kernel = Kernel()

    kernel.add_service(
        AnthropicChatCompletion(
            ai_model_id=os.getenv("MODEL_ID", "claude-sonnet-4-6"),
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    )

    return kernel


# Usage anywhere in the codebase:
# kernel = build_kernel()
# The kernel now routes all LLM calls to Claude Sonnet 4.6
""", language="python")

st.markdown(
    "**What `add_service()` does under the hood:** SK wraps the Anthropic SDK's "
    "`anthropic.Anthropic()` client inside a `ChatCompletionClientBase` interface. "
    "This means you could swap to `OpenAIChatCompletion` or `GoogleAIChatCompletion` "
    "without touching any agent code — only this file changes."
)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — One expert configured end-to-end
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 3 · Expert Agent Configuration — Grain Optimization Expert")
st.markdown(
    "The **Grain Optimization Expert** is a good example: it has a compact, well-defined 3-step "
    "control loop with clear physics motivation. All 12 experts follow exactly this pattern."
)

tab_cls, tab_base, tab_flow = st.tabs(["The Expert Class", "BaseExpert (shared logic)", "What the API receives"])

with tab_cls:
    st.markdown(
        "The expert is a plain Python class. Three class-level attributes define its entire identity. "
        "The `BaseExpert` base class supplies the actual API call logic — the subclass only needs to "
        "fill in these three strings."
    )
    st.code("""# agents/experts/grain_optimization.py
from .base_expert import BaseExpert


class GrainOptimizationExpert(BaseExpert):

    # ── Identity ─────────────────────────────────────────────────────────────
    display_name = "Grain Optimization Expert"
    #  ↑ Shown in the UI and in the .docx report header

    loop_steps = "Step 17 → 18 → 20 → 17"
    #  ↑ Appended to the user message so Claude knows which metrics to prioritise

    # ── System prompt ─────────────────────────────────────────────────────────
    system_prompt = \"\"\"You are the Grain Optimization Expert for a solar panel manufacturing line.
You specialize in the recrystallization stage where semiconductor grains must grow to sufficient size.

Your control loop:
  Step 17 (Avg. Grain Diameter)  → Are grains large enough (target > 5 µm)?
  Step 18 (ΔT Achieved)          → Did the oven actually reach the required temperature?
  Step 20 (Grain Size Increase)  → Did grains grow by at least 15% during annealing?
  → Loop back to Step 17 to verify grain size is now acceptable

Why grain size matters: In CdTe/CIGS solar cells, larger grains mean fewer grain boundaries.
Grain boundaries act as recombination centers — electrons created by sunlight get trapped
there instead of flowing as useful current. Small grains = low efficiency.

Root causes of grain growth failure:
  - Insufficient annealing temperature (check Step 18 ΔT)
  - Too short residence time in the oven (check Step 24)
  - Rapid cooling causing thermal stress and micro-cracks (check Step 26)

Your analysis style:
- Explain grain physics in simple terms
- Identify which parameter in the loop is the primary cause
- End with specific corrective actions

Keep your response under 400 words.\"\"\"


# ── SK Plugin alias ───────────────────────────────────────────────────────────
# The Plugin suffix class makes this discoverable by the SK Kernel's plugin registry.
# In this project the triage agent instantiates experts directly, but the Plugin
# class enables future integration with SK's automatic tool-calling system.
class GrainOptimizationPlugin(GrainOptimizationExpert):
    pass
""", language="python")

with tab_base:
    st.markdown(
        "`BaseExpert` is inherited by all 12 experts. It holds the Anthropic client, "
        "builds the user message, and streams the response. No expert duplicates this logic."
    )
    st.code("""# agents/experts/base_expert.py
import os
from typing import Generator
import anthropic
from dotenv import load_dotenv

load_dotenv()


class BaseExpert:
    display_name: str = "Expert"
    loop_steps:   str = ""
    system_prompt: str = ""

    def __init__(self):
        # Each expert holds its own Anthropic client instance.
        # The model ID and key come from .env via dotenv.
        self._client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self._model  = os.getenv("MODEL_ID", "claude-sonnet-4-6")

    def analyze_stream(
        self,
        sensor_snapshot_str: str,    # formatted text block of all 50 metrics
        faulty_steps: list[dict],    # list of metrics currently in FAULT state
    ) -> Generator[str, None, None]:
        \"\"\"Stream expert analysis as raw text chunks.\"\"\"

        # Build the user message Claude will receive
        fault_summary = self._format_faults(faulty_steps)

        user_message = (
            f"You are being consulted about the following PV manufacturing fault.\\n\\n"
            f"FAULTY METRICS DETECTED:\\n{fault_summary}\\n\\n"
            f"FULL SENSOR SNAPSHOT:\\n{sensor_snapshot_str}\\n\\n"
            f"Please perform your specialist analysis following your "
            f"assigned control loop: {self.loop_steps}"
            #                        ↑ injected from the subclass
        )

        # Open a streaming request — yields text chunks as Claude generates them
        with self._client.messages.stream(
            model=self._model,
            max_tokens=1200,
            system=self.system_prompt,   # ← subclass attribute
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            for text in stream.text_stream:
                yield text               # each chunk is ~1–5 words

    def analyze_full(self, sensor_snapshot_str: str, faulty_steps: list[dict]) -> str:
        \"\"\"Collect the full streaming response into a single string (for report generation).\"\"\"
        return "".join(self.analyze_stream(sensor_snapshot_str, faulty_steps))

    @staticmethod
    def _format_faults(faulty_steps: list[dict]) -> str:
        \"\"\"Format the faulty metrics list into a readable bullet block for the prompt.\"\"\"
        if not faulty_steps:
            return "No metrics currently in FAULT state."
        lines = []
        for f in faulty_steps:
            direction = "above" if f["direction"] == "above" else "below"
            lines.append(
                f"  • [{f['step']}] {f['name']}: {f['value']} {f['unit']} "
                f"(threshold {direction} {f['threshold']}) — {f['error_type']}"
            )
        return "\\n".join(lines)
""", language="python")

with tab_flow:
    st.markdown(
        "This is the exact JSON body that leaves Python and hits the Anthropic API "
        "for the Grain Optimization Expert when a grain growth fault is active."
    )
    st.code("""{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1200,
  "system": "You are the Grain Optimization Expert for a solar panel manufacturing line. \\nYou specialize in the recrystallization stage...",

  "messages": [
    {
      "role": "user",
      "content": "You are being consulted about the following PV manufacturing fault.\\n\\n
FAULTY METRICS DETECTED:\\n
  • [step_17] Avg. Grain Diameter: 0.31 µm (threshold below 0.5) — Grain size insufficient for efficient carrier collection\\n
  • [step_18] ΔT Achieved: 78.2 % (threshold below 90) — Oven did not reach target temperature\\n\\n
FULL SENSOR SNAPSHOT:\\n
=== PV Manufacturing Sensor Snapshot ===\\n
Timestamp: 2026-04-26 14:32:11\\n
Fault Active: YES\\n
\\n
Stage 1: Surface Preparation\\n
  [step_1]  Engagement Status: 1.0 binary     | Normal: 1–1   | Status: OK\\n
  [step_2]  Particle Density:  42.3 /cm²      | Normal: 0–100 | Status: OK\\n
  [step_5]  O₂ Concentration:  3.1 ppm        | Normal: 0–5   | Status: OK\\n
...\\n
Stage 4: Grain Growth\\n
  [step_17] Avg. Grain Diameter: 0.31 µm      | Normal: 0.5–5 | Status: FAULT\\n
  [step_18] ΔT Achieved:         78.2 %       | Normal: 90–105| Status: FAULT\\n
  [step_20] Grain Size Increase: 8.4 %        | Normal: 15–40 | Status: WARNING\\n
...\\n\\n
Please perform your specialist analysis following your assigned control loop: Step 17 → 18 → 20 → 17"
    }
  ]
}
""", language="json")
    st.info(
        "The expert receives the **entire** sensor snapshot (all 50 metrics, all 7 stages) "
        "plus the pre-filtered fault list. This lets it see context outside its own control "
        "loop — important for cross-stage root cause analysis."
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Agent communication sequence diagram
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 4 · How the Central Agent and Expert Agents Communicate")
st.markdown(
    "The triage agent and expert agents do not communicate with each other directly — they each "
    "make **independent API calls to Claude**, and the Python orchestration layer in "
    "`triage_agent.py` sequences those calls and routes the streamed output to the UI. "
    "The diagram below shows the full message flow."
)

_SEQ_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: transparent; font-family: 'Segoe UI', sans-serif; padding: 10px 6px; }

.seq { display: grid; grid-template-columns: 110px 1fr 110px 1fr 110px 1fr 110px; gap: 0; }

/* actor headers */
.actor {
  background: #1e2130; border: 1.5px solid #2d3348;
  border-radius: 6px; padding: 7px 4px; text-align: center;
  font-size: 10px; font-weight: 700; color: #c8d8e8;
  margin: 0 4px;
}
.actor.ui     { border-color: #2a4a7a; }
.actor.triage { border-color: #2a6a9c; }
.actor.python { border-color: #6a4a0a; }
.actor.claude { border-color: #6a2a8a; }
.actor sub { display: block; font-size: 8px; color: #8899aa; font-weight: 400; margin-top: 2px; }

/* lifeline grid area */
.lifelines {
  display: grid;
  grid-template-columns: 110px 1fr 110px 1fr 110px 1fr 110px;
  margin-top: 4px;
}

/* a single step row */
.step {
  display: contents;
}

/* the vertical lifeline bar inside each actor column */
.lline {
  display: flex; justify-content: center;
  padding: 0 4px;
}
.lline-bar {
  width: 2px; background: #2a2d3a; min-height: 100%;
}

/* arrow + label spanning the gap between two actors */
.arrow-cell {
  display: flex; flex-direction: column; justify-content: center;
  padding: 10px 6px; font-size: 10px; color: #8899aa;
}
.arrow-cell .alabel {
  background: #1a1d27; border: 1px solid #2a2d3a; border-radius: 4px;
  padding: 4px 8px; font-size: 10px; color: #c8d8e8; text-align: center;
  margin-bottom: 4px;
}
.arrow-cell .aline {
  height: 1px; background: #3a4060; position: relative;
}
.arrow-cell .aline::after {
  content: ''; position: absolute; right: -1px; top: -4px;
  border: 5px solid transparent; border-left-color: #3a4060;
}
.arrow-cell .aline.left::after {
  right: auto; left: -1px;
  border-left-color: transparent; border-right-color: #3a4060;
}
.arrow-cell .aline.return { background: #2a3050; border-top: 1px dashed #3a4060; }
.arrow-cell .aline.return::after { border-left-color: #3a4060; }
.arrow-cell .aline.stream { background: #2a5020; }
.arrow-cell .aline.stream::after { border-left-color: #2a5020; }

/* phase labels */
.phase {
  grid-column: 1 / -1;
  background: #1a1d27; border-left: 3px solid #2a6a9c;
  padding: 5px 10px; font-size: 10px; font-weight: 700; color: #7eb3d4;
  margin: 8px 0 4px; border-radius: 0 4px 4px 0;
}

/* activation boxes on lifelines */
.active { background: #2a4a6a !important; width: 8px !important; margin: 0 auto; border-radius: 2px; }
</style></head><body>

<!-- Actor headers -->
<div class="seq">
  <div class="actor ui">Streamlit UI<sub>home.py</sub></div>
  <div></div>
  <div class="actor triage">Triage Agent<sub>triage_agent.py</sub></div>
  <div></div>
  <div class="actor python">Expert Agent<sub>grain_optimization.py</sub></div>
  <div></div>
  <div class="actor claude">Claude API<sub>api.anthropic.com</sub></div>
</div>

<!-- Lifelines + steps -->
<div class="lifelines">

  <!-- Phase 1 label -->
  <div class="phase">① Fault detected → Triage Agent activated</div>

  <!-- Step: UI calls render_agent_panel -->
  <div class="lline"><div class="lline-bar active"></div></div>
  <div class="arrow-cell">
    <div class="alabel">render_agent_panel(snapshot, scenario)</div>
    <div class="aline"></div>
  </div>
  <div class="lline"><div class="lline-bar active"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar"></div></div>

  <!-- Step: Triage calls format_snapshot -->
  <div class="lline"><div class="lline-bar"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar active"></div></div>
  <div class="arrow-cell" style="grid-column:4/7">
    <div class="alabel">format_snapshot_for_agent(snapshot) + get_faulty_steps(snapshot)</div>
    <div class="aline" style="background:#6a4a0a"></div>
  </div>
  <div class="lline"><div class="lline-bar"></div></div>

  <!-- Phase 2 -->
  <div class="phase">② Triage sends snapshot to Claude — streams assessment</div>

  <!-- Step: Triage → Claude -->
  <div class="lline"><div class="lline-bar"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar active"></div></div>
  <div class="arrow-cell" style="grid-column:4/8">
    <div class="alabel">POST /messages { system: TRIAGE_SYSTEM_PROMPT, user: fault_summary + snapshot, max_tokens: 600 }</div>
    <div class="aline"></div>
  </div>

  <!-- Step: Claude streams → Triage -->
  <div class="lline"><div class="lline-bar"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar active"></div></div>
  <div class="arrow-cell" style="grid-column:4/8">
    <div class="alabel">stream: "Fault Assessment… Why This Expert… Initial Hypothesis…"</div>
    <div class="aline stream left"></div>
  </div>

  <!-- Step: Triage yields to UI -->
  <div class="lline"><div class="lline-bar active"></div></div>
  <div class="arrow-cell">
    <div class="alabel">yield ("triage", text_chunk) × N</div>
    <div class="aline left"></div>
  </div>
  <div class="lline"><div class="lline-bar active"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar"></div></div>

  <!-- Phase 3 -->
  <div class="phase">③ Python selects expert from EXPERT_MAP — instantiates it</div>

  <!-- Step: Triage instantiates expert -->
  <div class="lline"><div class="lline-bar"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar active"></div></div>
  <div class="arrow-cell">
    <div class="alabel">EXPERT_MAP["grain_optimization"]() → GrainOptimizationExpert()</div>
    <div class="aline"></div>
  </div>
  <div class="lline"><div class="lline-bar active"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar"></div></div>

  <!-- Phase 4 -->
  <div class="phase">④ Expert sends same snapshot to Claude — streams specialist analysis</div>

  <!-- Step: Expert → Claude -->
  <div class="lline"><div class="lline-bar"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar active"></div></div>
  <div class="arrow-cell">
    <div class="alabel">POST /messages { system: GRAIN_SYSTEM_PROMPT, user: fault_summary + snapshot + loop_steps, max_tokens: 1200 }</div>
    <div class="aline"></div>
  </div>
  <div class="lline"><div class="lline-bar active"></div></div>

  <!-- Step: Claude streams → Expert -->
  <div class="lline"><div class="lline-bar"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar active"></div></div>
  <div class="arrow-cell">
    <div class="alabel">stream: "Step 17 shows… Step 18 shows… Root cause: insufficient anneal…"</div>
    <div class="aline stream left"></div>
  </div>
  <div class="lline"><div class="lline-bar active"></div></div>

  <!-- Step: Expert → Triage yields to UI -->
  <div class="lline"><div class="lline-bar active"></div></div>
  <div class="arrow-cell">
    <div class="alabel">yield ("expert_primary", text_chunk) × N</div>
    <div class="aline left"></div>
  </div>
  <div class="lline"><div class="lline-bar active"></div></div>
  <div class="arrow-cell">
    <div class="alabel">for chunk in expert.analyze_stream(…): yield ("expert_primary", chunk)</div>
    <div class="aline left"></div>
  </div>
  <div class="lline"><div class="lline-bar active"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar"></div></div>

  <!-- Phase 5 -->
  <div class="phase">⑤ UI routes each (speaker, chunk) to the correct chat bubble</div>

  <!-- Step: UI renders -->
  <div class="lline"><div class="lline-bar active"></div></div>
  <div class="arrow-cell" style="grid-column:1/3;font-size:9px;color:#7eb3d4;">
    st.chat_message("🤖") → triage chunks<br>st.chat_message("👨‍🔬") → expert chunks
  </div>
  <div class="lline"><div class="lline-bar"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar"></div></div>
  <div></div>
  <div class="lline"><div class="lline-bar"></div></div>

</div>
</body></html>
"""
st.components.v1.html(apply_theme(_SEQ_HTML), height=820)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — The orchestration code
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 5 · The Orchestration Code")
st.markdown(
    "The key insight: the triage agent and expert agents do **not** communicate via LLM "
    "tool-calling or function-calling. The triage agent's text output is what the human audience "
    "sees — the actual expert routing decision is made by Python reading the fault scenario's "
    "`primary_expert` and `secondary_expert` fields. Both agents receive the same sensor snapshot "
    "but reason about it independently using different system prompts."
)

tab_orch, tab_ui, tab_msg = st.tabs(["Triage Orchestrator", "UI Routing Layer", "Message Structure Comparison"])

with tab_orch:
    st.markdown("**`agents/triage_agent.py` — the core orchestration logic (simplified)**")
    st.code("""class TriageAgent:
    def __init__(self):
        self._client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self._model  = os.getenv("MODEL_ID", "claude-sonnet-4-6")

    def analyze_stream(self, snapshot, scenario):
        # ── Prepare shared context ────────────────────────────────────────────
        snapshot_str = format_snapshot_for_agent(snapshot)   # all 50 metrics as text
        faulty_steps = get_faulty_steps(snapshot)            # only FAULT-state metrics
        fault_summary = self._format_fault_summary(faulty_steps)

        # ── Phase 1: Triage assessment ────────────────────────────────────────
        yield ("system", "Initiating centralized reasoning agent...")

        # Independent API call — triage agent sees the snapshot with its own system prompt
        with self._client.messages.stream(
            model=self._model,
            max_tokens=600,
            system=TRIAGE_SYSTEM_PROMPT,          # ← defines the triage role
            messages=[{"role": "user", "content":
                f"ANOMALOUS METRICS:\\n{fault_summary}\\n\\n"
                f"FULL SENSOR SNAPSHOT:\\n{snapshot_str}\\n\\n"
                f"Please perform your triage assessment."
            }],
        ) as stream:
            for text in stream.text_stream:
                yield ("triage", text)            # ← tagged so the UI knows which bubble

        # ── Phase 2: Expert routing ───────────────────────────────────────────
        # Python — not the LLM — decides which expert to call.
        # The fault scenario JSON already specifies primary_expert and secondary_expert.
        primary_key    = scenario.get("primary_expert", "quality_control")
        primary_expert = EXPERT_MAP[primary_key]()   # instantiate from registry

        yield ("system", f"Routing to: {primary_expert.display_name}")

        # Expert makes its own independent API call using its own system_prompt
        for chunk in primary_expert.analyze_stream(snapshot_str, faulty_steps):
            yield ("expert_primary", chunk)          # ← different tag

        # ── Phase 3: Optional secondary expert ───────────────────────────────
        secondary_key = scenario.get("secondary_expert")
        if secondary_key and secondary_key != primary_key:
            secondary_expert = EXPERT_MAP[secondary_key]()
            yield ("system", f"Cross-checking with: {secondary_expert.display_name}")
            for chunk in secondary_expert.analyze_stream(snapshot_str, faulty_steps):
                yield ("expert_secondary", chunk)    # ← third tag

        yield ("system", "Analysis complete.")
""", language="python")

with tab_ui:
    st.markdown("**`ui/agent_panel.py` — routing `(speaker, chunk)` tuples to Streamlit chat bubbles**")
    st.code("""def render_agent_panel(snapshot, scenario):
    agent = TriageAgent()

    current_speaker     = None
    current_container   = None
    current_placeholder = None
    current_buffer      = ""

    for speaker, chunk in agent.analyze_stream(snapshot, scenario):

        # ── System messages ───────────────────────────────────────────────
        if speaker == "system":
            if current_placeholder and current_buffer:
                current_placeholder.markdown(current_buffer)   # flush current bubble
                current_buffer = ""
            st.markdown(chunk)     # system messages render as plain markdown
            current_speaker = None
            continue

        # ── New speaker → open a new chat bubble ─────────────────────────
        if speaker != current_speaker:
            if current_placeholder and current_buffer:
                current_placeholder.markdown(current_buffer)
                current_buffer = ""

            avatar = {"triage": "🤖", "expert_primary": "👨‍🔬", "expert_secondary": "🔍"}[speaker]

            current_container   = st.chat_message(avatar)
            with current_container:
                current_placeholder = st.empty()

            current_speaker = speaker

        # ── Accumulate chunk and update placeholder live ──────────────────
        current_buffer += chunk

        with current_container:
            current_placeholder.markdown(current_buffer + "▌")   # ▌ = typing cursor

    # Final flush — remove typing cursor
    if current_placeholder and current_buffer:
        with current_container:
            current_placeholder.markdown(current_buffer)
""", language="python")

with tab_msg:
    st.markdown(
        "The triage agent and the expert agent each send a **separate, independent** HTTP request "
        "to the Anthropic API. Here is a side-by-side comparison of the two message structures."
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Triage Agent API call**")
        st.code("""{
  "model": "claude-sonnet-4-6",
  "max_tokens": 600,
  "system":
    "You are the Central Reasoning Agent
     for a near-closed-loop PV solar panel
     manufacturing system. You are the first
     responder when a fault is detected...
     [300 words defining triage role]",

  "messages": [{
    "role": "user",
    "content":
      "A fault has been detected.

       ANOMALOUS METRICS:
         • [step_17] Avg. Grain Diameter:
           0.31 µm (below threshold 0.5)
         • [step_18] ΔT Achieved:
           78.2% (below threshold 90)

       FULL SENSOR SNAPSHOT:
         Stage 1: Surface Prep … OK
         Stage 2: PVD Deposition … OK
         Stage 3: CdCl₂ Activation … OK
         Stage 4: Grain Growth … FAULT
         ...all 50 metrics...

       Please perform your triage assessment."
  }]
}""", language="json")

    with c2:
        st.markdown("**Grain Optimization Expert API call**")
        st.code("""{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1200,
  "system":
    "You are the Grain Optimization Expert
     for a solar panel manufacturing line.
     You specialize in the recrystallization
     stage...
     [expert domain knowledge + loop steps]",

  "messages": [{
    "role": "user",
    "content":
      "You are being consulted about the
       following PV manufacturing fault.

       FAULTY METRICS DETECTED:
         • [step_17] Avg. Grain Diameter:
           0.31 µm — Grain size insufficient
         • [step_18] ΔT Achieved:
           78.2% — Oven did not reach target

       FULL SENSOR SNAPSHOT:
         Stage 1: Surface Prep … OK
         Stage 2: PVD Deposition … OK
         ...all 50 metrics...

       Please perform your specialist analysis
       following your assigned control loop:
       Step 17 → 18 → 20 → 17"
  }]
}""", language="json")

    st.markdown(
        "**Key differences:**\n"
        "- The **triage agent** gets 600 max tokens and is told to assess, classify, and route\n"
        "- The **expert** gets 1200 max tokens and is told to perform deep specialist analysis\n"
        "- The **system prompt** is entirely different — triage knows about all 12 experts; "
        "the expert only knows about its own 3-step control loop\n"
        "- The **user message** is the same sensor snapshot, but the expert's version appends its `loop_steps` string as a final instruction\n"
        "- Neither agent sees the other's response — they reason independently over the same data"
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — SK's role summary
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 6 · What SK Contributes vs. What Python Handles")

col_sk, col_py = st.columns(2)

with col_sk:
    st.markdown(
        apply_theme(
            "<div style='background:#0f1f35;border:1.5px solid #2a6a9c;border-radius:8px;padding:14px;'>"
            "<div style='font-size:13px;font-weight:800;color:#a0d4ff;margin-bottom:8px;'>🔵 Semantic Kernel</div>"
            "<ul style='font-size:12px;color:#8eb3d4;line-height:2;list-style:none;padding:0;'>"
            "<li>✓ <code>AnthropicChatCompletion</code> — wraps the Anthropic SDK into SK's provider-agnostic interface</li>"
            "<li>✓ <code>Kernel.add_service()</code> — central service registry</li>"
            "<li>✓ Plugin class pattern — makes expert classes discoverable by the Kernel</li>"
            "<li>✓ Provider abstraction — swap Claude for GPT-4 by changing one line in kernel_setup.py</li>"
            "<li>✓ Future path — SK's <code>ChatCompletionAgent</code> and automatic tool-calling for fully autonomous routing</li>"
            "</ul></div>"
        ),
        unsafe_allow_html=True,
    )

with col_py:
    st.markdown(
        apply_theme(
            "<div style='background:#1a1f0a;border:1.5px solid #4a6a0a;border-radius:8px;padding:14px;'>"
            "<div style='font-size:13px;font-weight:800;color:#a0d4a0;margin-bottom:8px;'>🟢 Python Orchestration</div>"
            "<ul style='font-size:12px;color:#8eb3b4;line-height:2;list-style:none;padding:0;'>"
            "<li>✓ Expert routing — reads <code>primary_expert</code> from the fault scenario JSON</li>"
            "<li>✓ Streaming pipeline — sequences triage → primary → secondary as a Python generator</li>"
            "<li>✓ Speaker tagging — labels each chunk with 'triage' / 'expert_primary' / 'expert_secondary'</li>"
            "<li>✓ UI rendering — routes tagged chunks to the correct <code>st.chat_message()</code> bubble</li>"
            "<li>✓ Report assembly — collects full text per speaker and passes to python-docx exporter</li>"
            "</ul></div>"
        ),
        unsafe_allow_html=True,
    )

st.markdown("")
st.markdown(
    apply_theme(
        "<div style='text-align:center; color:#556677; font-size:11px; margin-top:8px;'>"
        "This architecture follows the paper's design: a <em>centralized reasoning agent</em> "
        "coordinating <em>specialist expert sub-agents</em>, implemented with Semantic Kernel as the "
        "AI service layer and Python as the orchestration layer."
        "</div>"
    ),
    unsafe_allow_html=True,
)
