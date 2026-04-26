# Near-Closed-Loop PV Manufacturing Control System

A live demo application built for the **IEEE PES Boston Chapter** that replicates the research paper:
> *"Near-Closed-Loop Control in PV Manufacturing with a Centralized Reasoning Agent — LLM and Semantic Kernel Based Implementation"*
> — Barsha Upadhyaya, University of Toledo

The system demonstrates that a single centralized LLM reasoning agent, orchestrated through **Microsoft Semantic Kernel** and powered by **Claude Sonnet 4.6**, can autonomously detect, diagnose, and report faults across a simulated 7-stage photovoltaic (solar panel) manufacturing line — monitoring 50 sensors in real time, routing to 12 specialist expert agents, and generating a complete fault report without any human intervention.

---

## What the App Does

1. **Simulates** a live PV production line — 50 sensor metrics across 7 manufacturing stages, with realistic noise and auto-injected fault scenarios after ~20 seconds of normal operation.
2. **Detects** anomalies the moment a sensor reading crosses its threshold.
3. **Reasons** — a centralized triage agent (Claude Sonnet 4.6 via Semantic Kernel) analyses the full sensor snapshot, selects the right specialist expert, and streams its chain-of-thought reasoning to the UI in real time.
4. **Reports** — a downloadable `.docx` fault analysis report (root cause, corrective actions, full sensor table) is generated automatically at the end of each run.

---

## Pages

| Tab | Description |
|-----|-------------|
| **Introduction** | 6-slide IEEE presentation — agenda, AI landscape, frameworks, capabilities, industry impact, PV demo. Includes a `.pptx` download. |
| **PV Stages** | Plain-English explainer for all 7 manufacturing stages with key physics and monitored parameters. |
| **Live Demo** | Animated conveyor belt + real-time agent reasoning panel. The main demo. |
| **Synthetic Data** | Live table of all 50 sensor readings, colour-coded by status. |
| **How SK Works** | Annotated Semantic Kernel code, sequence diagram, and architecture explanations. |
| **Agents Config** | Full system prompts and function signatures for all 13 agents (1 triage + 12 experts). |

---

## How to Build Locally

### Prerequisites

- Python 3.11 or 3.12 (3.13 works; 3.10 minimum)
- An [Anthropic API key](https://console.anthropic.com/)
- Git (to clone) or the project folder already on disk

### 1. Clone / navigate to the project

```bash
cd "c:\Documents\Semantic Kernel"
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (copy the template below):

```env
ANTHROPIC_API_KEY=sk-ant-...your-key-here...
MODEL_ID=claude-sonnet-4-6
```

`MODEL_ID` is optional — it defaults to `claude-sonnet-4-6` if omitted.

### 5. Run the app

```bash
streamlit run app.py
```

Streamlit will open `http://localhost:8501` in your browser automatically.

### 6. Verify everything works

| Check | Expected |
|-------|----------|
| App loads | 6-tab navigation visible in sidebar |
| Live Demo | Animated conveyor runs; green metric cards visible |
| After ~20 s | One station turns red with a fault indicator |
| Agent panel | Streams triage + expert reasoning in real time |
| Download Report | `.docx` file opens with root cause and sensor table |
| Introduction tab | 6 slides navigable; `.pptx` download button present |

---

## File Structure

```
c:\Documents\Semantic Kernel\
│
├── app.py                          # Streamlit entry point — multi-page router
├── home.py                         # Live Demo page (conveyor + agent panel)
├── requirements.txt                # Python dependencies
├── .env                            # API key and model ID (not committed)
│
├── pages/                          # Streamlit pages (rendered by app.py navigation)
│   ├── introduction.py             # 6-slide IEEE presentation with .pptx download
│   ├── pv_stages.py                # Educational explainer for 7 PV stages
│   ├── synthetic_data.py           # Live sensor data table (all 50 metrics)
│   ├── sk_explainer.py             # How Semantic Kernel works — diagrams + code
│   └── agents_config.py            # Agent system prompts and function docs
│
├── config/                         # Static configuration data
│   ├── metrics.json                # 50 sensor metrics: name, unit, thresholds, stage, description
│   └── fault_scenarios.json        # 10 named fault scenarios with injected sensor values
│
├── data/
│   └── simulator.py                # Generates live readings; auto-injects a fault after ~20 s
│
├── agents/                         # Semantic Kernel agent layer
│   ├── kernel_setup.py             # Builds SK Kernel with AnthropicChatCompletion connector
│   ├── triage_agent.py             # Central triage ChatCompletionAgent — routes to experts
│   └── experts/                    # 12 SK Plugin classes (one per control loop)
│       ├── base_expert.py          # Shared base class for all expert plugins
│       ├── defect_reduction.py     # Control loop: 4→5→10→17→21→23→4
│       ├── efficiency.py           # Control loop: 33→4 (triggers if η < 15 %)
│       ├── grain_optimization.py   # Control loop: 17→18→20→17
│       ├── uniformity_correction.py# Control loop: 11→12→13→11
│       ├── contamination_control.py# Control loop: 2→25→35→2
│       ├── temperature_stabilization.py  # Control loop: 6→18→40→6
│       ├── pressure_calibration.py # Control loop: 7→30→44→7
│       ├── activation_completion.py# Control loop: 21→22→23→21
│       ├── maintenance.py          # Control loop: 46→36→45→46 (human-in-loop gate)
│       ├── throughput.py           # Control loop: 47→32→34→47
│       ├── cross_process.py        # Control loop: 1→3→7→14→19→31→38→42→1
│       └── quality_control.py      # Control loop: 2→5→9→15→20→26→29→33→41→49→2
│
├── ui/                             # Streamlit UI components
│   ├── conveyor_panel.py           # HTML/JS animated conveyor belt (7 stations)
│   └── agent_panel.py              # Streaming agent thought-process panel
│
├── utils/                          # Export utilities
│   ├── report_exporter.py          # Builds .docx fault analysis report (python-docx)
│   ├── ppt_exporter.py             # Generates Introduction slides .pptx (python-pptx)
│   └── agentic_ppt.py              # Standalone generator: Agentic_Systems_Overview.pptx
│
└── Agentic_Systems_Overview.pptx   # Pre-generated presentation on agentic AI systems
```

### Key design decisions

- **Streamlit `st.navigation()`** (v1.36+) — each page is a separate `.py` file; no `pages/` auto-discovery needed, giving explicit ordering and icons.
- **`st.components.v1.html()`** — the conveyor animation runs in its own iframe so the JavaScript animation loop is never interrupted by Streamlit reruns.
- **Semantic Kernel `ChatCompletionAgent`** — all 12 expert plugins are registered on a single Kernel; the triage agent selects and invokes them as tool calls, keeping orchestration logic out of application code.
- **`st.write_stream()`** — consumes the async generator from SK's `invoke_stream()`, rendering the agent's live reasoning token-by-token in the UI.

---

## Technology Stack

| Component | Library / Service |
|-----------|-------------------|
| UI framework | Streamlit ≥ 1.35 |
| Agent orchestration | Semantic Kernel ≥ 1.5 |
| LLM | Claude Sonnet 4.6 (Anthropic) |
| LLM connector | `anthropic` SDK ≥ 0.30 |
| Report export | `python-docx` ≥ 1.1 |
| Slide export | `python-pptx` ≥ 0.6.23 |
| Charts | Plotly ≥ 5.18 |
| Config | `python-dotenv` |

---

## Research Context

This application is a Python implementation of the control architecture described in the paper. The 12 control loops, 50 monitored metrics, 7 manufacturing stages, and 10 fault scenarios are all drawn directly from the original research. The goal of the live demo is to show that the closed-loop reasoning described on paper is achievable in a running system — not as a simulation of outputs, but as a real LLM agent making real decisions over synthetic sensor data.
