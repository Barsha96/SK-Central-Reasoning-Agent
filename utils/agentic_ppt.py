"""
Standalone PowerPoint generator: Agentic AI Systems — From Concept to Production.
Run directly:  python utils/agentic_ppt.py
Outputs:       Agentic_Systems_Overview.pptx  in the project root.
"""
from io import BytesIO
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt, Emu

# ── Colour palette ─────────────────────────────────────────────────────────────
BG     = RGBColor(0x0a, 0x0d, 0x14)
PANEL  = RGBColor(0x11, 0x18, 0x27)
DPANEL = RGBColor(0x0f, 0x14, 0x20)
BORDER = RGBColor(0x1e, 0x2d, 0x45)

BLUE   = RGBColor(0x5a, 0xb4, 0xe8)
LBLUE  = RGBColor(0x3a, 0x80, 0xb8)
DBLUE  = RGBColor(0x1e, 0x3a, 0x5a)
ORANGE = RGBColor(0xf0, 0xa8, 0x30)
DORNG  = RGBColor(0x3a, 0x28, 0x08)
GREEN  = RGBColor(0x27, 0xae, 0x60)
DGRN   = RGBColor(0x0f, 0x2a, 0x18)
PURPLE = RGBColor(0x9b, 0x59, 0xb6)
DPUR   = RGBColor(0x28, 0x10, 0x38)
TEAL   = RGBColor(0x1a, 0xbc, 0x9c)
RED    = RGBColor(0xe7, 0x4c, 0x3c)
AMBER  = RGBColor(0xf3, 0x9c, 0x12)

TEXT   = RGBColor(0xe8, 0xf0, 0xf8)
TDIM   = RGBColor(0x7a, 0x9a, 0xb8)
MUTED  = RGBColor(0x4a, 0x6a, 0x9c)
WHITE  = RGBColor(0xff, 0xff, 0xff)

W = Inches(13.333)
H = Inches(7.5)

# ── Low-level helpers ──────────────────────────────────────────────────────────

def _bg(slide, color: RGBColor):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def _rect(slide, x, y, w, h, fill=PANEL, line=BORDER, lw=0.75, radius=False):
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    shape = slide.shapes.add_shape(1, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line:
        shape.line.color.rgb = line
        shape.line.width = Pt(lw)
    else:
        shape.line.fill.background()
    return shape


def _tb(slide, text, x, y, w, h,
        size=11, color=TEXT, bold=False,
        align=PP_ALIGN.LEFT, wrap=True, italic=False, spacing=1.0):
    txb = slide.shapes.add_textbox(x, y, w, h)
    tf  = txb.text_frame
    tf.word_wrap = wrap
    for i, line in enumerate(text.split("\n")):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        run = para.add_run()
        run.text = line
        run.font.size  = Pt(size)
        run.font.color.rgb = color
        run.font.bold  = bold
        run.font.italic = italic
    return txb


def _tb2(slide, runs, x, y, w, h, size=11, align=PP_ALIGN.LEFT):
    """runs = list of (text, color, bold, italic) tuples — all on one paragraph."""
    txb = slide.shapes.add_textbox(x, y, w, h)
    tf  = txb.text_frame
    tf.word_wrap = True
    para = tf.paragraphs[0]
    para.alignment = align
    for text, color, bold, italic in runs:
        for i, part in enumerate(text.split("\n")):
            if i > 0:
                para = tf.add_paragraph()
                para.alignment = align
            run = para.add_run()
            run.text = part
            run.font.size = Pt(size)
            run.font.color.rgb = color
            run.font.bold = bold
            run.font.italic = italic
    return txb


def _label(slide, text, x, y, color=MUTED):
    _tb(slide, text, x, y, Inches(6), Inches(0.25),
        size=8, color=color, bold=True)


def _stripe(slide, color=BLUE):
    _rect(slide, 0, 0, W, Inches(0.055), fill=color, line=None)


def _hline(slide, x, y, w, color=BORDER):
    _rect(slide, x, y, w, Pt(1), fill=color, line=None)

# ── Slide builders ─────────────────────────────────────────────────────────────

def _slide1_title(prs, blank):
    """Cover + Agenda."""
    slide = prs.slides.add_slide(blank)
    _bg(slide, BG)

    # left accent column
    _rect(slide, 0, 0, Inches(0.35), H, fill=BLUE, line=None)

    # title block
    _tb(slide, "Agentic AI Systems",
        Inches(0.7), Inches(1.1), Inches(7.5), Inches(1.0),
        size=40, color=TEXT, bold=True)
    _tb(slide, "From Concept to Production",
        Inches(0.7), Inches(2.0), Inches(7.5), Inches(0.5),
        size=22, color=BLUE, bold=False)
    _tb(slide, "Architecture · Frameworks · Real-World Integration",
        Inches(0.7), Inches(2.5), Inches(7.5), Inches(0.35),
        size=13, color=TDIM)

    _hline(slide, Inches(0.7), Inches(2.95), Inches(6.5), BORDER)

    # agenda
    _tb(slide, "AGENDA",
        Inches(0.7), Inches(3.1), Inches(3), Inches(0.3),
        size=8, color=MUTED, bold=True)

    agenda = [
        ("01", "What is an Agentic System?"),
        ("02", "Development of Agentic Systems"),
        ("03", "What Agentic Systems Enable"),
        ("04", "Enabling Technologies"),
        ("05", "How to Plug In This System"),
        ("06", "Use Case: Semantic Kernel in Practice"),
    ]
    for i, (num, label) in enumerate(agenda):
        y = Inches(3.5) + i * Inches(0.52)
        _tb(slide, num, Inches(0.7), y, Inches(0.5), Inches(0.45),
            size=10, color=BLUE, bold=True)
        _tb(slide, label, Inches(1.15), y, Inches(5.5), Inches(0.45),
            size=12, color=TEXT)

    # right decorative panel
    _rect(slide, Inches(8.4), Inches(0.8), Inches(4.6), Inches(5.8),
          fill=PANEL, line=BORDER)
    _tb(slide, "KEY THEMES",
        Inches(8.7), Inches(1.1), Inches(4.0), Inches(0.3),
        size=8, color=MUTED, bold=True)

    themes = [
        (BLUE,   "🧠", "Autonomous Reasoning"),
        (GREEN,  "🔧", "Tool-Using Agents"),
        (ORANGE, "🔄", "Closed-Loop Orchestration"),
        (PURPLE, "🏭", "Production Integration"),
        (TEAL,   "⚡", "Real-Time Decision Making"),
    ]
    for i, (col, icon, label) in enumerate(themes):
        y = Inches(1.55) + i * Inches(0.85)
        _rect(slide, Inches(8.7), y, Inches(4.0), Inches(0.72),
              fill=DPANEL, line=col, lw=1.5)
        _tb(slide, icon, Inches(8.85), y + Inches(0.15), Inches(0.4), Inches(0.45), size=16)
        _tb(slide, label, Inches(9.35), y + Inches(0.18), Inches(3.2), Inches(0.45),
            size=12, color=col, bold=True)

    _stripe(slide)


def _slide2_what(prs, blank):
    """What is an Agentic System?"""
    slide = prs.slides.add_slide(blank)
    _bg(slide, BG)
    _stripe(slide)

    _label(slide, "01 · WHAT IS AN AGENTIC SYSTEM?", Inches(0.5), Inches(0.15))
    _tb(slide, "An Agent that Perceives, Reasons, Acts — and Learns",
        Inches(0.5), Inches(0.45), Inches(9), Inches(0.65),
        size=26, color=TEXT, bold=True)
    _tb(slide, "An agentic system is an AI that autonomously pursues goals by interacting with its environment through tools and feedback loops.",
        Inches(0.5), Inches(1.05), Inches(9.5), Inches(0.45),
        size=12, color=TDIM)

    # 4-step loop
    steps = [
        (BLUE,   "PERCEIVE",  "Reads structured & unstructured inputs:\nAPIs, sensors, databases, documents, user messages"),
        (GREEN,  "REASON",    "Applies LLM-grade chain-of-thought:\ndecomposes goals, selects tools, plans sub-steps"),
        (ORANGE, "ACT",       "Calls external tools & APIs:\nwrites code, queries DBs, moves files, sends alerts"),
        (PURPLE, "LEARN",     "Updates context from results:\nreflects on outcomes, adapts strategy, escalates if needed"),
    ]
    for i, (col, title, desc) in enumerate(steps):
        x = Inches(0.5) + i * Inches(3.15)
        _rect(slide, x, Inches(1.65), Inches(2.95), Inches(2.15),
              fill=DPANEL, line=col, lw=2)
        _tb(slide, title, x + Inches(0.15), Inches(1.72), Inches(2.7), Inches(0.35),
            size=13, color=col, bold=True)
        _tb(slide, desc, x + Inches(0.15), Inches(2.08), Inches(2.7), Inches(1.6),
            size=10, color=TDIM)

    # arrows between boxes
    for i in range(3):
        ax = Inches(3.45) + i * Inches(3.15)
        _tb(slide, "→", ax, Inches(2.5), Inches(0.22), Inches(0.35),
            size=16, color=MUTED, bold=True, align=PP_ALIGN.CENTER)

    _hline(slide, Inches(0.5), Inches(3.95), Inches(12.3))

    # vs traditional AI
    _tb(slide, "VS. TRADITIONAL AI",
        Inches(0.5), Inches(4.05), Inches(4), Inches(0.3),
        size=8, color=MUTED, bold=True)

    cols_data = [
        ("Traditional ML / AI",   TDIM, ["Fixed input → output mapping", "Requires explicit feature engineering", "No environment interaction", "Batch or synchronous inference", "Human decides next step"]),
        ("Agentic AI System",      BLUE, ["Dynamic goal decomposition", "Self-directed tool selection", "Multi-step environment interaction", "Continuous feedback loop", "Agent decides AND executes next step"]),
    ]
    for ci, (header, col, items) in enumerate(cols_data):
        x = Inches(0.5) + ci * Inches(6.2)
        _rect(slide, x, Inches(4.4), Inches(6.0), Inches(2.7),
              fill=PANEL, line=col, lw=1.2)
        _tb(slide, header, x + Inches(0.15), Inches(4.5), Inches(5.7), Inches(0.35),
            size=12, color=col, bold=True)
        for j, item in enumerate(items):
            prefix = "✓" if ci == 1 else "·"
            _tb(slide, f"{prefix}  {item}",
                x + Inches(0.15), Inches(4.9) + j * Inches(0.4),
                Inches(5.7), Inches(0.38),
                size=10, color=TEXT if ci == 1 else TDIM)


def _slide3_dev(prs, blank):
    """Development of Agentic Systems — timeline."""
    slide = prs.slides.add_slide(blank)
    _bg(slide, BG)
    _stripe(slide, ORANGE)

    _label(slide, "02 · DEVELOPMENT OF AGENTIC SYSTEMS", Inches(0.5), Inches(0.15), ORANGE)
    _tb(slide, "Four Decades of Progress — One Paradigm Shift",
        Inches(0.5), Inches(0.45), Inches(12), Inches(0.65),
        size=26, color=TEXT, bold=True)

    # Timeline
    eras = [
        ("1980s–2000s", "Rule-Based\nExperts", RED,
         "Hand-crafted if/else decision trees.\nExpert systems like MYCIN.\nBrittle: any rule gap = failure.",
         ["MYCIN", "CLIPS", "Prolog", "Decision Trees"]),
        ("2010–2020", "Statistical\nML Agents", AMBER,
         "Learned policies from labelled data.\nDeep RL (AlphaGo, Atari).\nNeeds massive training data.",
         ["DQN", "PPO", "A3C", "AlphaGo", "OpenAI Five"]),
        ("2020–2023", "LLM-Powered\nAssistants", BLUE,
         "GPT-3/4 enable few-shot reasoning.\nChatGPT shifts public expectation.\nStill single-turn, no tool use.",
         ["GPT-3", "ChatGPT", "Claude 1/2", "PaLM"]),
        ("2023–Now", "Agentic\nOrchestration", GREEN,
         "Tool-calling + multi-step planning.\nFrameworks abstract orchestration.\nClosed-loop production systems.",
         ["GPT-4 Tools", "Claude 3/4", "Semantic Kernel", "LangGraph"]),
    ]

    for i, (era, title, col, desc, tags) in enumerate(eras):
        x = Inches(0.4) + i * Inches(3.2)

        # era pill
        _rect(slide, x, Inches(1.25), Inches(2.85), Inches(0.32),
              fill=col, line=None)
        _tb(slide, era, x + Inches(0.1), Inches(1.27), Inches(2.65), Inches(0.28),
            size=9, color=BG, bold=True, align=PP_ALIGN.CENTER)

        # card
        _rect(slide, x, Inches(1.6), Inches(2.85), Inches(4.8),
              fill=PANEL, line=col, lw=1.5)
        _tb(slide, title, x + Inches(0.15), Inches(1.7), Inches(2.6), Inches(0.7),
            size=14, color=col, bold=True)
        _tb(slide, desc, x + Inches(0.15), Inches(2.4), Inches(2.6), Inches(1.5),
            size=10, color=TDIM)

        _tb(slide, "KEY EXAMPLES", x + Inches(0.15), Inches(4.0), Inches(2.6), Inches(0.25),
            size=7, color=MUTED, bold=True)
        for j, tag in enumerate(tags):
            _rect(slide, x + Inches(0.15), Inches(4.3) + j * Inches(0.38),
                  Inches(2.55), Inches(0.3), fill=DPANEL, line=col, lw=0.5)
            _tb(slide, tag,
                x + Inches(0.25), Inches(4.32) + j * Inches(0.38),
                Inches(2.3), Inches(0.28), size=9, color=col)

    # bottom insight
    _rect(slide, Inches(0.4), Inches(6.7), Inches(12.5), Inches(0.5),
          fill=DORNG, line=ORANGE, lw=1)
    _tb2(slide, [
        ("Key insight: ", ORANGE, True, False),
        ("Each era didn't replace the last — agentic systems ", TEXT, False, False),
        ("incorporate", TEXT, True, False),
        (" ML, rules, and LLMs as composable layers inside an orchestration framework.", TEXT, False, False),
    ], Inches(0.6), Inches(6.73), Inches(12.1), Inches(0.44), size=11)


def _slide4_enable(prs, blank):
    """What agentic systems enable."""
    slide = prs.slides.add_slide(blank)
    _bg(slide, BG)
    _stripe(slide, GREEN)

    _label(slide, "03 · WHAT AGENTIC SYSTEMS ENABLE", Inches(0.5), Inches(0.15), GREEN)
    _tb(slide, "Capabilities Unlocked Beyond Traditional Automation",
        Inches(0.5), Inches(0.45), Inches(12), Inches(0.65),
        size=26, color=TEXT, bold=True)

    # 2×3 capability grid
    caps = [
        (GREEN,  "⚡", "Autonomous\nDecision-Making",
         "Agents evaluate conditions and choose actions without human prompting. "
         "Threshold crossings, anomaly detection, and corrective commands are issued in real time."),
        (BLUE,   "🔍", "Multi-Step\nReasoning",
         "Chain-of-thought decomposition breaks complex problems into verifiable sub-steps — "
         "tracing a QA failure back through 7 upstream stages, for example."),
        (ORANGE, "🛠️", "Dynamic\nTool Use",
         "Agents call APIs, query databases, run code, write files, send notifications — "
         "any tool exposed through a function schema becomes an agent action."),
        (PURPLE, "👥", "Multi-Agent\nCollaboration",
         "Specialist agents work in parallel or in sequence. A triage agent routes; "
         "domain experts analyse; a synthesis agent consolidates — no single bottleneck."),
        (TEAL,   "🔄", "Closed-Loop\nFeedback",
         "Agents observe the result of their action, re-evaluate, and iterate. "
         "Near-closed-loop control replaces brittle one-shot commands with adaptive correction."),
        (RED,    "📄", "Automated\nReporting",
         "Full audit trails, structured reports, and natural-language summaries are generated "
         "automatically — cutting post-incident documentation from hours to seconds."),
    ]
    for i, (col, icon, title, desc) in enumerate(caps):
        row, ci = divmod(i, 3)
        x = Inches(0.4) + ci * Inches(4.28)
        y = Inches(1.4) + row * Inches(2.6)
        _rect(slide, x, y, Inches(4.1), Inches(2.45), fill=PANEL, line=col, lw=1.5)
        _tb(slide, icon, x + Inches(0.2), y + Inches(0.12), Inches(0.5), Inches(0.45), size=20)
        _tb(slide, title, x + Inches(0.75), y + Inches(0.12), Inches(3.2), Inches(0.55),
            size=13, color=col, bold=True)
        _tb(slide, desc, x + Inches(0.2), y + Inches(0.7), Inches(3.7), Inches(1.6),
            size=10, color=TDIM)


def _slide5_tech(prs, blank):
    """Enabling Technologies."""
    slide = prs.slides.add_slide(blank)
    _bg(slide, BG)
    _stripe(slide, PURPLE)

    _label(slide, "04 · ENABLING TECHNOLOGIES", Inches(0.5), Inches(0.15), PURPLE)
    _tb(slide, "The Stack That Makes Agentic Systems Possible",
        Inches(0.5), Inches(0.45), Inches(12), Inches(0.65),
        size=26, color=TEXT, bold=True)

    layers = [
        (BLUE,   "LAYER 5 · Orchestration Frameworks",
         ["Semantic Kernel (Microsoft)", "LangChain / LangGraph", "LlamaIndex", "AutoGen", "CrewAI"],
         "Route between agents, manage tool registries, handle streaming and memory"),
        (GREEN,  "LAYER 4 · Foundation Models (LLMs)",
         ["Claude Sonnet / Opus 4 (Anthropic)", "GPT-4o / o1 (OpenAI)", "Gemini 1.5 Pro (Google)", "Llama 3.1 (Meta / Open)", "Mistral Large"],
         "Provide chain-of-thought reasoning, tool calling, and natural-language generation"),
        (ORANGE, "LAYER 3 · Memory & Knowledge",
         ["Vector DBs: Pinecone, Weaviate, Chroma", "Graph DBs: Neo4j, Amazon Neptune", "Relational: PostgreSQL + pgvector", "Structured caches: Redis", "Conversation buffers"],
         "Give agents long-term recall, semantic search, and context beyond the context window"),
        (PURPLE, "LAYER 2 · Tool & API Layer",
         ["REST / GraphQL APIs", "Code interpreters (Python sandbox)", "File I/O, browser control", "Database connectors", "IoT / SCADA sensor feeds"],
         "Every callable function becomes a potential agent action through a typed schema"),
        (TEAL,   "LAYER 1 · Infrastructure",
         ["Cloud: Azure, AWS, GCP", "On-prem / edge compute", "Containers: Docker / Kubernetes", "CI/CD: GitHub Actions", "Observability: LangSmith, Weights & Biases"],
         "Runs, monitors, and scales the agentic workload reliably"),
    ]

    for i, (col, header, items, note) in enumerate(layers):
        y = Inches(1.3) + i * Inches(1.1)
        _rect(slide, Inches(0.4), y, Inches(12.5), Inches(1.0), fill=PANEL, line=col, lw=1.2)
        _tb(slide, header, Inches(0.6), y + Inches(0.07), Inches(3.8), Inches(0.32),
            size=10, color=col, bold=True)
        _tb(slide, note, Inches(0.6), y + Inches(0.42), Inches(3.8), Inches(0.5),
            size=9, color=TDIM, italic=True)
        # tags
        for j, item in enumerate(items):
            tx = Inches(4.5) + j * Inches(1.68)
            _rect(slide, tx, y + Inches(0.2), Inches(1.6), Inches(0.58),
                  fill=DPANEL, line=col, lw=0.6)
            _tb(slide, item, tx + Inches(0.08), y + Inches(0.22), Inches(1.48), Inches(0.54),
                size=8, color=TEXT)


def _slide6_plugin(prs, blank):
    """How to plug in this system."""
    slide = prs.slides.add_slide(blank)
    _bg(slide, BG)
    _stripe(slide, TEAL)

    _label(slide, "05 · HOW TO PLUG IN THIS SYSTEM", Inches(0.5), Inches(0.15), TEAL)
    _tb(slide, "Four Integration Patterns — Choose What Fits Your Architecture",
        Inches(0.5), Inches(0.45), Inches(12), Inches(0.65),
        size=24, color=TEXT, bold=True)

    patterns = [
        (BLUE,   "Pattern A", "API-First Drop-In",
         "Your existing system exposes a REST endpoint.\n"
         "The agentic layer subscribes to events or polls.\n"
         "Zero changes to downstream services.\n"
         "→ Best for: brownfield systems with stable APIs."),
        (GREEN,  "Pattern B", "Event-Driven Sidecar",
         "An agent container runs alongside your app.\n"
         "Listens to message queue (Kafka / Event Hub).\n"
         "Fires when threshold events arrive.\n"
         "→ Best for: real-time IoT / sensor pipelines."),
        (ORANGE, "Pattern C", "Embedded SDK",
         "Import Semantic Kernel directly into your service.\n"
         "Agents live in the same process as business logic.\n"
         "Low latency; shared memory.\n"
         "→ Best for: greenfield apps or Python backends."),
        (PURPLE, "Pattern D", "Human-in-the-Loop Gateway",
         "Agent recommends; human approves via UI / Slack.\n"
         "Approval unlocks the next automated step.\n"
         "Full audit trail of every decision gate.\n"
         "→ Best for: regulated industries (finance, medical)."),
    ]

    for i, (col, tag, title, desc) in enumerate(patterns):
        x = Inches(0.4) + i * Inches(3.22)
        _rect(slide, x, Inches(1.35), Inches(3.05), Inches(3.4),
              fill=PANEL, line=col, lw=2)
        _rect(slide, x, Inches(1.35), Inches(3.05), Inches(0.32),
              fill=col, line=None)
        _tb(slide, tag, x + Inches(0.12), Inches(1.37), Inches(2.8), Inches(0.28),
            size=9, color=BG, bold=True)
        _tb(slide, title, x + Inches(0.12), Inches(1.72), Inches(2.8), Inches(0.4),
            size=13, color=col, bold=True)
        _tb(slide, desc, x + Inches(0.12), Inches(2.15), Inches(2.8), Inches(2.4),
            size=10, color=TEXT)

    # data flow diagram strip
    _hline(slide, Inches(0.4), Inches(4.9), Inches(12.5))
    _tb(slide, "DATA FLOW IN ALL PATTERNS",
        Inches(0.5), Inches(4.98), Inches(4), Inches(0.28),
        size=8, color=MUTED, bold=True)

    flow = [
        (BLUE,   "Data\nSources"),
        (GREEN,  "Triage\nAgent"),
        (ORANGE, "Expert\nAgents"),
        (PURPLE, "Tool\nCalls"),
        (TEAL,   "Output /\nAction"),
        (RED,    "Feedback\nLoop"),
    ]
    for i, (col, label) in enumerate(flow):
        x = Inches(0.4) + i * Inches(2.1)
        _rect(slide, x, Inches(5.3), Inches(1.85), Inches(0.85),
              fill=DPANEL, line=col, lw=1.5)
        _tb(slide, label, x + Inches(0.1), Inches(5.35), Inches(1.65), Inches(0.75),
            size=10, color=col, bold=True, align=PP_ALIGN.CENTER)
        if i < len(flow) - 1:
            _tb(slide, "→", x + Inches(1.85), Inches(5.5), Inches(0.25), Inches(0.4),
                size=14, color=MUTED, bold=True, align=PP_ALIGN.CENTER)

    _rect(slide, Inches(0.4), Inches(6.3), Inches(12.5), Inches(0.85),
          fill=DGRN, line=GREEN, lw=0.8)
    _tb2(slide, [
        ("Security note: ", GREEN, True, False),
        ("All agent tool calls should be wrapped in permission scopes. "
         "Use short-lived credentials, log every action, "
         "and gate high-impact actions (write, delete, send) behind explicit human approval.", TEXT, False, False),
    ], Inches(0.6), Inches(6.38), Inches(12.1), Inches(0.65), size=10)


def _slide7_sk(prs, blank):
    """Semantic Kernel use case — PV manufacturing."""
    slide = prs.slides.add_slide(blank)
    _bg(slide, BG)
    _stripe(slide, ORANGE)

    _label(slide, "06 · USE CASE — SEMANTIC KERNEL IN PRACTICE", Inches(0.5), Inches(0.15), ORANGE)
    _tb(slide, "Near-Closed-Loop PV Manufacturing Control",
        Inches(0.5), Inches(0.45), Inches(9), Inches(0.65),
        size=24, color=TEXT, bold=True)
    _tb(slide, "A real system built with Claude Sonnet 4.6 + Semantic Kernel to detect & diagnose faults across 7 solar panel production stages",
        Inches(0.5), Inches(1.05), Inches(12), Inches(0.38),
        size=11, color=TDIM)

    # left: architecture
    _tb(slide, "HOW SEMANTIC KERNEL WIRES IT TOGETHER",
        Inches(0.5), Inches(1.55), Inches(6), Inches(0.28),
        size=8, color=MUTED, bold=True)

    sk_steps = [
        (BLUE,   "1. Kernel + Connector",
         "AnthropicChatCompletion registered as the AI service.\n"
         "Model ID and API key loaded from .env — swap the model in one line."),
        (GREEN,  "2. Plugin Registration",
         "12 Expert plugins (one per control loop) registered on the Kernel.\n"
         "Each @kernel_function becomes a callable tool for Claude."),
        (ORANGE, "3. ChatCompletionAgent",
         "Triage Agent created with all 12 plugins in scope.\n"
         "System prompt instructs it to read a sensor snapshot and route."),
        (PURPLE, "4. Streaming Invocation",
         "agent.invoke_stream(snapshot) yields content chunks.\n"
         "Streamlit's write_stream() renders the live reasoning in the UI."),
    ]

    for i, (col, title, desc) in enumerate(sk_steps):
        y = Inches(1.9) + i * Inches(1.1)
        _rect(slide, Inches(0.5), y, Inches(5.9), Inches(1.0),
              fill=DPANEL, line=col, lw=1.5)
        _tb(slide, f"●  {title}", Inches(0.65), y + Inches(0.07), Inches(5.5), Inches(0.32),
            size=11, color=col, bold=True)
        _tb(slide, desc, Inches(0.8), y + Inches(0.4), Inches(5.4), Inches(0.55),
            size=9.5, color=TEXT)

    # right: code snippet
    _rect(slide, Inches(6.65), Inches(1.55), Inches(6.35), Inches(4.5),
          fill=RGBColor(0x06, 0x08, 0x10), line=BORDER)
    _tb(slide, "kernel_setup.py",
        Inches(6.8), Inches(1.6), Inches(4), Inches(0.28),
        size=8, color=MUTED, bold=True)
    code = (
        "from semantic_kernel import Kernel\n"
        "from semantic_kernel.connectors.ai\n"
        "  .anthropic import AnthropicChatCompletion\n"
        "\n"
        "def build_kernel() -> Kernel:\n"
        "    kernel = Kernel()\n"
        "    kernel.add_service(\n"
        "        AnthropicChatCompletion(\n"
        "            ai_model_id=os.getenv(\n"
        '                "MODEL_ID",\n'
        '                "claude-sonnet-4-6"),\n'
        "            api_key=os.getenv(\n"
        '                "ANTHROPIC_API_KEY")))\n'
        "    return kernel\n"
        "\n"
        "# Expert plugin (one of 12)\n"
        "class GrainOptimizationPlugin:\n"
        "    @kernel_function(\n"
        '        name="analyze_grain",\n'
        '        description="Grain growth loop")\n'
        "    def analyze(self, snapshot: str) -> str:\n"
        "        # Claude reasons over metrics\n"
        "        # 17→18→20→17 control loop\n"
        "        ..."
    )
    _tb(slide, code,
        Inches(6.8), Inches(1.95), Inches(6.0), Inches(3.9),
        size=8, color=RGBColor(0x90, 0xd4, 0x90))

    # bottom outcome
    outcomes = [
        (BLUE,   "50 metrics", "monitored across\n7 production stages"),
        (GREEN,  "< 3 seconds", "from fault trigger to\nroot cause diagnosis"),
        (ORANGE, "12 experts", "specialist agents,\none per control loop"),
        (PURPLE, "Auto .docx", "full report generated\nwithout human writing"),
    ]
    for i, (col, metric, label) in enumerate(outcomes):
        x = Inches(0.5) + i * Inches(3.22)
        _rect(slide, x, Inches(6.1), Inches(3.05), Inches(1.1),
              fill=PANEL, line=col, lw=1.2)
        _tb(slide, metric, x + Inches(0.15), Inches(6.15), Inches(2.75), Inches(0.42),
            size=18, color=col, bold=True)
        _tb(slide, label, x + Inches(0.15), Inches(6.55), Inches(2.75), Inches(0.55),
            size=9, color=TDIM)


def _slide8_summary(prs, blank):
    """Summary and Q&A."""
    slide = prs.slides.add_slide(blank)
    _bg(slide, BG)
    _stripe(slide)

    _label(slide, "SUMMARY & KEY TAKEAWAYS", Inches(0.5), Inches(0.15))
    _tb(slide, "Agentic Systems are Production-Ready Today",
        Inches(0.5), Inches(0.45), Inches(12), Inches(0.65),
        size=28, color=TEXT, bold=True)

    takeaways = [
        (BLUE,   "01", "Agentic AI = Perceive + Reason + Act + Learn",
         "It's not a chatbot — it's a goal-directed system that uses tools, maintains context, and adapts."),
        (GREEN,  "02", "Decades of evolution, now converging",
         "Rule engines, ML, and LLMs are all layers inside a modern orchestration framework."),
        (ORANGE, "03", "Enables automation beyond rigid scripts",
         "Multi-step reasoning, cross-domain specialist routing, and closed-loop correction are now achievable."),
        (PURPLE, "04", "The stack is mature and open",
         "Semantic Kernel, LangGraph, and AutoGen all expose production-grade orchestration for any LLM."),
        (TEAL,   "05", "Integration is pattern-driven, not disruptive",
         "API-first, event-driven, embedded SDK, or human-in-the-loop — pick the pattern that fits."),
        (RED,    "06", "Semantic Kernel proved it in PV manufacturing",
         "50 sensors · 12 expert agents · < 3-second diagnosis · auto-generated fault report."),
    ]

    for i, (col, num, title, desc) in enumerate(takeaways):
        row, ci = divmod(i, 2)
        x = Inches(0.4) + ci * Inches(6.45)
        y = Inches(1.35) + row * Inches(1.6)
        _rect(slide, x, y, Inches(6.25), Inches(1.45), fill=PANEL, line=col, lw=1.5)
        _tb(slide, num, x + Inches(0.15), y + Inches(0.12), Inches(0.5), Inches(0.4),
            size=14, color=col, bold=True)
        _tb(slide, title, x + Inches(0.65), y + Inches(0.1), Inches(5.4), Inches(0.38),
            size=12, color=col, bold=True)
        _tb(slide, desc, x + Inches(0.65), y + Inches(0.5), Inches(5.4), Inches(0.85),
            size=10, color=TDIM)

    # Q&A bar
    _rect(slide, Inches(0.4), Inches(6.55), Inches(12.5), Inches(0.65),
          fill=DBLUE, line=BLUE, lw=1)
    _tb2(slide, [
        ("Questions?  ", BLUE, True, False),
        ("Semantic Kernel docs: ", TDIM, False, False),
        ("learn.microsoft.com/semantic-kernel    ", TEXT, False, False),
        ("Claude API: ", TDIM, False, False),
        ("docs.anthropic.com", TEXT, False, False),
    ], Inches(0.6), Inches(6.6), Inches(12.1), Inches(0.55), size=11, align=PP_ALIGN.CENTER)


# ── Public entry point ─────────────────────────────────────────────────────────

def generate(output_path: str | None = None) -> bytes:
    """Build the presentation and return raw bytes (also saves if output_path given)."""
    prs = Presentation()
    prs.slide_width  = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    _slide1_title(prs, blank)
    _slide2_what(prs, blank)
    _slide3_dev(prs, blank)
    _slide4_enable(prs, blank)
    _slide5_tech(prs, blank)
    _slide6_plugin(prs, blank)
    _slide7_sk(prs, blank)
    _slide8_summary(prs, blank)

    buf = BytesIO()
    prs.save(buf)
    data = buf.getvalue()

    if output_path:
        Path(output_path).write_bytes(data)

    return data


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "Agentic_Systems_Overview.pptx"
    generate(out)
    print(f"Saved: {out}  ({Path(out).stat().st_size // 1024} KB)")
