import json
import random
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

CONFIG_DIR = Path(__file__).parent.parent / "config"

with open(CONFIG_DIR / "metrics.json", encoding="utf-8") as f:
    METRICS = json.load(f)

with open(CONFIG_DIR / "fault_scenarios.json", encoding="utf-8") as f:
    FAULT_SCENARIOS = json.load(f)


@dataclass
class SensorSnapshot:
    metrics: dict[str, float]
    timestamp: str
    fault_active: bool
    fault_scenario: Optional[dict] = None
    elapsed_seconds: float = 0.0


def _normal_reading(meta: dict) -> float:
    lo, hi = meta["normal_min"], meta["normal_max"]
    noise = (hi - lo) * 0.05
    val = random.uniform(lo, hi) + random.uniform(-noise, noise)
    return round(max(lo * 0.9, min(hi * 1.1, val)), 4)


class PVSimulator:
    """
    Generates live PV manufacturing sensor readings.
    Auto-injects a random fault scenario after fault_delay seconds.
    """

    def __init__(self, fault_delay_range: tuple[int, int] = (18, 25)):
        self._fault_delay = random.randint(*fault_delay_range)
        self._start_time: Optional[float] = None
        self._fault_scenario: Optional[dict] = None
        self._fault_triggered = False

    def start(self):
        self._start_time = time.time()
        self._fault_scenario = random.choice(FAULT_SCENARIOS)
        self._fault_triggered = False

    def reset(self):
        self._start_time = None
        self._fault_scenario = None
        self._fault_triggered = False

    @property
    def fault_triggered(self) -> bool:
        return self._fault_triggered

    @property
    def active_scenario(self) -> Optional[dict]:
        return self._fault_scenario if self._fault_triggered else None

    def get_snapshot(self) -> SensorSnapshot:
        if self._start_time is None:
            self.start()

        elapsed = time.time() - self._start_time

        # Build normal readings for all 50 metrics
        readings: dict[str, float] = {}
        for step_key, meta in METRICS.items():
            readings[step_key] = _normal_reading(meta)

        # Inject fault after delay
        fault_active = False
        if elapsed >= self._fault_delay and self._fault_scenario:
            self._fault_triggered = True
            fault_active = True
            for step_key, injected_val in self._fault_scenario["injected_faults"].items():
                readings[step_key] = injected_val

        return SensorSnapshot(
            metrics=readings,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            fault_active=fault_active,
            fault_scenario=self._fault_scenario if fault_active else None,
            elapsed_seconds=elapsed,
        )


def format_snapshot_for_agent(snapshot: SensorSnapshot) -> str:
    """Format a sensor snapshot as a structured string for the LLM agent."""
    lines = [
        f"=== PV Manufacturing Sensor Snapshot ===",
        f"Timestamp: {snapshot.timestamp}",
        f"Fault Active: {'YES' if snapshot.fault_active else 'NO'}",
        "",
        "--- Sensor Readings by Stage ---",
    ]

    stage_names = {
        1: "Surface Preparation",
        2: "PVD Deposition",
        3: "CdCl₂ Activation",
        4: "Grain Growth",
        5: "Back Contact",
        6: "Laser Scribing",
        7: "QA Testing",
    }

    by_stage: dict[int, list] = {s: [] for s in range(1, 8)}
    for step_key, val in snapshot.metrics.items():
        meta = METRICS[step_key]
        stage = meta["stage"]
        status = _check_status(step_key, val)
        by_stage[stage].append(
            f"  [{step_key}] {meta['name']}: {val} {meta['unit']} | "
            f"Normal: {meta['normal_min']}–{meta['normal_max']} | Status: {status}"
        )

    for stage_num, name in stage_names.items():
        lines.append(f"\nStage {stage_num}: {name}")
        lines.extend(by_stage[stage_num])

    return "\n".join(lines)


def _check_status(step_key: str, value: float) -> str:
    meta = METRICS[step_key]
    direction = meta["fault_direction"]
    threshold = meta["fault_threshold"]
    if direction == "above" and value > threshold:
        return "FAULT"
    if direction == "below" and value < threshold:
        return "FAULT"
    if direction == "above" and value > meta["normal_max"]:
        return "WARNING"
    if direction == "below" and value < meta["normal_min"]:
        return "WARNING"
    return "OK"


def get_stage_metrics(snapshot: SensorSnapshot, stage: int) -> dict:
    """Return metrics and their status for a given stage number."""
    result = {}
    for step_key, val in snapshot.metrics.items():
        meta = METRICS[step_key]
        if meta["stage"] == stage:
            result[step_key] = {
                "name": meta["name"],
                "value": val,
                "unit": meta["unit"],
                "status": _check_status(step_key, val),
                "plain_english": meta["plain_english"],
            }
    return result


def get_faulty_steps(snapshot: SensorSnapshot) -> list[dict]:
    """Return list of metrics currently in FAULT state."""
    faults = []
    for step_key, val in snapshot.metrics.items():
        if _check_status(step_key, val) == "FAULT":
            meta = METRICS[step_key]
            faults.append({
                "step": step_key,
                "name": meta["name"],
                "value": val,
                "unit": meta["unit"],
                "threshold": meta["fault_threshold"],
                "direction": meta["fault_direction"],
                "stage": meta["stage"],
                "plain_english": meta["plain_english"],
                "error_type": meta["error_type"],
            })
    return faults
