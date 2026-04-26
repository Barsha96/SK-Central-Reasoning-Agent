"""
Animated conveyor belt panel — two-row layout.
Row 1: Stages 1–4  |  Row 2: Stages 5–7
Each row has its own belt with moving solar panel shapes.
"""
from __future__ import annotations
import json
import streamlit.components.v1 as components

STAGE_INFO = [
    {"id": 1, "short": "Surface Prep",      "icon": "🧹", "desc": "Clean & texture the silicon wafer"},
    {"id": 2, "short": "PVD Deposition",    "icon": "⚗️",  "desc": "Deposit semiconductor layers in vacuum"},
    {"id": 3, "short": "CdCl₂ Activation", "icon": "🔥",  "desc": "Heat treatment to improve the junction"},
    {"id": 4, "short": "Grain Growth",      "icon": "🔬",  "desc": "Recrystallize grains for better conductivity"},
    {"id": 5, "short": "Back Contact",      "icon": "🔩",  "desc": "Deposit metal back contact layer"},
    {"id": 6, "short": "Laser Scribing",    "icon": "⚡",  "desc": "Laser-cut cells to interconnect them"},
    {"id": 7, "short": "QA Testing",        "icon": "✅",  "desc": "Final electrical test for efficiency & power"},
]

ROW1 = [s for s in STAGE_INFO if s["id"] <= 4]
ROW2 = [s for s in STAGE_INFO if s["id"] >  4]


def render_conveyor(
    stage_statuses: dict[int, str],
    stage_metrics:  dict[int, list],
    fault_stage:    int | None = None,
    running:        bool = True,
    height:         int  = 580,
):
    statuses_json   = json.dumps(stage_statuses)
    metrics_json    = json.dumps(stage_metrics)
    fault_stage_js  = str(fault_stage) if fault_stage else "null"
    running_js      = "true" if running else "false"
    row1_json       = json.dumps(ROW1)
    row2_json       = json.dumps(ROW2)

    html = f"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  background: #0f1117;
  font-family: 'Segoe UI', sans-serif;
  color: #e0e0e0;
  overflow: hidden;
  padding: 10px 8px 6px;
}}

/* ── title ── */
.title-bar {{
  text-align: center;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #7eb3d4;
  text-transform: uppercase;
  margin-bottom: 8px;
}}

/* ── each conveyor row ── */
.conveyor-row {{
  background: #13161f;
  border: 1px solid #252836;
  border-radius: 8px;
  padding: 10px 8px 0;
  margin-bottom: 8px;
  position: relative;
  overflow: hidden;
}}

/* ── stage boxes row ── */
.stages-row {{
  display: flex;
  gap: 8px;
  justify-content: space-around;
  margin-bottom: 6px;
}}

/* ── individual stage box ── */
.stage-box {{
  flex: 1;
  background: #1e2130;
  border: 2px solid #2d3348;
  border-radius: 8px;
  padding: 10px 8px;
  text-align: center;
  transition: all 0.3s ease;
  min-height: 130px;
  position: relative;
}}
.stage-box.ok      {{ border-color: #2d6a4f; }}
.stage-box.warning {{ border-color: #d4a017; background: #1e1c10; }}
.stage-box.fault   {{
  border-color: #c0392b; background: #1e1010;
  animation: pulse-red 0.8s ease-in-out infinite;
}}
@keyframes pulse-red {{
  0%,100% {{ box-shadow: 0 0 0px #c0392b; border-color: #c0392b; }}
  50%     {{ box-shadow: 0 0 14px #ff4444; border-color: #ff6666; }}
}}

.fault-badge {{
  position: absolute; top: -9px; right: -6px;
  background: #c0392b; color: #fff;
  font-size: 9px; font-weight: 800;
  padding: 1px 5px; border-radius: 3px;
  display: none;
}}
.stage-box.fault .fault-badge {{ display: block; }}

.stage-icon {{ font-size: 26px; line-height: 1; }}
.stage-name {{
  font-size: 13px; font-weight: 700;
  color: #c8d8e8; margin-top: 5px;
  line-height: 1.25;
}}
.status-dot {{
  width: 9px; height: 9px; border-radius: 50%;
  margin: 5px auto 4px;
}}
.dot-ok      {{ background: #27ae60; box-shadow: 0 0 5px #27ae60; }}
.dot-warning {{ background: #f39c12; box-shadow: 0 0 5px #f39c12; }}
.dot-fault   {{
  background: #e74c3c; box-shadow: 0 0 7px #e74c3c;
  animation: dot-blink 0.6s ease-in-out infinite;
}}
@keyframes dot-blink {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:0.2; }} }}

.metric-pills {{ margin-top: 4px; }}
.mpill {{
  font-size: 10px; color: #8899aa;
  margin: 2px 0; white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis;
}}
.mpill.fault-val {{ color: #ff6666; font-weight: 700; }}

/* ── belt ── */
.belt-wrap {{
  position: relative;
  height: 36px;
  margin: 0 -8px;
}}
.belt {{
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 22px;
  background: repeating-linear-gradient(
    90deg,
    #2d3142 0px,  #2d3142 28px,
    #232638 28px, #232638 40px
  );
  border-top: 2px solid #3a3f55;
  border-bottom: 2px solid #3a3f55;
  animation: belt-move 1.2s linear infinite;
}}
.belt.paused {{ animation: none; }}
@keyframes belt-move {{
  from {{ background-position: 0 0; }}
  to   {{ background-position: 40px 0; }}
}}

/* ── solar panels on belt ── */
.panels-layer {{
  position: absolute;
  bottom: 4px; left: 0; right: 0;
  height: 32px;
  overflow: hidden;
}}
.solar-panel {{
  position: absolute;
  width: 48px; height: 26px;
  background: linear-gradient(135deg, #1a3a5c 25%, #1e4d7a 50%, #1a3a5c 75%);
  border: 1.5px solid #2a5a8a;
  border-radius: 3px;
  top: 3px;
  animation: slide-panel 7s linear infinite;
}}
.solar-panel::after {{
  content: '';
  position: absolute; inset: 3px;
  background:
    repeating-linear-gradient(0deg,   transparent 0, transparent 5px, rgba(100,160,220,.15) 5px, rgba(100,160,220,.15) 6px),
    repeating-linear-gradient(90deg,  transparent 0, transparent 10px, rgba(100,160,220,.15) 10px, rgba(100,160,220,.15) 11px);
  border-radius: 1px;
}}
.solar-panel.panel-fault {{
  background: linear-gradient(135deg, #4a1010 25%, #6a1a1a 50%, #4a1010 75%);
  border-color: #c0392b;
}}
@keyframes slide-panel {{
  from {{ left: -60px; }}
  to   {{ left: 110%; }}
}}

/* ── fault banner ── */
.fault-banner {{
  display: none;
  position: absolute; bottom: 40px;
  left: 50%; transform: translateX(-50%);
  background: #c0392b; color: #fff;
  font-size: 11px; font-weight: 800;
  padding: 3px 14px; border-radius: 4px;
  letter-spacing: 1px; white-space: nowrap; z-index: 10;
}}
.fault-banner.visible {{
  display: block;
  animation: banner-pulse 1s ease-in-out infinite alternate;
}}
@keyframes banner-pulse {{ from {{ opacity:.7; }} to {{ opacity:1; }} }}

/* ── summary metric cards ── */
.metrics-row {{
  display: flex; gap: 4px; justify-content: space-around;
}}
.metric-card {{
  flex: 1; background: #1a1d27;
  border: 1px solid #2a2d3a;
  border-radius: 5px; padding: 5px 4px; text-align: center;
}}
.metric-card.fault-card {{ border-color: #c0392b; background: #1e1010; }}
.mc-stage {{ font-size: 8px; color: #556; text-transform: uppercase; letter-spacing: 1px; }}
.mc-name  {{ font-size: 9px; color: #8899aa; margin-top: 1px; }}
.mc-val   {{ font-size: 12px; font-weight: 700; color: #a0d4ff; margin-top: 1px; }}
.mc-val.fault-val {{ color: #ff6666; }}
</style>
</head>
<body>

<div class="title-bar">☀️ &nbsp;Solar Panel Manufacturing Line — Live Monitor</div>

<!-- ROW 1 -->
<div class="conveyor-row" id="row1">
  <div class="stages-row" id="stagesRow1"></div>
  <div class="belt-wrap">
    <div class="belt {'paused' if not running else ''}" id="belt1"></div>
    <div class="panels-layer" id="panelsLayer1"></div>
  </div>
  <div class="fault-banner" id="faultBanner1">⚠ FAULT DETECTED</div>
</div>

<!-- ROW 2 -->
<div class="conveyor-row" id="row2">
  <div class="stages-row" id="stagesRow2"></div>
  <div class="belt-wrap">
    <div class="belt {'paused' if not running else ''}" id="belt2"></div>
    <div class="panels-layer" id="panelsLayer2"></div>
  </div>
  <div class="fault-banner" id="faultBanner2">⚠ FAULT DETECTED</div>
</div>

<!-- summary cards -->
<div class="metrics-row" id="metricsRow"></div>

<script>
const row1Data   = {row1_json};
const row2Data   = {row2_json};
const statuses   = {statuses_json};
const metrics    = {metrics_json};
const faultStage = {fault_stage_js};
const isRunning  = {running_js};

function statusClass(id) {{
  return (statuses[id] || 'ok').toLowerCase();
}}

function buildStageBox(s) {{
  const st    = statusClass(s.id);
  const mList = metrics[s.id] || [];
  const pills = mList.slice(0, 4).map(m => {{
    const cls = m.status === 'FAULT' ? 'mpill fault-val' : 'mpill';
    const val = typeof m.value === 'number'
      ? (Number.isInteger(m.value) ? m.value : m.value.toFixed(2))
      : m.value;
    return `<div class="${{cls}}">${{m.name}}: ${{val}} ${{m.unit || ''}}</div>`;
  }}).join('');

  const box = document.createElement('div');
  box.className = `stage-box ${{st}}`;
  box.id = `stage-${{s.id}}`;
  box.innerHTML = `
    <span class="fault-badge">FAULT</span>
    <div class="stage-icon">${{s.icon}}</div>
    <div class="stage-name">${{s.short}}</div>
    <div class="status-dot dot-${{st}}"></div>
    <div class="metric-pills">${{pills}}</div>
  `;
  return box;
}}

// Populate rows
const sr1 = document.getElementById('stagesRow1');
const sr2 = document.getElementById('stagesRow2');
row1Data.forEach(s => sr1.appendChild(buildStageBox(s)));
row2Data.forEach(s => sr2.appendChild(buildStageBox(s)));

// Fault banners
const row1Ids = row1Data.map(s => s.id);
const row2Ids = row2Data.map(s => s.id);
if (faultStage !== null) {{
  if (row1Ids.includes(faultStage))
    document.getElementById('faultBanner1').classList.add('visible');
  if (row2Ids.includes(faultStage))
    document.getElementById('faultBanner2').classList.add('visible');
}}

// Add moving panels
function addPanels(layerId, stagesInRow) {{
  if (!isRunning) return;
  const layer = document.getElementById(layerId);
  const n = 5;
  for (let i = 0; i < n; i++) {{
    const panel = document.createElement('div');
    const isFaulty = faultStage !== null && stagesInRow.includes(faultStage) && i === 2;
    panel.className = 'solar-panel' + (isFaulty ? ' panel-fault' : '');
    panel.style.animationDelay = -(i * (7 / n)) + 's';
    layer.appendChild(panel);
  }}
}}
addPanels('panelsLayer1', row1Ids);
addPanels('panelsLayer2', row2Ids);

// Summary metric cards
const metricsRow = document.getElementById('metricsRow');
[...row1Data, ...row2Data].forEach(s => {{
  const mList   = metrics[s.id] || [];
  const hasFault = statusClass(s.id) === 'fault';
  const topM    = mList.find(m => m.status === 'FAULT') || mList[0];
  if (!topM) return;
  const val = typeof topM.value === 'number'
    ? (Number.isInteger(topM.value) ? topM.value : topM.value.toFixed(2))
    : topM.value;
  const card = document.createElement('div');
  card.className = 'metric-card' + (hasFault ? ' fault-card' : '');
  card.innerHTML = `
    <div class="mc-stage">Stage ${{s.id}}</div>
    <div class="mc-name">${{topM.name}}</div>
    <div class="mc-val ${{hasFault ? 'fault-val' : ''}}">${{val}} ${{topM.unit || ''}}</div>
  `;
  metricsRow.appendChild(card);
}});
</script>
</body></html>
"""
    components.html(html, height=height, scrolling=False)


def build_stage_statuses(snapshot) -> dict[int, str]:
    from data.simulator import get_stage_metrics
    stage_statuses: dict[int, str] = {}
    for stage_id in range(1, 8):
        stage_m = get_stage_metrics(snapshot, stage_id)
        if any(v["status"] == "FAULT" for v in stage_m.values()):
            stage_statuses[stage_id] = "FAULT"
        elif any(v["status"] == "WARNING" for v in stage_m.values()):
            stage_statuses[stage_id] = "WARNING"
        else:
            stage_statuses[stage_id] = "OK"
    return stage_statuses


def build_stage_metrics_for_ui(snapshot) -> dict[int, list]:
    from data.simulator import get_stage_metrics
    result: dict[int, list] = {}
    for stage_id in range(1, 8):
        stage_m = get_stage_metrics(snapshot, stage_id)
        result[stage_id] = [
            {"name": v["name"], "value": v["value"], "unit": v["unit"], "status": v["status"]}
            for v in stage_m.values()
        ]
    return result
