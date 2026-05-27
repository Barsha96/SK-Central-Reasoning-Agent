"""Generate a PowerPoint presentation matching the Architecture Forum Introduction slides."""
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
GREEN     = RGBColor(0x50, 0xd4, 0xa0)
PURPLE    = RGBColor(0xc0, 0x80, 0xe0)
TEAL      = RGBColor(0x50, 0xd4, 0xa0)
RED       = RGBColor(0xe0, 0x55, 0x55)
AMBER     = RGBColor(0xe8, 0x70, 0x70)
TEXT      = RGBColor(0xe8, 0xf0, 0xf8)
TDIM      = RGBColor(0x7a, 0x9a, 0xb8)
MUTED     = RGBColor(0x4a, 0x6a, 0x9c)
DARK_CARD = RGBColor(0x1a, 0x1f, 0x0a)
OLIVE_BRD = RGBColor(0x3a, 0x3a, 0x1a)
OLIVE_TXT = RGBColor(0xa0, 0xa0, 0x60)
OLIVE_HDR = RGBColor(0xe0, 0xe0, 0x80)
DK_BLUE   = RGBColor(0x0f, 0x1a, 0x2a)
DK_PURP   = RGBColor(0x1a, 0x0f, 0x1f)
PURP_BRD  = RGBColor(0x7a, 0x3a, 0x9a)
SK_BRD    = RGBColor(0x2a, 0x7a, 0x5a)
SK_TEXT   = RGBColor(0x50, 0xd4, 0xa0)
DK_OLIV   = RGBColor(0x1a, 0x1a, 0x0a)
GRN_BRD   = RGBColor(0x2a, 0x50, 0x20)
GRN_TEXT  = RGBColor(0x90, 0xd4, 0x90)
EXPERT_BG = RGBColor(0x0f, 0x1f, 0x35)


# ── Low-level helpers ─────────────────────────────────────────────────────────

def _bg(slide, color: RGBColor) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def _rect(slide, x, y, w, h, fill=CARD, line=BORDER, lw: float = 0.75):
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
    _rect(slide, 0, 0, 13.333, 0.055, fill=color, line=None)


# ── Slide 1: Title & Agenda ───────────────────────────────────────────────────

def _slide1_title(prs, blank) -> None:
    s = prs.slides.add_slide(blank)
    _bg(s, BG)
    _stripe(s, BLUE)

    _tb(s, "Architecture Forum  ·  May 2026",
        0.6, 0.18, 12, 0.28, size=9, color=MUTED)
    _tb2(s, [
            ("Near-Closed Loop Control with ", TEXT, True),
            ("Centralized Reasoning Agent", BLUE, True),
        ], 0.6, 0.5, 12.5, 0.8, size=28)
    _tb(s, "A Multi-Agent AI System for Solar PV Manufacturing  ·  Semantic Kernel + Claude Sonnet 4.6",
        0.6, 1.26, 12, 0.32, size=12, color=TDIM)

    agenda = [
        ("01", "Project Overview",         "Problem statement & motivation"),
        ("02", "System Architecture",      "Components, layers & data flow"),
        ("03", "Expert Agent Catalog",     "12 specialist domain agents"),
        ("04", "Expert Selection & Routing", "How the triage agent decides"),
        ("05", "Reasoning Chain",          "Triage → Expert → Cross-check"),
        ("06", "Live Demo",                "7-stage PV line fault detection"),
    ]
    xs = [0.6, 7.0,  0.6, 7.0,  0.6, 7.0]
    ys = [1.75, 1.75, 3.2, 3.2,  4.65, 4.65]
    ws = [6.1, 6.1,  6.1, 6.1,  6.1, 6.1]
    cols = [BLUE, BLUE, BLUE, ORANGE, ORANGE, GREEN]

    for i, (num, title, desc) in enumerate(agenda):
        x, y, w = xs[i], ys[i], ws[i]
        _rect(s, x, y, w, 1.28, fill=CARD, line=BORDER)
        _tb(s, num,   x+0.18, y+0.1,  2,     0.26, size=9,  color=cols[i], bold=True)
        _tb(s, title, x+0.18, y+0.38, w-0.4, 0.32, size=11, color=TEXT,   bold=True)
        _tb(s, desc,  x+0.18, y+0.74, w-0.4, 0.42, size=9,  color=TDIM)

    _tb(s, "Barsha Upadhyaya  ·  First Solar",
        0.6, 7.12, 12, 0.26, size=8, color=RGBColor(0x2a, 0x4a, 0x6a))


# ── Slide 2: Project Overview ─────────────────────────────────────────────────

def _slide2_overview(prs, blank) -> None:
    s = prs.slides.add_slide(blank)
    _bg(s, BG)
    _stripe(s, RED)

    _label(s, "01  ·  PROJECT OVERVIEW", 0.6, 0.18)
    _tb(s, "Why We Built This", 0.6, 0.45, 12, 0.65, size=26, color=TEXT, bold=True)
    _tb(s, "Every minute of undiagnosed fault on a 225-module/hr line is measured in dollars",
        0.6, 1.1, 12, 0.28, size=11, color=TDIM)

    # Problems column
    problems = [
        ("Faults are invisible until it is too late",
         "50 sensors across 7 stages produce simultaneous readings no operator can fully track. A micro-deviation in Stage 2 chamber pressure can cascade unseen through to Stage 7 QA failure."),
        ("MTTR is the margin killer",
         "The gap between 45-min human diagnosis and 5-min AI diagnosis is ~$21,800 per fault event and ~$2.2M annually at typical fault rates."),
        ("No single expert sees the full picture",
         "Cross-stage root causes require simultaneous expertise across multiple process domains — that is not a human-scale problem."),
    ]
    py = 1.52
    for pt, pd in problems:
        _rect(s, 0.6, py, 5.8, 1.45, fill=RGBColor(0x1a, 0x0f, 0x0f),
              line=RED, lw=1.5)
        _rect(s, 0.6, py, 0.07, 1.45, fill=RED, line=None)
        _tb(s, pt, 0.82, py+0.1,  5.4, 0.3,  size=10, color=AMBER, bold=True)
        _tb(s, pd, 0.82, py+0.45, 5.4, 0.88, size=9,  color=RGBColor(0x9a, 0x70, 0x70))
        py += 1.55

    # MTTR table
    _tb(s, "Downtime Cost by MTTR", 6.8, 1.52, 5.8, 0.28, size=9,
        color=TDIM, bold=True)

    # Stats box
    _rect(s, 6.8, 1.84, 5.8, 0.68, fill=DCARD, line=BRBR)
    _tb(s, "Cycle time:", 6.98, 1.9, 2.5, 0.28, size=9, color=TDIM)
    _tb(s, "16 sec/module  →  225 modules/hr", 9.0, 1.9, 3.4, 0.28, size=9, color=BLUE, bold=True)
    _tb(s, "Module value:", 6.98, 2.2, 2.5, 0.28, size=9, color=TDIM)
    _tb(s, "~$145  (525W thin-film)", 9.0, 2.2, 3.4, 0.28, size=9, color=BLUE, bold=True)

    # Table
    rows = [
        ("MTTR", "Modules Lost", "Revenue Lost", MUTED),
        ("1 hour", "225", "~$32,600", RED),
        ("45 min", "169", "~$24,500", RED),
        ("30 min", "113", "~$16,400", RED),
        ("5 min (AI)", "19",  "~$2,800",  GREEN),
    ]
    ty = 2.65
    for mttr, mods, rev, rc in rows:
        bg   = RGBColor(0x0a, 0x1a, 0x0a) if mttr == "5 min (AI)" else RGBColor(0x0a, 0x10, 0x20)
        _rect(s, 6.8, ty, 5.8, 0.42, fill=bg, line=BORDER, lw=0.5)
        _tb(s, mttr, 6.98, ty+0.08, 1.6, 0.28, size=10, color=rc, bold=(mttr != "MTTR"))
        _tb(s, mods, 9.1,  ty+0.08, 1.4, 0.28, size=10, color=rc, bold=(mttr != "MTTR"),
            align=PP_ALIGN.CENTER)
        _tb(s, rev,  10.8, ty+0.08, 1.6, 0.28, size=10, color=rc, bold=(mttr != "MTTR"),
            align=PP_ALIGN.RIGHT)
        ty += 0.43

    # Goal callout
    _rect(s, 6.8, 4.95, 5.8, 0.85, fill=DCARD, line=BLUE, lw=1.5)
    _rect(s, 6.8, 4.95, 0.07, 0.85, fill=BLUE, line=None)
    _tb(s, "Our goal", 7.02, 5.02, 5.4, 0.26, size=10, color=BLUE, bold=True)
    _tb(s, ("Compress detection-to-corrective-action from 45 minutes to under 5 minutes "
            "using a centralized AI reasoning agent — without replacing human judgment on "
            "safety-critical decisions."),
        7.02, 5.32, 5.4, 0.42, size=9, color=TDIM)


# ── Slide 3: System Architecture ─────────────────────────────────────────────

def _slide3_architecture(prs, blank) -> None:
    s = prs.slides.add_slide(blank)
    _bg(s, BG)
    _stripe(s, BLUE)

    _label(s, "02  ·  SYSTEM ARCHITECTURE", 0.6, 0.18)
    _tb(s, "How the System is Designed", 0.6, 0.45, 12, 0.65, size=26, color=TEXT, bold=True)
    _tb(s, "Four layers — UI, orchestration, reasoning, and domain expertise — with a live data feed from the simulator",
        0.6, 1.1, 12, 0.28, size=11, color=TDIM)

    # Layer 1: UI
    _rect(s, 0.6, 1.5, 8.4, 0.88, fill=RGBColor(0x0f, 0x1f, 0x35), line=BRBR, lw=1.5)
    _tb(s, "PRESENTATION LAYER", 0.78, 1.56, 8.0, 0.22, size=8, color=BLUE, bold=True)
    _tb(s, "Streamlit UI Dashboard", 0.78, 1.8, 5.0, 0.3, size=12, color=TEXT, bold=True)
    _tb(s, "Live conveyor visualization  ·  Agent response stream  ·  Report download",
        0.78, 2.12, 7.8, 0.22, size=9, color=TDIM)

    # Arrow 1
    _tb(s, "↕", 4.7, 2.42, 0.4, 0.3, size=14, color=BRBR, align=PP_ALIGN.CENTER)

    # Layer 2: SK
    _rect(s, 0.6, 2.76, 8.4, 0.88, fill=RGBColor(0x0f, 0x1f, 0x0f), line=SK_BRD, lw=1.5)
    _tb(s, "ORCHESTRATION LAYER", 0.78, 2.82, 8.0, 0.22, size=8, color=SK_TEXT, bold=True)
    _tb(s, "Semantic Kernel (v1.5+)", 0.78, 3.06, 5.0, 0.3, size=12, color=TEXT, bold=True)
    _tb(s, "AnthropicChatCompletion connector  ·  Plugin registry  ·  Streaming API",
        0.78, 3.38, 7.8, 0.22, size=9, color=TDIM)

    # Arrow 2
    _tb(s, "↕", 4.7, 3.68, 0.4, 0.3, size=14, color=SK_BRD, align=PP_ALIGN.CENTER)

    # Layer 3: Triage Agent
    _rect(s, 0.6, 4.02, 8.4, 0.92, fill=DK_PURP, line=PURP_BRD, lw=1.5)
    _tb(s, "REASONING LAYER", 0.78, 4.08, 8.0, 0.22, size=8, color=PURPLE, bold=True)
    _tb(s, "Central Reasoning Agent", 0.78, 4.32, 5.0, 0.3, size=12, color=TEXT, bold=True)
    _tb(s, "Claude Sonnet 4.6  ·  Fault assessment  ·  Expert routing  ·  Initial hypothesis",
        0.78, 4.64, 7.8, 0.22, size=9, color=TDIM)

    # Arrow 3
    _tb(s, "↕", 4.7, 4.98, 0.4, 0.3, size=14, color=PURP_BRD, align=PP_ALIGN.CENTER)

    # Layer 4: Expert pool
    _rect(s, 0.6, 5.32, 8.4, 0.92, fill=DK_OLIV, line=ORANGE, lw=1.5)
    _tb(s, "EXPERT AGENT POOL  ·  12 SPECIALISTS", 0.78, 5.38, 8.0, 0.22, size=8, color=ORANGE, bold=True)
    experts = "Defect Reduction  ·  Efficiency  ·  Grain Optimization  ·  Uniformity  ·  Contamination  ·  Temp Stabilization"
    experts2 = "Pressure Calibration  ·  Activation Completion  ·  Maintenance (HITL)  ·  Throughput  ·  Cross-Process  ·  Quality Control"
    _tb(s, experts,  0.78, 5.62, 7.8, 0.24, size=8.5, color=RGBColor(0xd4, 0xa0, 0x60))
    _tb(s, experts2, 0.78, 5.88, 7.8, 0.24, size=8.5, color=RGBColor(0x90, 0xd4, 0x90))

    # Tech stack panel
    _rect(s, 9.2, 1.5, 3.8, 5.75, fill=CARD, line=BORDER)
    _tb(s, "TECHNOLOGY STACK", 9.38, 1.58, 3.4, 0.22, size=8, color=BLUE, bold=True)

    stack = [
        ("Language",      "Python 3.11+",         TEXT),
        ("UI",            "Streamlit 1.35+",       TEXT),
        ("Orchestration", "Semantic Kernel 1.5+",  SK_TEXT),
        ("LLM",           "Claude Sonnet 4.6",     PURPLE),
        ("Expert agents", "12 specialists",        ORANGE),
        ("Report",        "python-docx",           TEXT),
    ]
    sy = 1.86
    for lbl, val, vc in stack:
        _tb(s, lbl, 9.38, sy, 1.5, 0.28, size=9, color=TDIM)
        _tb(s, val, 10.9, sy, 2.0, 0.28, size=9, color=vc, bold=True)
        sy += 0.4

    _tb(s, "DATA FLOW", 9.38, 4.36, 3.4, 0.22, size=8, color=BLUE, bold=True)
    flow = (
        "① Simulator generates 50-metric snapshot\n"
        "② Fault threshold crossed → UI triggers agent\n"
        "③ SK passes snapshot to triage agent\n"
        "④ Triage selects 1–2 expert agents\n"
        "⑤ Experts stream analysis back to UI\n"
        "⑥ Report generated & offered for download"
    )
    _tb(s, flow, 9.38, 4.62, 3.4, 1.8, size=8.5, color=TDIM)

    _rect(s, 9.2, 6.54, 3.8, 0.72, fill=DK_OLIV, line=ORANGE, lw=1.5)
    _rect(s, 9.2, 6.54, 0.07, 0.72, fill=ORANGE, line=None)
    _tb(s, "Near-closed loop:", 9.42, 6.6, 3.4, 0.24, size=9, color=ORANGE, bold=True)
    _tb(s, "AI diagnoses and recommends. Human approves before line intervention.",
        9.42, 6.86, 3.4, 0.32, size=8.5, color=OLIVE_TXT)


# ── Slide 4: Expert Agent Catalog ─────────────────────────────────────────────

def _slide4_experts(prs, blank) -> None:
    s = prs.slides.add_slide(blank)
    _bg(s, BG)
    _stripe(s, BLUE)

    _label(s, "03  ·  EXPERT AGENT CATALOG", 0.6, 0.18)
    _tb(s, "12 Specialist Domain Agents", 0.6, 0.45, 12, 0.65, size=26, color=TEXT, bold=True)
    _tb(s, "Each agent carries a focused system prompt covering exactly one control loop from the PV research literature",
        0.6, 1.1, 12, 0.28, size=11, color=TDIM)

    agents_blue = [
        ("Defect Reduction Expert",
         "Tracks defect propagation across stages. Pinhole, delamination, and patterning defects from upstream."),
        ("Efficiency Expert",
         "Diagnoses low conversion efficiency. Analyzes Voc, Jsc, and fill-factor deviations."),
        ("Grain Optimization Expert",
         "Handles CdTe grain growth failures. Correlates grain diameter with deposition temperature and pressure."),
        ("Uniformity Correction Expert",
         "Handles deposition non-uniformity. Recommends scan-speed and source adjustments."),
        ("Contamination Control Expert",
         "Handles particle and chemical contamination. Assesses cleanroom metrics and particle counts."),
        ("Temperature Stabilization Expert",
         "Handles thermal process deviations across deposition and annealing stages."),
    ]
    agents_green = [
        ("Pressure Calibration Expert",
         "Handles vacuum and gas pressure anomalies. Distinguishes sensor drift from real chamber leaks."),
        ("Activation Completion Expert",
         "Handles CdCl₂ activation problems (Stage 3). Correlates incomplete activation with efficiency loss."),
        ("Maintenance Expert (HITL)",
         "Escalates equipment and human-factor issues. Generates structured handoff reports for operators."),
        ("Throughput & Yield Expert",
         "Handles production rate and yield loss. Identifies bottleneck stages."),
        ("Cross-Process Optimization Expert",
         "Handles multi-stage systemic faults spanning more than one process zone."),
        ("Quality Control Expert",
         "Runs the end-to-end quality audit. Acts as the final gate confirming or rejecting a module."),
    ]

    ew = 4.1
    for i, (name, desc) in enumerate(agents_blue):
        col = i % 3
        row = i // 3
        x = 0.6 + col * 4.37
        y = 1.52 + row * 1.65
        _rect(s, x, y, ew, 1.5, fill=EXPERT_BG, line=BRBR)
        _tb(s, name, x+0.14, y+0.1,  ew-0.28, 0.3,  size=10, color=BLUE,  bold=True)
        _tb(s, desc, x+0.14, y+0.46, ew-0.28, 0.88, size=9,  color=TDIM)

    for i, (name, desc) in enumerate(agents_green):
        col = i % 3
        row = i // 3
        x = 0.6 + col * 4.37
        y = 4.82 + row * 1.65
        _rect(s, x, y, ew, 1.5, fill=RGBColor(0x1a, 0x2a, 0x0a), line=GRN_BRD)
        _tb(s, name, x+0.14, y+0.1,  ew-0.28, 0.3,  size=10, color=GRN_TEXT, bold=True)
        _tb(s, desc, x+0.14, y+0.46, ew-0.28, 0.88, size=9,  color=RGBColor(0x4a, 0x6a, 0x4a))

    # Footer note
    _rect(s, 0.6, 6.5, 12.0, 0.72, fill=DK_BLUE, line=BLUE, lw=1.5)
    _rect(s, 0.6, 6.5, 0.07, 0.72, fill=BLUE, line=None)
    _tb(s, "Design principle:", 0.82, 6.57, 2.0, 0.28, size=9, color=BLUE, bold=True)
    _tb(s, ("Each agent's system prompt is scoped to its domain only — no agent sees instructions for others. "
            "This keeps context focused, prevents cross-contamination of reasoning, and makes individual agent "
            "behavior explainable and auditable."),
        2.6, 6.57, 9.8, 0.58, size=9, color=TDIM)


# ── Slide 5: Expert Selection & Routing ──────────────────────────────────────

def _slide5_routing(prs, blank) -> None:
    s = prs.slides.add_slide(blank)
    _bg(s, BG)
    _stripe(s, ORANGE)

    _label(s, "04  ·  EXPERT SELECTION & ROUTING", 0.6, 0.18)
    _tb(s, "How the Triage Agent Decides", 0.6, 0.45, 12, 0.65, size=26, color=TEXT, bold=True)
    _tb(s, "The Central Reasoning Agent reasons over fault data and explains its expert selection — not a black box",
        0.6, 1.1, 12, 0.28, size=11, color=TDIM)

    steps = [
        ("1", "Receive full sensor snapshot",
         "All 50 metrics from the 7-stage line are passed simultaneously. Anomalous readings are pre-flagged with direction (above/below) and deviation magnitude."),
        ("2", "Perform fault assessment",
         "The agent explains what each anomalous reading means physically — not just numbers, but the process implication of each deviation."),
        ("3", "Select primary + secondary expert",
         "From the 12 available experts, the triage agent picks the most relevant primary and a cross-check secondary — explaining why each was chosen."),
        ("4", "State initial hypothesis",
         "Before expert agents run, the triage agent commits to a brief root-cause hypothesis, visible to the operator and revisable by the experts."),
    ]
    sy = 1.52
    for num, title, desc in steps:
        _rect(s, 0.6, sy, 6.0, 1.35, fill=DARK_CARD, line=OLIVE_BRD)
        _rect(s, 0.6, sy, 0.38, 1.35,
              fill=RGBColor(0x3a, 0x3a, 0x0a), line=None)
        _tb(s, num,   0.6,  sy+0.48, 0.38, 0.4, size=13, color=ORANGE,
            bold=True, align=PP_ALIGN.CENTER)
        _tb(s, title, 1.14, sy+0.1,  5.3,  0.3,  size=11, color=OLIVE_HDR, bold=True)
        _tb(s, desc,  1.14, sy+0.48, 5.3,  0.76, size=9,  color=OLIVE_TXT)
        sy += 1.45

    # Right column
    _rect(s, 6.9, 1.52, 6.0, 1.45, fill=DCARD, line=BRBR)
    _tb(s, "Scenario-Based Routing", 7.08, 1.6, 5.6, 0.28, size=10, color=BLUE, bold=True)
    _tb(s, ("Each fault scenario carries a primary_expert and secondary_expert key. "
            "The triage agent's reasoning surfaces the 'why' behind that routing — making it "
            "explainable, not a black box."),
        7.08, 1.94, 5.6, 0.9, size=9, color=TDIM)

    _rect(s, 6.9, 3.08, 6.0, 1.45, fill=DCARD, line=BRBR)
    _tb(s, "Triage Agent Response Structure", 7.08, 3.16, 5.6, 0.28, size=10, color=BLUE, bold=True)
    sections = "## Fault Assessment\n## Why This Expert?\n## Initial Hypothesis"
    _tb(s, sections, 7.08, 3.5, 5.6, 0.9, size=10, color=PURPLE, bold=True)

    _rect(s, 6.9, 4.64, 6.0, 1.1, fill=DCARD, line=BRBR)
    _tb(s, "Why Two Experts?", 7.08, 4.72, 5.6, 0.28, size=10, color=BLUE, bold=True)
    _tb(s, ("The primary expert performs the deep-dive. The secondary independently reviews the same "
            "snapshot and confirms or challenges the finding — mirroring peer review to reduce "
            "hallucination risk before any corrective action is recommended."),
        7.08, 5.06, 5.6, 0.62, size=9, color=TDIM)

    _rect(s, 6.9, 5.86, 6.0, 1.42, fill=DARK_CARD, line=OLIVE_BRD)
    _tb(s, "Example routing (fault scenario config):", 7.08, 5.94, 5.6, 0.28, size=9, color=OLIVE_TXT)
    code = "primary_expert:   pressure_calibration\nsecondary_expert: contamination_control"
    _tb(s, code, 7.08, 6.26, 5.6, 0.9, size=9, color=ORANGE, bold=True)


# ── Slide 6: Reasoning Chain ──────────────────────────────────────────────────

def _slide6_reasoning(prs, blank) -> None:
    s = prs.slides.add_slide(blank)
    _bg(s, BG)
    _stripe(s, ORANGE)

    _label(s, "05  ·  REASONING CHAIN", 0.6, 0.18)
    _tb(s, "From Sensor Anomaly to Diagnostic Report", 0.6, 0.45, 12, 0.65, size=24, color=TEXT, bold=True)
    _tb(s, "Three sequential reasoning phases, each with a distinct system prompt — streamed live to the operator",
        0.6, 1.1, 12, 0.28, size=11, color=TDIM)

    phases = [
        (DK_PURP,  PURP_BRD, PURPLE,  "Phase 1",
         "Central Triage Agent",   "Claude Sonnet 4.6  ·  ~600 tokens",
         "- Receives 50-metric snapshot\n- Identifies anomalous readings\n- Explains physical meaning\n- Selects primary + secondary expert\n- States initial hypothesis\n- Streams response to UI"),
        (DCARD,    BRBR,     BLUE,    "Phase 2",
         "Primary Expert Agent",   "Claude Sonnet 4.6  ·  ~1200 tokens",
         "- Receives same sensor snapshot\n- Applies domain-specific prompt\n- Focused root-cause analysis\n- Quantifies deviation severity\n- Prescribes corrective actions\n- Streams response to UI"),
        (DARK_CARD, OLIVE_BRD, GREEN, "Phase 3",
         "Cross-Check Expert",     "Claude Sonnet 4.6  ·  ~1200 tokens",
         "- Independent analysis of same data\n- Applies different domain lens\n- Confirms or challenges Phase 2\n- Surfaces any missed signals\n- Adds complementary perspective\n- Streams response to UI"),
    ]

    pw = 4.0
    for i, (bg, bc, ac, phase, title, sub, desc) in enumerate(phases):
        x = 0.4 + i * 4.38
        _rect(s, x, 1.5, pw, 4.72, fill=bg, line=bc, lw=1.5)
        _tb(s, phase, x+0.16, 1.6,  pw-0.32, 0.26, size=9,  color=ac, bold=True)
        _tb(s, title, x+0.16, 1.9,  pw-0.32, 0.36, size=12, color=TEXT, bold=True)
        _tb(s, sub,   x+0.16, 2.3,  pw-0.32, 0.26, size=8,  color=TDIM)
        _tb(s, desc,  x+0.16, 2.62, pw-0.32, 3.44, size=9,  color=TDIM)
        if i < 2:
            _tb(s, "→", x+pw+0.06, 3.68, 0.28, 0.4, size=16, color=MUTED, align=PP_ALIGN.CENTER)

    # Output banner
    _rect(s, 0.4, 6.38, 12.53, 0.9, fill=CARD, line=BORDER)
    _tb(s, "📄", 0.6, 6.5, 0.5, 0.5, size=20, color=TEXT)
    _tb(s, "Output: Autonomous Diagnostic Report (.docx)",
        1.22, 6.46, 6.0, 0.3, size=11, color=TEXT, bold=True)
    _tb(s, ("Fault summary  ·  Triage assessment  ·  Primary expert analysis  ·  "
            "Cross-check findings  ·  Full sensor snapshot  ·  Corrective actions"),
        1.22, 6.8, 7.0, 0.4, size=9, color=TDIM)
    checks = "✓ Root cause     ✓ Actions listed     ✓ Sensor snapshot     ✓ Cross-check done"
    _tb(s, checks, 8.4, 6.62, 4.4, 0.58, size=9, color=BLUE, bold=True)


# ── Slide 7: Live Demo ────────────────────────────────────────────────────────

def _slide7_demo(prs, blank) -> None:
    s = prs.slides.add_slide(blank)
    _bg(s, BG)
    _stripe(s, GREEN)

    _label(s, "06  ·  LIVE DEMO", 0.6, 0.18)
    _tb2(s, [("See It in Action: ", TEXT, True),
             ("Solar PV Manufacturing Line", ORANGE, True)],
         0.6, 0.45, 12.5, 0.7, size=24)
    _tb(s, "From sensor anomaly to downloadable diagnostic report — in under 60 seconds",
        0.6, 1.14, 12, 0.28, size=12, color=TDIM)

    steps = [
        ("\U0001f3ed", "Conveyor runs normally (~20 sec)", "All 7 stages green, all 50 metrics within range."),
        ("⚠️",  "Random fault auto-injects",       "Chosen from 10 pre-defined scenarios across the 7-stage line."),
        ("\U0001f9e0", "Triage agent activates",           "Streams fault assessment, expert selection, and hypothesis live."),
        ("\U0001f468‍\U0001f52c", "Expert agents respond", "Primary analysis, then cross-check — each streamed as generated."),
        ("\U0001f4c4", "Report generated",                 "A .docx diagnostic report is automatically offered for download."),
    ]
    sy = 1.56
    for icon, title, desc in steps:
        _rect(s, 0.6, sy, 7.8, 1.0, fill=DCARD, line=BORDER)
        _tb(s, icon,  0.78, sy+0.2, 0.5,  0.55, size=18, color=TEXT)
        _tb(s, title, 1.42, sy+0.12, 6.8, 0.3,  size=11, color=BLUE, bold=True)
        _tb(s, desc,  1.42, sy+0.48, 6.8, 0.42, size=9,  color=TDIM)
        sy += 1.1

    # Stats grid
    stats = [("7", "Stages"), ("50", "Sensors"), ("12", "Experts"), ("<60s", "To report")]
    sx = 8.9
    sw = 2.1
    for i, (val, lbl) in enumerate(stats):
        sy2 = 1.56 + i * 1.4
        _rect(s, sx, sy2, sw, 1.22, fill=CARD, line=BORDER)
        vc = BLUE if i < 2 else (ORANGE if i == 2 else GREEN)
        _tb(s, val, sx+0.1, sy2+0.14, sw-0.2, 0.54, size=24, color=vc, bold=True, align=PP_ALIGN.CENTER)
        _tb(s, lbl, sx+0.1, sy2+0.74, sw-0.2, 0.36, size=9,  color=TDIM,          align=PP_ALIGN.CENTER)

    # CTA
    _rect(s, 0.6, 7.02, 12.0, 0.38, fill=DK_OLIV, line=RGBColor(0x3a, 0x5a, 0x3a), lw=1.5)
    _tb2(s, [
            ("Ready to see it live?   ", RGBColor(0xf0, 0xc0, 0x60), True),
            ("Switch to the Live Demo tab — from sensor anomaly to downloadable report in under 60 seconds.", TDIM, False),
        ], 0.82, 7.08, 11.5, 0.28, size=9.5)


# ── Public entry point ────────────────────────────────────────────────────────

def generate_intro_ppt() -> bytes:
    """Build the Architecture Forum slide deck and return raw .pptx bytes."""
    prs = Presentation()
    prs.slide_width  = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank = prs.slide_layouts[6]

    _slide1_title(prs, blank)
    _slide3_architecture(prs, blank)
    _slide4_experts(prs, blank)
    _slide5_routing(prs, blank)
    _slide6_reasoning(prs, blank)
    _slide7_demo(prs, blank)

    buf = BytesIO()
    prs.save(buf)
    return buf.getvalue()
