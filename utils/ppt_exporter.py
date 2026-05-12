"""Generate a PowerPoint presentation matching the Introduction slides."""
from __future__ import annotations
from io import BytesIO

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Colour palette ────────────────────────────────────────────────────────────
BG        = RGBColor(0x0a, 0x0d, 0x14)
CARD      = RGBColor(0x11, 0x18, 0x27)
DCARD     = RGBColor(0x0f, 0x1a, 0x2a)
BORDER    = RGBColor(0x1e, 0x2d, 0x45)
BRBR      = RGBColor(0x2a, 0x6a, 0x9c)
BLUE      = RGBColor(0x5a, 0xb4, 0xe8)
ORANGE    = RGBColor(0xf0, 0xa8, 0x30)
GREEN     = RGBColor(0x27, 0xae, 0x60)
PURPLE    = RGBColor(0x9b, 0x59, 0xb6)
TEAL      = RGBColor(0x1a, 0xbc, 0x9c)
RED       = RGBColor(0xe7, 0x4c, 0x3c)
AMBER     = RGBColor(0xe6, 0x7e, 0x22)
TEXT      = RGBColor(0xe8, 0xf0, 0xf8)
TDIM      = RGBColor(0x7a, 0x9a, 0xb8)
MUTED     = RGBColor(0x4a, 0x6a, 0x9c)
DK_OLIVE  = RGBColor(0x1a, 0x1a, 0x0a)
OL_BORD   = RGBColor(0x3a, 0x3a, 0x0a)
OL_TEXT   = RGBColor(0xa0, 0xa0, 0x60)
OL_HEAD   = RGBColor(0xe0, 0xe0, 0x80)
XDARK     = RGBColor(0x0a, 0x10, 0x20)
NEG_BG    = RGBColor(0x0a, 0x12, 0x0a)
NEG_BORD  = RGBColor(0x1a, 0x3a, 0x1a)
NEG_TEXT  = RGBColor(0x4a, 0x6a, 0x4a)
NEG_HEAD  = RGBColor(0x60, 0xa0, 0x60)


# ── Low-level helpers ─────────────────────────────────────────────────────────

def _bg(slide, color: RGBColor) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def _rect(slide, x, y, w, h, fill=CARD, line=BORDER, lw: float = 0.75):
    """Filled rectangle. All dimensions in inches."""
    shp = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(lw)
    return shp


def _tb(slide, text: str, x, y, w, h,
        size=11, color=TEXT, bold=False,
        align=PP_ALIGN.LEFT, wrap=True) -> None:
    """Text box with optional newline splitting into separate paragraphs."""
    txb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf  = txb.text_frame
    tf.word_wrap   = wrap
    tf.margin_left = tf.margin_right = tf.margin_bottom = 0
    tf.margin_top  = Pt(2)

    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text           = line
        run.font.size      = Pt(size)
        run.font.color.rgb = color
        run.font.bold      = bold


def _tb2(slide, runs: list[tuple[str, RGBColor, bool]],
         x, y, w, h, size=11, align=PP_ALIGN.LEFT) -> None:
    """Text box with mixed-colour runs in a single paragraph."""
    txb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf  = txb.text_frame
    tf.word_wrap   = True
    tf.margin_left = tf.margin_right = tf.margin_bottom = 0
    tf.margin_top  = Pt(2)
    p = tf.paragraphs[0]
    p.alignment = align
    for text, color, bold in runs:
        run = p.add_run()
        run.text           = text
        run.font.size      = Pt(size)
        run.font.color.rgb = color
        run.font.bold      = bold


def _label(slide, text: str, x, y) -> None:
    _tb(slide, text, x, y, 12, 0.25, size=8, color=MUTED, bold=True)


def _stripe(slide, color=BLUE) -> None:
    """Thin top accent bar."""
    _rect(slide, 0, 0, 13.333, 0.055, fill=color, line=None)


# ── Slide builders ─────────────────────────────────────────────────────────────

def _slide1_agenda(prs, blank) -> None:
    s = prs.slides.add_slide(blank)
    _bg(s, BG)
    _stripe(s, BLUE)

    _tb(s, "April 2026",
        0.6, 0.18, 12, 0.28, size=9, color=MUTED)
    _tb2(s, [
            ("Near-Closed-Loop Control in ", TEXT, True),
            ("PV Manufacturing", BLUE, True),
        ], 0.6, 0.5, 12.5, 0.8, size=30)
    _tb(s, "A Centralized LLM Reasoning Agent with Semantic Kernel",
        0.6, 1.28, 12, 0.35, size=14, color=TDIM)

    agenda = [
        ("01", "Current AI Landscape",          "From language models to autonomous agents"),
        ("02", "Agentic Frameworks",             "Semantic Kernel, Agent Studio & more"),
        ("03", "What Is Achievable",             "Capabilities unlocked by multi-agent design"),
        ("04", "Industry Applications",          "Real-world impact across sectors"),
        ("05", "PV Manufacturing — Live Demo",   "Fault detection in a 7-stage production line"),
    ]
    xs   = [0.6, 7.0,  0.6, 7.0,  0.6]
    ys   = [1.85, 1.85, 3.45, 3.45, 5.05]
    ws   = [6.1, 6.1,  6.1, 6.1,  12.7]

    for i, (num, title, desc) in enumerate(agenda):
        x, y, w = xs[i], ys[i], ws[i]
        _rect(s, x, y, w, 1.42, fill=CARD, line=BORDER)
        _tb(s, num,   x+0.18, y+0.12, 2,    0.26, size=9,  color=BLUE,  bold=True)
        _tb(s, title, x+0.18, y+0.42, w-0.4, 0.34, size=12, color=TEXT,  bold=True)
        _tb(s, desc,  x+0.18, y+0.82, w-0.4, 0.46, size=10, color=TDIM)

    _tb(s, "Barsha Upadhyaya",
        0.6, 7.18, 12, 0.26, size=8, color=RGBColor(0x2a, 0x4a, 0x6a))


def _slide2_landscape(prs, blank) -> None:
    s = prs.slides.add_slide(blank)
    _bg(s, BG)
    _stripe(s)

    _label(s, "01  ·  AI LANDSCAPE", 0.6, 0.18)
    _tb2(s, [("The Shift from ", TEXT, True), ("Answering", BLUE, True),
             (" to ", TEXT, True), ("Acting", ORANGE, True)],
         0.6, 0.45, 12.5, 0.72, size=28)
    _tb(s, "How AI evolved from a search box to an autonomous decision-maker",
        0.6, 1.14, 12, 0.3, size=12, color=TDIM)

    # Timeline cards
    tl = [
        ("2017 – 2020", "Large Language\nModels",
         "GPT-2, BERT\nText generation\nSingle-turn Q&A",        BLUE,   CARD,  BORDER,  0.75),
        ("2021 – 2022", "Instruction\nTuning",
         "ChatGPT, InstructGPT\nConversational AI\nTask completion", BLUE, CARD,  BORDER,  0.75),
        ("2023 – 2024", "Tool Use &\nFunction Calling",
         "GPT-4, Claude 3\nAPI integration\nCode execution",       BLUE,  CARD,  BORDER,  0.75),
        ("2025 – Now",  "Agentic\nSystems",
         "Multi-agent teams\nAutonomous loops\nReal-world control", ORANGE, DCARD, ORANGE, 1.5),
    ]
    bw = 2.92
    for i, (yr, ttl, dsc, ac, bg, bc, lw) in enumerate(tl):
        x = 0.6 + i * 3.18
        _rect(s, x, 1.55, bw, 2.05, fill=bg, line=bc, lw=lw)
        _tb(s, yr,  x+0.18, 1.63, bw-0.36, 0.28, size=9,  color=ac, bold=True)
        _tb(s, ttl, x+0.18, 1.97, bw-0.36, 0.5,  size=11, color=ac if i==3 else TEXT, bold=True)
        _tb(s, dsc, x+0.18, 2.55, bw-0.36, 0.9,  size=9,  color=TDIM)

    # Key insight
    _rect(s, 0.6, 3.76, 12.0, 1.05, fill=DCARD, line=BLUE, lw=1.5)
    _rect(s, 0.6, 3.76, 0.07, 1.05, fill=BLUE, line=None)
    _tb(s, "The fundamental shift",
        0.82, 3.84, 11, 0.3, size=11, color=BLUE, bold=True)
    _tb(s, ("Early AI was reactive — it answered what you asked. Agentic AI is proactive — "
            "it monitors, decides, and acts in closed loops without waiting for a human to ask. "
            "The model is no longer the product; the system of models is."),
        0.82, 4.18, 11.3, 0.55, size=10, color=TDIM)

    # Perceive → Reason → Act → Loop
    flow = [
        ("Perceive",  "Read sensors,\nlogs, databases"),
        ("Reason",    "Identify root cause\nacross context"),
        ("Act",       "Issue commands,\nalert humans"),
        ("Loop",      "Verify outcome,\nadapt, repeat"),
    ]
    fw = 2.6
    for j, (ft, fd) in enumerate(flow):
        fx = 0.6 + j * (fw + 0.57)
        bg = RGBColor(0x1a, 0x1d, 0x27) if j == 3 else CARD
        bc = ORANGE if j == 3 else BORDER
        _rect(s, fx, 4.97, fw, 1.35, fill=bg, line=bc)
        _tb(s, ft, fx+0.18, 5.07, fw-0.36, 0.35, size=11,
            color=ORANGE if j == 3 else TEXT, bold=True)
        _tb(s, fd, fx+0.18, 5.46, fw-0.36, 0.75, size=9, color=TDIM)
        if j < 3:
            _tb(s, "→", fx+fw+0.1, 5.52, 0.42, 0.35, size=14,
                color=BRBR, align=PP_ALIGN.CENTER)


def _slide3_frameworks(prs, blank) -> None:
    s = prs.slides.add_slide(blank)
    _bg(s, BG)
    _stripe(s)

    _label(s, "02  ·  AGENTIC FRAMEWORKS", 0.6, 0.18)
    _tb(s, "The Orchestration Layer", 0.6, 0.45, 12, 0.7, size=28, color=TEXT, bold=True)
    _tb(s, "Frameworks that turn a single LLM into a coordinated team of specialists",
        0.6, 1.14, 12, 0.3, size=12, color=TDIM)

    cards = [
        ("Semantic Kernel",      "Microsoft  ·  Open Source",
         ("Provider-agnostic orchestration SDK. Registers AI services (OpenAI, Claude, Gemini), "
          "defines Plugins as callable expert units, and manages multi-step agent pipelines in "
          "Python or C#."),
         "Used in this demo  ·  Anthropic connector  ·  Production-ready",
         BLUE,   RGBColor(0x0f,0x1f,0x35), BRBR),
        ("Microsoft Agent Studio", "Low-Code  ·  Azure",
         ("GUI-based builder on top of Semantic Kernel. Drag-and-drop agent topologies, visual "
          "prompt editing, and built-in monitoring for enterprise teams without deep ML expertise."),
         "Azure integration  ·  Copilot Studio successor  ·  Teams / M365",
         RGBColor(0x50,0xd4,0xa0), RGBColor(0x0f,0x1a,0x1a), RGBColor(0x2a,0x7a,0x5a)),
        ("Other Frameworks",    "Ecosystem",
         ("LangGraph — stateful graph-based agent workflows\n"
          "AutoGen — conversational multi-agent debates (Microsoft)\n"
          "CrewAI — role-based agent crews with human-in-loop\n"
          "LlamaIndex — retrieval-augmented agent pipelines"),
         "",
         RGBColor(0xc0,0x90,0xe0), RGBColor(0x1a,0x0f,0x1a), RGBColor(0x7a,0x3a,0x9a)),
    ]
    cw = 3.97
    for i, (ct, cs, cd, cn, col, bg, bc) in enumerate(cards):
        x = 0.6 + i * 4.27
        _rect(s, x, 1.55, cw, 3.75, fill=bg, line=bc, lw=1.5)
        _tb(s, ct, x+0.18, 1.65, cw-0.36, 0.36, size=12, color=col, bold=True)
        _tb(s, cs, x+0.18, 2.06, cw-0.36, 0.26, size=8,  color=MUTED, bold=True)
        _tb(s, cd, x+0.18, 2.38, cw-0.36, 2.1,  size=9.5, color=TDIM)
        if cn:
            _tb(s, cn, x+0.18, 5.0, cw-0.36, 0.26, size=8, color=MUTED)

    # SK primitives
    _rect(s, 0.6, 5.52, 12.0, 1.82, fill=XDARK, line=BORDER)
    _tb(s, "Semantic Kernel — key primitives used in this system",
        0.78, 5.59, 11, 0.28, size=10, color=BLUE, bold=True)
    prims = [
        ("Kernel",                   "Central service container — holds the Claude connector and all plugin registrations"),
        ("AnthropicChatCompletion",  "SK's Claude adapter — wraps api.anthropic.com behind a provider-agnostic interface"),
        ("Plugin classes",           "Each of the 12 expert agents is an SK Plugin — named, callable, and discoverable"),
        ("Streaming API",            "Token-by-token streaming from Claude to the UI — the live 'thinking out loud' effect"),
    ]
    pw = 2.88
    for j, (pn, pd) in enumerate(prims):
        px = 0.78 + j * 3.07
        _rect(s, px, 5.95, pw, 1.26, fill=RGBColor(0x07,0x0c,0x18), line=BORDER)
        _tb(s, pn, px+0.12, 6.02, pw-0.24, 0.28, size=9,   color=BLUE, bold=True)
        _tb(s, pd, px+0.12, 6.34, pw-0.24, 0.78, size=8.5, color=TDIM)


def _slide4_capabilities(prs, blank) -> None:
    s = prs.slides.add_slide(blank)
    _bg(s, BG)
    _stripe(s)

    _label(s, "03  ·  CAPABILITIES", 0.6, 0.18)
    _tb2(s, [("What Multi-Agent Systems ", TEXT, True), ("Unlock", BLUE, True)],
         0.6, 0.45, 12.5, 0.7, size=28)
    _tb(s, "Capabilities that emerge when you orchestrate multiple LLMs as a coordinated team",
        0.6, 1.14, 12, 0.3, size=12, color=TDIM)

    caps = [
        ("Specialised Division of Labour",
         ("Each agent has a focused system prompt and narrow domain. A grain growth expert knows "
          "CdTe physics; a contamination expert knows cleanroom science. No single prompt needs "
          "to know everything — agents contribute what they know best.")),
        ("Closed-Loop Autonomous Operation",
         ("Agents observe sensor data, reason about anomalies, and issue corrective actions — all "
          "without human initiation. The loop closes faster than any operator managing "
          "50 concurrent metrics.")),
        ("Cross-Agent Verification",
         ("A second expert independently reviews the same data and challenges or confirms the "
          "primary diagnosis — mirroring peer review to reduce hallucination before "
          "action is taken.")),
        ("Human-in-the-Loop Escalation",
         ("Agents identify when physical inspection is needed, generate structured escalation "
          "reports, and route to the right human role — without replacing judgment for "
          "safety-critical decisions.")),
    ]
    cw = 6.1
    for i, (ct, cd) in enumerate(caps):
        cx = 0.6 if i % 2 == 0 else 6.9
        cy = 1.55 if i < 2 else 3.35
        _rect(s, cx, cy, cw, 1.65, fill=DCARD, line=BRBR)
        _tb(s, ct, cx+0.2, cy+0.14, cw-0.4, 0.34, size=11, color=BLUE, bold=True)
        _tb(s, cd, cx+0.2, cy+0.52, cw-0.4, 1.0,  size=9.5, color=TDIM)

    # Comparison
    half = 5.85
    _rect(s, 0.6,  5.18, half, 2.1, fill=NEG_BG,  line=NEG_BORD)
    _tb(s, "Single LLM approach", 0.78, 5.26, half-0.3, 0.28, size=10, color=NEG_HEAD, bold=True)
    _tb(s, ("X  One massive prompt for all domains\n"
            "X  Context window fills with irrelevant data\n"
            "X  No second opinion\n"
            "X  Slower — one call to answer everything\n"
            "X  Hard to explain which expertise was applied"),
        0.78, 5.58, half-0.3, 1.55, size=9, color=NEG_TEXT)

    _tb(s, "vs", 6.58, 6.04, 0.48, 0.46, size=13, color=BRBR, align=PP_ALIGN.CENTER)

    _rect(s, 7.12, 5.18, half, 2.1, fill=DCARD, line=BRBR, lw=1.5)
    _tb(s, "Multi-agent system", 7.30, 5.26, half-0.3, 0.28, size=10, color=BLUE, bold=True)
    _tb(s, ("✓  Focused prompts per specialist domain\n"
            "✓  Each agent sees only relevant context\n"
            "✓  Cross-checking by secondary expert\n"
            "✓  Parallel capability, sequential reasoning\n"
            "✓  Transparent: visible which agent said what"),
        7.30, 5.58, half-0.3, 1.55, size=9, color=TDIM)


def _slide5_industry(prs, blank) -> None:
    s = prs.slides.add_slide(blank)
    _bg(s, BG)
    _stripe(s)

    _label(s, "04  ·  INDUSTRY IMPACT", 0.6, 0.18)
    _tb(s, "Agentic AI Across Sectors", 0.6, 0.45, 12, 0.7, size=28, color=TEXT, bold=True)
    _tb(s, "The same orchestration pattern adapts to any domain where expert knowledge must act on live data",
        0.6, 1.14, 12, 0.3, size=12, color=TDIM)

    sectors = [
        ("Healthcare",          RED,    "Diagnostic support — radiology + pathology agents cross-check imaging\nICU monitoring — vital sign agents flag deterioration in real time\nDrug discovery — chemistry + toxicology agents screen candidates"),
        ("Finance",             ORANGE, "Fraud detection — transaction, behavioural & network agents triage\nRisk management — macro, credit & liquidity agents hold guardrails\nCompliance — regulatory agents monitor trades against rulebooks"),
        ("Energy & Grid",       GREEN,  "Grid stability — load, generation & storage agents balance supply\nRenewable forecasting — weather + demand agents optimise dispatch\nFault isolation — protection agents localise faults before cascade"),
        ("Aerospace & Defence", PURPLE, "Predictive maintenance — engine, avionics & structural agents\nMission planning — logistics & threat-assessment agents optimise\nSupply chain — inventory agents anticipate AOG part shortages"),
        ("Smart Manufacturing", TEAL,   "Quality control — vision + process agents detect defects live\nYield optimisation — recipe agents adjust parameters to spec\nOEE improvement — downtime, speed & quality agents coordinate"),
        ("Legal & Compliance",  AMBER,  "Contract review — clause, risk & jurisdiction agents flag terms\nRegulatory monitoring — policy agents track rule changes live\nDue diligence — financial, legal & ESG agents run in parallel"),
    ]
    sw = 3.97
    for i, (sec, col, desc) in enumerate(sectors):
        sx = 0.6 + (i % 3) * 4.27
        sy = 1.55 if i < 3 else 4.24
        _rect(s, sx, sy,        sw, 0.07, fill=col,  line=None)
        _rect(s, sx, sy + 0.07, sw, 2.45, fill=CARD, line=BORDER)
        _tb(s, sec,  sx+0.18, sy+0.17, sw-0.36, 0.32, size=11, color=col,  bold=True)
        _tb(s, desc, sx+0.18, sy+0.55, sw-0.36, 1.82, size=9,  color=TDIM)

    # Footer
    _rect(s, 0.6, 6.96, 12.0, 0.42, fill=RGBColor(0x0f,0x14,0x20), line=ORANGE, lw=1.5)
    _rect(s, 0.6, 6.96, 0.07, 0.42, fill=ORANGE, line=None)
    _tb(s, ("Common pattern: a central reasoning agent receives live data, routes to the right "
            "specialist, and surfaces an actionable conclusion — faster than any human team could convene."),
        0.82, 7.02, 11.5, 0.32, size=8.5, color=RGBColor(0xa0,0x80,0x40))


def _slide6_pv(prs, blank) -> None:
    s = prs.slides.add_slide(blank)
    _bg(s, BG)
    _stripe(s, ORANGE)

    _label(s, "05  ·  OUR DEMO", 0.6, 0.18)
    _tb2(s, [("Applying This to ", TEXT, True),
             ("Solar Panel Manufacturing", ORANGE, True)],
         0.6, 0.45, 12.5, 0.72, size=26)
    _tb(s, "Why PV manufacturing is an ideal testbed for near-closed-loop agentic control",
        0.6, 1.14, 12, 0.3, size=12, color=TDIM)

    # Challenge column
    _tb(s, "The challenge", 0.6, 1.55, 6.0, 0.3, size=11, color=ORANGE, bold=True)
    challenges = [
        ("50 sensors  ·  7 stages  ·  millisecond faults",
         ("No human operator can simultaneously track particle density, chamber pressure, "
          "grain diameter, laser deviation, and QA efficiency across a live production line.")),
        ("Cross-stage root causes",
         ("A drop in QA efficiency (Stage 7) may trace back to incomplete CdCl2 activation "
          "(Stage 3) — an expert at Stage 7 alone cannot see that.")),
        ("Cost of delayed diagnosis",
         ("Each panel that fails QA has consumed full upstream processing cost. Catching a "
          "vacuum leak at Stage 2 saves five downstream stages of wasted processing.")),
    ]
    cy = 1.9
    for ch_t, ch_d in challenges:
        _rect(s, 0.6, cy, 5.9, 1.52, fill=DK_OLIVE, line=OL_BORD)
        _tb(s, ch_t, 0.78, cy+0.1,  5.6, 0.3,  size=10, color=OL_HEAD, bold=True)
        _tb(s, ch_d, 0.78, cy+0.46, 5.6, 0.9,  size=9,  color=OL_TEXT)
        cy += 1.62

    # Solution column
    _tb(s, "The agentic solution", 6.9, 1.55, 6.0, 0.3, size=11, color=BLUE, bold=True)
    solutions = [
        ("Central Reasoning Agent (Claude Sonnet 4.6)",
         ("Receives all 50 metrics the moment a fault threshold is crossed. Identifies the "
          "anomaly, explains its significance, and selects the right expert to investigate.")),
        ("12 Specialist Expert Agents",
         ("Each covers one control loop from the research paper. They reason over the same "
          "sensor snapshot through the lens of their specific domain expertise.")),
        ("Autonomous Diagnostic Report",
         ("Generates a complete .docx fault analysis report — root cause, corrective actions, "
          "and full sensor snapshot — without any human writing a single line.")),
    ]
    sy = 1.9
    for sol_t, sol_d in solutions:
        _rect(s, 6.9, sy, 5.9, 1.52, fill=DCARD, line=BRBR)
        _tb(s, sol_t, 7.08, sy+0.1,  5.6, 0.34, size=10, color=BLUE, bold=True)
        _tb(s, sol_d, 7.08, sy+0.5,  5.6, 0.9,  size=9,  color=TDIM)
        sy += 1.62

    # CTA banner
    _rect(s, 0.6, 6.94, 12.0, 0.5, fill=DK_OLIVE, line=RGBColor(0x3a,0x5a,0x3a), lw=1.5)
    _tb2(s, [
            ("Ready to see it live?   ", RGBColor(0xf0,0xc0,0x60), True),
            ("Switch to the Live Demo tab — from sensor anomaly to downloadable report in under 60 seconds.", TDIM, False),
        ], 0.82, 7.02, 11.5, 0.38, size=9.5)


# ── Public entry point ────────────────────────────────────────────────────────

def generate_intro_ppt() -> bytes:
    """Build the Introduction slide deck and return it as raw .pptx bytes."""
    prs = Presentation()
    prs.slide_width  = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank = prs.slide_layouts[6]   # Blank layout

    _slide1_agenda(prs, blank)
    _slide2_landscape(prs, blank)
    _slide3_frameworks(prs, blank)
    _slide4_capabilities(prs, blank)
    _slide5_industry(prs, blank)
    _slide6_pv(prs, blank)

    buf = BytesIO()
    prs.save(buf)
    return buf.getvalue()
