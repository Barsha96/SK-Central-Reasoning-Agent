"""Introduction — slide-style presentation for IEEE PES Boston Chapter demo."""
import streamlit as st
from utils.ppt_exporter import generate_intro_ppt
from datetime import datetime

st.markdown("""
<style>
.stApp { background-color: #0a0d14; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }
.block-container { padding-top: 2rem !important; padding-bottom: 0.5rem !important; }
div[data-testid="stHorizontalBlock"] { gap: 6px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "intro_slide" not in st.session_state:
    st.session_state.intro_slide = 0

TOTAL_SLIDES = 6

def go(delta):
    st.session_state.intro_slide = max(0, min(TOTAL_SLIDES - 1, st.session_state.intro_slide + delta))

# ── Slide definitions ─────────────────────────────────────────────────────────
SLIDES = [

    # ── 0: AGENDA ─────────────────────────────────────────────────────────────
    dict(
        bg="#0a0d14",
        html="""
<div style="min-height:540px;display:flex;flex-direction:column;justify-content:center;padding:40px 60px;">

  <div style="font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#4a6a9c;font-weight:700;margin-bottom:16px;">
    IEEE PES Boston Chapter · April 2026
  </div>

  <div style="font-size:38px;font-weight:900;color:#e8f0f8;line-height:1.15;margin-bottom:8px;">
    Near-Closed-Loop Control<br>
    <span style="color:#5ab4e8;">in PV Manufacturing</span>
  </div>

  <div style="font-size:16px;color:#7a9ab8;margin-bottom:40px;font-weight:400;">
    A Centralized LLM Reasoning Agent with Semantic Kernel
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:720px;">

    <div style="background:#111827;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px;display:flex;gap:14px;align-items:flex-start;">
      <div style="font-size:22px;min-width:28px;">📡</div>
      <div>
        <div style="font-size:12px;font-weight:800;color:#5ab4e8;text-transform:uppercase;letter-spacing:1px;">01</div>
        <div style="font-size:14px;font-weight:700;color:#c8d8e8;margin-top:2px;">Current AI Landscape</div>
        <div style="font-size:11px;color:#5a7a9a;margin-top:3px;">From language models to autonomous agents</div>
      </div>
    </div>

    <div style="background:#111827;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px;display:flex;gap:14px;align-items:flex-start;">
      <div style="font-size:22px;min-width:28px;">🧠</div>
      <div>
        <div style="font-size:12px;font-weight:800;color:#5ab4e8;text-transform:uppercase;letter-spacing:1px;">02</div>
        <div style="font-size:14px;font-weight:700;color:#c8d8e8;margin-top:2px;">Agentic Frameworks</div>
        <div style="font-size:11px;color:#5a7a9a;margin-top:3px;">Semantic Kernel, Agent Studio &amp; more</div>
      </div>
    </div>

    <div style="background:#111827;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px;display:flex;gap:14px;align-items:flex-start;">
      <div style="font-size:22px;min-width:28px;">🚀</div>
      <div>
        <div style="font-size:12px;font-weight:800;color:#5ab4e8;text-transform:uppercase;letter-spacing:1px;">03</div>
        <div style="font-size:14px;font-weight:700;color:#c8d8e8;margin-top:2px;">What Is Achievable</div>
        <div style="font-size:11px;color:#5a7a9a;margin-top:3px;">Capabilities unlocked by multi-agent design</div>
      </div>
    </div>

    <div style="background:#111827;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px;display:flex;gap:14px;align-items:flex-start;">
      <div style="font-size:22px;min-width:28px;">🏭</div>
      <div>
        <div style="font-size:12px;font-weight:800;color:#5ab4e8;text-transform:uppercase;letter-spacing:1px;">04</div>
        <div style="font-size:14px;font-weight:700;color:#c8d8e8;margin-top:2px;">Industry Applications</div>
        <div style="font-size:11px;color:#5a7a9a;margin-top:3px;">Real-world impact across sectors</div>
      </div>
    </div>

    <div style="background:#111827;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px;display:flex;gap:14px;align-items:flex-start;grid-column:1/-1;max-width:340px;">
      <div style="font-size:22px;min-width:28px;">☀️</div>
      <div>
        <div style="font-size:12px;font-weight:800;color:#f0a830;text-transform:uppercase;letter-spacing:1px;">05</div>
        <div style="font-size:14px;font-weight:700;color:#c8d8e8;margin-top:2px;">PV Manufacturing — Live Demo</div>
        <div style="font-size:11px;color:#5a7a9a;margin-top:3px;">Fault detection in a 7-stage production line</div>
      </div>
    </div>

  </div>

  <div style="margin-top:36px;font-size:11px;color:#2a4a6a;">
    Barsha Upadhyaya · University of Toledo · IEEE PES Boston Chapter
  </div>
</div>
"""),

    # ── 1: AI LANDSCAPE ───────────────────────────────────────────────────────
    dict(
        bg="#0a0d14",
        html="""
<div style="min-height:540px;display:flex;flex-direction:column;justify-content:center;padding:40px 60px;">

  <div style="font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#4a6a9c;font-weight:700;margin-bottom:12px;">01 · AI Landscape</div>
  <div style="font-size:32px;font-weight:900;color:#e8f0f8;line-height:1.2;margin-bottom:6px;">
    The Shift from <span style="color:#5ab4e8;">Answering</span> to <span style="color:#f0a830;">Acting</span>
  </div>
  <div style="font-size:14px;color:#5a7a9a;margin-bottom:32px;">How AI evolved from a search box to an autonomous decision-maker</div>

  <!-- Timeline -->
  <div style="display:flex;align-items:flex-start;gap:0;margin-bottom:28px;position:relative;">

    <div style="position:absolute;top:28px;left:60px;right:60px;height:2px;background:linear-gradient(90deg,#1e3a5c,#2a6a9c,#f0a830);z-index:0;"></div>

    <div style="flex:1;text-align:center;position:relative;z-index:1;">
      <div style="width:14px;height:14px;border-radius:50%;background:#1e3a5c;border:2px solid #5ab4e8;margin:21px auto 10px;"></div>
      <div style="font-size:10px;font-weight:800;color:#5ab4e8;">2017–2020</div>
      <div style="font-size:12px;color:#c8d8e8;font-weight:700;margin-top:4px;">Large Language<br>Models</div>
      <div style="font-size:10px;color:#4a6a8a;margin-top:4px;">GPT-2, BERT<br>Text generation<br>Single-turn Q&A</div>
    </div>

    <div style="flex:1;text-align:center;position:relative;z-index:1;">
      <div style="width:14px;height:14px;border-radius:50%;background:#1e3a5c;border:2px solid #5ab4e8;margin:21px auto 10px;"></div>
      <div style="font-size:10px;font-weight:800;color:#5ab4e8;">2021–2022</div>
      <div style="font-size:12px;color:#c8d8e8;font-weight:700;margin-top:4px;">Instruction<br>Tuning</div>
      <div style="font-size:10px;color:#4a6a8a;margin-top:4px;">ChatGPT, InstructGPT<br>Conversational AI<br>Task completion</div>
    </div>

    <div style="flex:1;text-align:center;position:relative;z-index:1;">
      <div style="width:14px;height:14px;border-radius:50%;background:#1e3a5c;border:2px solid #5ab4e8;margin:21px auto 10px;"></div>
      <div style="font-size:10px;font-weight:800;color:#5ab4e8;">2023–2024</div>
      <div style="font-size:12px;color:#c8d8e8;font-weight:700;margin-top:4px;">Tool Use &amp;<br>Function Calling</div>
      <div style="font-size:10px;color:#4a6a8a;margin-top:4px;">GPT-4, Claude 3<br>API integration<br>Code execution</div>
    </div>

    <div style="flex:1;text-align:center;position:relative;z-index:1;">
      <div style="width:18px;height:18px;border-radius:50%;background:#f0a830;border:2px solid #f0a830;margin:19px auto 10px;box-shadow:0 0 10px #f0a83066;"></div>
      <div style="font-size:10px;font-weight:800;color:#f0a830;">2025–Now</div>
      <div style="font-size:12px;color:#f0a830;font-weight:800;margin-top:4px;">Agentic<br>Systems</div>
      <div style="font-size:10px;color:#a07030;margin-top:4px;">Multi-agent teams<br>Autonomous loops<br>Real-world control</div>
    </div>

  </div>

  <!-- Key insight -->
  <div style="background:#0f1a2a;border-left:4px solid #5ab4e8;border-radius:0 8px 8px 0;padding:16px 20px;margin-bottom:20px;">
    <div style="font-size:13px;font-weight:800;color:#5ab4e8;margin-bottom:6px;">The fundamental shift</div>
    <div style="font-size:13px;color:#a0b8d0;line-height:1.6;">
      Early AI systems were <strong style="color:#e8f0f8">reactive</strong> — they answered what you asked.
      Agentic AI is <strong style="color:#f0a830">proactive</strong> — it monitors, decides, and acts in closed loops
      without waiting for a human to ask the question. The model is no longer the product;
      the <em>system of models</em> is.
    </div>
  </div>

  <div style="display:flex;gap:12px;">
    <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:12px 16px;flex:1;font-size:11px;color:#5a7a9a;text-align:center;">
      <div style="font-size:20px;margin-bottom:4px;">🔍</div>
      <strong style="color:#c8d8e8;display:block;">Perceive</strong>
      Read sensors, logs, databases, user signals
    </div>
    <div style="font-size:18px;color:#2a4060;display:flex;align-items:center;">→</div>
    <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:12px 16px;flex:1;font-size:11px;color:#5a7a9a;text-align:center;">
      <div style="font-size:20px;margin-bottom:4px;">🧠</div>
      <strong style="color:#c8d8e8;display:block;">Reason</strong>
      Identify root cause across complex context
    </div>
    <div style="font-size:18px;color:#2a4060;display:flex;align-items:center;">→</div>
    <div style="background:#111827;border:1px solid #1e2d45;border-radius:8px;padding:12px 16px;flex:1;font-size:11px;color:#5a7a9a;text-align:center;">
      <div style="font-size:20px;margin-bottom:4px;">⚡</div>
      <strong style="color:#c8d8e8;display:block;">Act</strong>
      Issue commands, generate reports, alert humans
    </div>
    <div style="font-size:18px;color:#2a4060;display:flex;align-items:center;">→</div>
    <div style="background:#111827;border:1px solid #f0a83033;border-radius:8px;padding:12px 16px;flex:1;font-size:11px;color:#5a7a9a;text-align:center;">
      <div style="font-size:20px;margin-bottom:4px;">🔄</div>
      <strong style="color:#f0a830;display:block;">Loop</strong>
      Verify outcome, adapt, repeat
    </div>
  </div>

</div>
"""),

    # ── 2: AGENTIC FRAMEWORKS ─────────────────────────────────────────────────
    dict(
        bg="#0a0d14",
        html="""
<div style="min-height:540px;display:flex;flex-direction:column;justify-content:center;padding:40px 60px;">

  <div style="font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#4a6a9c;font-weight:700;margin-bottom:12px;">02 · Agentic Frameworks</div>
  <div style="font-size:32px;font-weight:900;color:#e8f0f8;line-height:1.2;margin-bottom:6px;">
    The Orchestration Layer
  </div>
  <div style="font-size:14px;color:#5a7a9a;margin-bottom:28px;">Frameworks that turn a single LLM into a coordinated team of specialists</div>

  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:24px;">

    <div style="background:#0f1a2a;border:1.5px solid #2a6a9c;border-radius:10px;padding:18px 16px;">
      <div style="font-size:13px;font-weight:900;color:#5ab4e8;margin-bottom:6px;">⚙️ Semantic Kernel</div>
      <div style="font-size:10px;color:#3a6a9a;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Microsoft · Open Source</div>
      <div style="font-size:11px;color:#8ab0c8;line-height:1.7;">
        Provider-agnostic orchestration SDK. Registers AI services (OpenAI, Claude, Gemini), defines <em>Plugins</em> as callable expert units, and manages multi-step agent pipelines in Python or C#.
      </div>
      <div style="margin-top:10px;font-size:10px;color:#2a5a8a;">
        ✓ Used in this demo &nbsp;·&nbsp; ✓ Anthropic connector &nbsp;·&nbsp; ✓ Production-ready
      </div>
    </div>

    <div style="background:#0f1a1a;border:1.5px solid #2a7a5a;border-radius:10px;padding:18px 16px;">
      <div style="font-size:13px;font-weight:900;color:#50d4a0;margin-bottom:6px;">🏗 Microsoft Agent Studio</div>
      <div style="font-size:10px;color:#3a8a5a;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Low-Code · Azure</div>
      <div style="font-size:11px;color:#80b0a0;line-height:1.7;">
        GUI-based builder on top of Semantic Kernel. Drag-and-drop agent topologies, visual prompt editing, and built-in monitoring. Targets enterprise teams without deep ML expertise.
      </div>
      <div style="margin-top:10px;font-size:10px;color:#2a6a4a;">
        ✓ Azure integration &nbsp;·&nbsp; ✓ Copilot Studio successor &nbsp;·&nbsp; ✓ Teams / M365
      </div>
    </div>

    <div style="background:#1a0f1a;border:1.5px solid #7a3a9a;border-radius:10px;padding:18px 16px;">
      <div style="font-size:13px;font-weight:900;color:#c080e0;margin-bottom:6px;">🔗 Other Frameworks</div>
      <div style="font-size:10px;color:#6a3a8a;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Ecosystem</div>
      <div style="font-size:11px;color:#a080c0;line-height:1.7;">
        <strong style="color:#c8b0e8;">LangGraph</strong> — stateful graph-based agent workflows<br>
        <strong style="color:#c8b0e8;">AutoGen</strong> — Microsoft's conversational multi-agent debates<br>
        <strong style="color:#c8b0e8;">CrewAI</strong> — role-based agent crews with human-in-loop<br>
        <strong style="color:#c8b0e8;">LlamaIndex</strong> — retrieval-augmented agent pipelines
      </div>
    </div>

  </div>

  <!-- SK anatomy -->
  <div style="background:#0f1420;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px;">
    <div style="font-size:12px;font-weight:800;color:#7eb3d4;margin-bottom:10px;">Semantic Kernel — key primitives used in this system</div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;">

      <div style="background:#0a1020;border:1px solid #1a3a5a;border-radius:6px;padding:8px 12px;min-width:160px;">
        <div style="font-size:11px;font-weight:800;color:#5ab4e8;">Kernel</div>
        <div style="font-size:10px;color:#4a6a8a;margin-top:2px;">Central service container — holds the Claude connector and all plugin registrations</div>
      </div>

      <div style="background:#0a1020;border:1px solid #1a3a5a;border-radius:6px;padding:8px 12px;min-width:160px;">
        <div style="font-size:11px;font-weight:800;color:#5ab4e8;">AnthropicChatCompletion</div>
        <div style="font-size:10px;color:#4a6a8a;margin-top:2px;">SK's Claude adapter — wraps api.anthropic.com behind a provider-agnostic interface</div>
      </div>

      <div style="background:#0a1020;border:1px solid #1a3a5a;border-radius:6px;padding:8px 12px;min-width:160px;">
        <div style="font-size:11px;font-weight:800;color:#5ab4e8;">Plugin classes</div>
        <div style="font-size:10px;color:#4a6a8a;margin-top:2px;">Each of the 12 expert agents is a SK Plugin — a named, callable unit the Kernel can discover</div>
      </div>

      <div style="background:#0a1020;border:1px solid #1a3a5a;border-radius:6px;padding:8px 12px;min-width:160px;">
        <div style="font-size:11px;font-weight:800;color:#5ab4e8;">Streaming API</div>
        <div style="font-size:10px;color:#4a6a8a;margin-top:2px;">Token-by-token streaming from Claude to the UI — the "thinking out loud" effect</div>
      </div>

    </div>
  </div>

</div>
"""),

    # ── 3: WHAT IS ACHIEVABLE ─────────────────────────────────────────────────
    dict(
        bg="#0a0d14",
        html="""
<div style="min-height:580px;display:flex;flex-direction:column;justify-content:center;padding:20px 56px 16px;">

  <div style="font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#4a6a9c;font-weight:700;margin-bottom:8px;">03 · Capabilities</div>
  <div style="font-size:30px;font-weight:900;color:#e8f0f8;line-height:1.2;margin-bottom:4px;">
    What Multi-Agent Systems <span style="color:#5ab4e8;">Unlock</span>
  </div>
  <div style="font-size:13px;color:#5a7a9a;margin-bottom:18px;">Capabilities that emerge when you orchestrate multiple LLMs as a coordinated team</div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;">

    <div style="background:#0f1a2a;border:1px solid #1e3a5a;border-radius:10px;padding:12px 14px;display:flex;gap:12px;align-items:flex-start;">
      <div style="font-size:24px;line-height:1;padding-top:2px;">🎯</div>
      <div>
        <div style="font-size:12px;font-weight:800;color:#5ab4e8;margin-bottom:4px;">Specialised Division of Labour</div>
        <div style="font-size:11px;color:#7a9ab8;line-height:1.55;">
          Each agent has a focused system prompt and narrow domain. A grain growth expert knows CdTe physics;
          a contamination expert knows cleanroom science. No single prompt needs to know everything.
        </div>
      </div>
    </div>

    <div style="background:#0f1a2a;border:1px solid #1e3a5a;border-radius:10px;padding:12px 14px;display:flex;gap:12px;align-items:flex-start;">
      <div style="font-size:24px;line-height:1;padding-top:2px;">🔄</div>
      <div>
        <div style="font-size:12px;font-weight:800;color:#5ab4e8;margin-bottom:4px;">Closed-Loop Autonomous Operation</div>
        <div style="font-size:11px;color:#7a9ab8;line-height:1.55;">
          Agents observe sensor data, reason about anomalies, and issue corrective actions —
          all without human initiation. The loop closes faster than any operator managing 50 concurrent metrics.
        </div>
      </div>
    </div>

    <div style="background:#0f1a2a;border:1px solid #1e3a5a;border-radius:10px;padding:12px 14px;display:flex;gap:12px;align-items:flex-start;">
      <div style="font-size:24px;line-height:1;padding-top:2px;">🔍</div>
      <div>
        <div style="font-size:12px;font-weight:800;color:#5ab4e8;margin-bottom:4px;">Cross-Agent Verification</div>
        <div style="font-size:11px;color:#7a9ab8;line-height:1.55;">
          A second expert independently reviews the same data and challenges or confirms the primary diagnosis —
          mirroring peer review to reduce hallucination before action is taken.
        </div>
      </div>
    </div>

    <div style="background:#0f1a2a;border:1px solid #1e3a5a;border-radius:10px;padding:12px 14px;display:flex;gap:12px;align-items:flex-start;">
      <div style="font-size:24px;line-height:1;padding-top:2px;">🧑‍💼</div>
      <div>
        <div style="font-size:12px;font-weight:800;color:#5ab4e8;margin-bottom:4px;">Human-in-the-Loop Escalation</div>
        <div style="font-size:11px;color:#7a9ab8;line-height:1.55;">
          Agents identify when physical inspection is needed, generate structured escalation reports,
          and route to the right human role — without replacing judgment for safety-critical decisions.
        </div>
      </div>
    </div>

  </div>

  <!-- Comparison row -->
  <div style="display:grid;grid-template-columns:1fr 32px 1fr;gap:8px;align-items:stretch;">

    <div style="background:#0a120a;border:1px solid #1a3a1a;border-radius:8px;padding:10px 14px;">
      <div style="font-size:11px;font-weight:800;color:#60a060;margin-bottom:6px;">Single LLM approach</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:2px 10px;font-size:10px;color:#4a6a4a;line-height:1.6;">
        <div>✗ One massive prompt for all domains</div>
        <div>✗ Slower — one call to answer everything</div>
        <div>✗ Context window fills with irrelevant data</div>
        <div>✗ Hard to explain which expertise was applied</div>
        <div>✗ No second opinion</div>
        <div></div>
      </div>
    </div>

    <div style="display:flex;align-items:center;justify-content:center;font-size:16px;color:#2a4060;font-weight:700;">vs</div>

    <div style="background:#0a1020;border:1.5px solid #2a6a9c;border-radius:8px;padding:10px 14px;">
      <div style="font-size:11px;font-weight:800;color:#5ab4e8;margin-bottom:6px;">Multi-agent system</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:2px 10px;font-size:10px;color:#4a6a8a;line-height:1.6;">
        <div>✓ Focused prompts per specialist domain</div>
        <div>✓ Parallel capability, sequential reasoning</div>
        <div>✓ Each agent sees only relevant context</div>
        <div>✓ Transparent: visible which agent said what</div>
        <div>✓ Cross-checking by secondary expert</div>
        <div></div>
      </div>
    </div>

  </div>

</div>
"""),

    # ── 4: INDUSTRY APPLICATIONS ──────────────────────────────────────────────
    dict(
        bg="#0a0d14",
        html="""
<div style="min-height:540px;display:flex;flex-direction:column;justify-content:center;padding:20px 56px 16px;">

  <div style="font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#4a6a9c;font-weight:700;margin-bottom:8px;">04 · Industry Impact</div>
  <div style="font-size:30px;font-weight:900;color:#e8f0f8;line-height:1.2;margin-bottom:4px;">
    Agentic AI Across Sectors
  </div>
  <div style="font-size:13px;color:#5a7a9a;margin-bottom:16px;">The same orchestration pattern adapts to any domain where expert knowledge must act on live data</div>

  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:12px;">

    <div style="background:#111827;border-top:3px solid #e74c3c;border-radius:0 0 8px 8px;padding:10px 12px;">
      <div style="font-size:16px;margin-bottom:4px;">🏥</div>
      <div style="font-size:11px;font-weight:800;color:#e87070;margin-bottom:4px;">Healthcare</div>
      <div style="font-size:10px;color:#7a9a9a;line-height:1.55;">
        <strong style="color:#c8d8d8;">Diagnostic support</strong> — radiology + pathology agents cross-check imaging<br>
        <strong style="color:#c8d8d8;">ICU monitoring</strong> — vital sign agents flag deterioration in real time<br>
        <strong style="color:#c8d8d8;">Drug discovery</strong> — chemistry + toxicology agents screen candidates
      </div>
    </div>

    <div style="background:#111827;border-top:3px solid #f39c12;border-radius:0 0 8px 8px;padding:10px 12px;">
      <div style="font-size:16px;margin-bottom:4px;">💹</div>
      <div style="font-size:11px;font-weight:800;color:#e8b060;margin-bottom:4px;">Finance</div>
      <div style="font-size:10px;color:#7a9a8a;line-height:1.55;">
        <strong style="color:#c8d8c8;">Fraud detection</strong> — transaction, behavioural &amp; network agents triage<br>
        <strong style="color:#c8d8c8;">Risk management</strong> — macro, credit &amp; liquidity agents hold guardrails<br>
        <strong style="color:#c8d8c8;">Compliance</strong> — regulatory agents monitor trades against rulebooks
      </div>
    </div>

    <div style="background:#111827;border-top:3px solid #27ae60;border-radius:0 0 8px 8px;padding:10px 12px;">
      <div style="font-size:16px;margin-bottom:4px;">⚡</div>
      <div style="font-size:11px;font-weight:800;color:#60e890;margin-bottom:4px;">Energy &amp; Grid</div>
      <div style="font-size:10px;color:#7a9a7a;line-height:1.55;">
        <strong style="color:#c8e8c8;">Grid stability</strong> — load, generation &amp; storage agents balance supply<br>
        <strong style="color:#c8e8c8;">Renewable forecasting</strong> — weather + demand agents optimise dispatch<br>
        <strong style="color:#c8e8c8;">Fault isolation</strong> — protection agents localise faults before cascade
      </div>
    </div>

    <div style="background:#111827;border-top:3px solid #9b59b6;border-radius:0 0 8px 8px;padding:10px 12px;">
      <div style="font-size:16px;margin-bottom:4px;">✈️</div>
      <div style="font-size:11px;font-weight:800;color:#c090e0;margin-bottom:4px;">Aerospace &amp; Defence</div>
      <div style="font-size:10px;color:#9a8ab0;line-height:1.55;">
        <strong style="color:#d8c8e8;">Predictive maintenance</strong> — engine, avionics &amp; structural agents<br>
        <strong style="color:#d8c8e8;">Mission planning</strong> — logistics &amp; threat-assessment agents<br>
        <strong style="color:#d8c8e8;">Supply chain</strong> — inventory agents anticipate AOG part shortages
      </div>
    </div>

    <div style="background:#111827;border-top:3px solid #1abc9c;border-radius:0 0 8px 8px;padding:10px 12px;">
      <div style="font-size:16px;margin-bottom:4px;">🏭</div>
      <div style="font-size:11px;font-weight:800;color:#60d4b8;margin-bottom:4px;">Smart Manufacturing</div>
      <div style="font-size:10px;color:#7aaa9a;line-height:1.55;">
        <strong style="color:#c8e8e0;">Quality control</strong> — vision + process agents detect defects live<br>
        <strong style="color:#c8e8e0;">Yield optimisation</strong> — recipe agents adjust parameters to spec<br>
        <strong style="color:#c8e8e0;">OEE improvement</strong> — downtime, speed &amp; quality agents coordinate
      </div>
    </div>

    <div style="background:#111827;border-top:3px solid #e67e22;border-radius:0 0 8px 8px;padding:10px 12px;">
      <div style="font-size:16px;margin-bottom:4px;">⚖️</div>
      <div style="font-size:11px;font-weight:800;color:#e09050;margin-bottom:4px;">Legal &amp; Compliance</div>
      <div style="font-size:10px;color:#9a8070;line-height:1.55;">
        <strong style="color:#e8d0c0;">Contract review</strong> — clause, risk &amp; jurisdiction agents flag terms<br>
        <strong style="color:#e8d0c0;">Regulatory monitoring</strong> — policy agents track rule changes<br>
        <strong style="color:#e8d0c0;">Due diligence</strong> — financial, legal &amp; ESG agents run in parallel
      </div>
    </div>

  </div>

  <div style="background:#0f1420;border-left:4px solid #f0a830;border-radius:0 6px 6px 0;padding:9px 14px;font-size:11px;color:#a08040;">
    <strong style="color:#f0c060;">Common pattern across all sectors:</strong> a central reasoning agent receives live data,
    routes to the right specialist, and surfaces an actionable conclusion — faster than any human team could convene.
  </div>

</div>
"""),

    # ── 5: TRANSITION TO PV ───────────────────────────────────────────────────
    dict(
        bg="#0a0d14",
        html="""
<div style="min-height:540px;display:flex;flex-direction:column;justify-content:center;padding:40px 60px;">

  <div style="font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#f0a830;font-weight:700;margin-bottom:12px;">05 · Our Demo</div>
  <div style="font-size:32px;font-weight:900;color:#e8f0f8;line-height:1.2;margin-bottom:6px;">
    Applying This to <span style="color:#f0a830;">Solar Panel Manufacturing</span>
  </div>
  <div style="font-size:14px;color:#5a7a9a;margin-bottom:28px;">Why PV manufacturing is an ideal testbed for near-closed-loop agentic control</div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px;">

    <div>
      <div style="font-size:12px;font-weight:800;color:#f0a830;margin-bottom:10px;">The challenge</div>

      <div style="display:flex;flex-direction:column;gap:8px;">
        <div style="background:#1a1a0a;border:1px solid #3a3a0a;border-radius:6px;padding:10px 14px;font-size:11px;color:#a0a060;line-height:1.6;">
          <strong style="color:#e0e080;display:block;margin-bottom:3px;">50 sensors · 7 stages · millisecond faults</strong>
          No human operator can simultaneously track particle density, chamber pressure,
          grain diameter, laser deviation, and QA efficiency across a live production line.
        </div>
        <div style="background:#1a1a0a;border:1px solid #3a3a0a;border-radius:6px;padding:10px 14px;font-size:11px;color:#a0a060;line-height:1.6;">
          <strong style="color:#e0e080;display:block;margin-bottom:3px;">Cross-stage root causes</strong>
          A drop in QA efficiency (Stage 7) might trace back to incomplete CdCl₂ activation
          (Stage 3) — an expert in Stage 7 alone cannot see that.
        </div>
        <div style="background:#1a1a0a;border:1px solid #3a3a0a;border-radius:6px;padding:10px 14px;font-size:11px;color:#a0a060;line-height:1.6;">
          <strong style="color:#e0e080;display:block;margin-bottom:3px;">Cost of delayed diagnosis</strong>
          Each panel that fails QA has consumed full upstream cost. Catching a vacuum leak
          at Stage 2 saves the cost of 5 downstream stages of processing.
        </div>
      </div>
    </div>

    <div>
      <div style="font-size:12px;font-weight:800;color:#5ab4e8;margin-bottom:10px;">The agentic solution</div>

      <div style="display:flex;flex-direction:column;gap:6px;">

        <div style="display:flex;gap:10px;align-items:flex-start;background:#0f1a2a;border:1px solid #1e3a5a;border-radius:6px;padding:10px 14px;">
          <div style="font-size:18px;min-width:24px;">🧠</div>
          <div style="font-size:11px;color:#7a9ab8;line-height:1.6;">
            <strong style="color:#5ab4e8;">Central Reasoning Agent (Claude Sonnet 4.6)</strong><br>
            Receives all 50 metrics the moment a fault threshold is crossed. Identifies the anomaly,
            explains its significance, and selects the right expert.
          </div>
        </div>

        <div style="display:flex;gap:10px;align-items:flex-start;background:#0f1a2a;border:1px solid #1e3a5a;border-radius:6px;padding:10px 14px;">
          <div style="font-size:18px;min-width:24px;">👨‍🔬</div>
          <div style="font-size:11px;color:#7a9ab8;line-height:1.6;">
            <strong style="color:#5ab4e8;">12 Specialist Expert Agents</strong><br>
            Each covers one control loop from the research paper. They reason over the same snapshot
            but through the lens of their specific domain expertise.
          </div>
        </div>

        <div style="display:flex;gap:10px;align-items:flex-start;background:#0f1a2a;border:1px solid #1e3a5a;border-radius:6px;padding:10px 14px;">
          <div style="font-size:18px;min-width:24px;">📄</div>
          <div style="font-size:11px;color:#7a9ab8;line-height:1.6;">
            <strong style="color:#5ab4e8;">Autonomous Diagnostic Report</strong><br>
            The system generates a complete .docx fault analysis report — root cause, corrective actions,
            and full sensor snapshot — without any human writing a single line.
          </div>
        </div>

      </div>
    </div>

  </div>

  <div style="background:linear-gradient(90deg,#1a1a0a,#0f1a2a);border:1px solid #3a5a3a;border-radius:10px;padding:16px 22px;display:flex;align-items:center;gap:20px;">
    <div style="font-size:32px;">☀️</div>
    <div>
      <div style="font-size:13px;font-weight:800;color:#f0c060;margin-bottom:4px;">Ready to see it live?</div>
      <div style="font-size:11px;color:#7a9a7a;line-height:1.6;">
        Switch to the <strong style="color:#e0e0a0;">PV Stages</strong> tab to understand the manufacturing process,
        then open <strong style="color:#e0e0a0;">Live Demo</strong> to watch the AI agent detect and diagnose a
        real-time fault injection — from sensor anomaly to downloadable report in under 60 seconds.
      </div>
    </div>
  </div>

</div>
"""),

]

# ── Render current slide ───────────────────────────────────────────────────────
idx = st.session_state.intro_slide
slide = SLIDES[idx]

st.components.v1.html(f"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  background: {slide['bg']};
  font-family: 'Segoe UI', -apple-system, sans-serif;
  min-height: 560px;
}}
</style></head>
<body>{slide['html']}</body></html>
""", height=650, scrolling=False)

# ── Navigation bar ─────────────────────────────────────────────────────────────
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

nav_left, nav_dots, nav_right = st.columns([1, 4, 1])

with nav_left:
    if idx > 0:
        if st.button("← Back", use_container_width=True):
            go(-1)
            st.rerun()

with nav_dots:
    LABELS = ["Agenda", "AI Landscape", "Agentic Frameworks", "What's Achievable", "Industry Impact", "PV Manufacturing"]
    dots_html = "<div style='display:flex;justify-content:center;align-items:center;gap:10px;padding:6px 0;'>"
    for i, label in enumerate(LABELS):
        if i == idx:
            dots_html += (
                f"<div style='display:flex;align-items:center;gap:6px;'>"
                f"<div style='width:10px;height:10px;border-radius:50%;background:#5ab4e8;box-shadow:0 0 6px #5ab4e888;'></div>"
                f"<span style='font-size:11px;font-weight:700;color:#5ab4e8;'>{label}</span>"
                f"</div>"
            )
        else:
            dots_html += f"<div style='width:7px;height:7px;border-radius:50%;background:#2a3050;'></div>"
    dots_html += "</div>"
    st.markdown(dots_html, unsafe_allow_html=True)

with nav_right:
    if idx < TOTAL_SLIDES - 1:
        if st.button("Next →", use_container_width=True):
            go(1)
            st.rerun()

# Slide counter
st.markdown(
    f"<div style='text-align:center;font-size:10px;color:#2a3a5a;margin-top:2px;'>"
    f"Slide {idx + 1} of {TOTAL_SLIDES}</div>",
    unsafe_allow_html=True,
)

# ── Download button ────────────────────────────────────────────────────────────
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
_, col_dl, _ = st.columns([2, 3, 2])
with col_dl:
    ppt_bytes = generate_intro_ppt()
    fname = f"IEEE_PES_Introduction_{datetime.now().strftime('%Y%m%d')}.pptx"
    st.download_button(
        label="⬇ Download Slides (.pptx)",
        data=ppt_bytes,
        file_name=fname,
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        use_container_width=True,
    )
