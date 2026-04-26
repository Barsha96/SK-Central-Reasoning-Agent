"""
Central Triage Agent — the orchestrator that receives sensor data,
identifies what kind of fault occurred, routes to the right expert(s),
and streams the entire thought process for the UI.
"""
from __future__ import annotations

import os
from typing import Generator
import anthropic
from dotenv import load_dotenv

from data.simulator import SensorSnapshot, format_snapshot_for_agent, get_faulty_steps
from agents.experts.defect_reduction import DefectReductionExpert
from agents.experts.efficiency import EfficiencyExpert
from agents.experts.grain_optimization import GrainOptimizationExpert
from agents.experts.uniformity_correction import UniformityCorrectionExpert
from agents.experts.contamination_control import ContaminationControlExpert
from agents.experts.temperature_stabilization import TemperatureStabilizationExpert
from agents.experts.pressure_calibration import PressureCalibrationExpert
from agents.experts.activation_completion import ActivationCompletionExpert
from agents.experts.maintenance import MaintenanceExpert
from agents.experts.throughput import ThroughputExpert
from agents.experts.cross_process import CrossProcessExpert
from agents.experts.quality_control import QualityControlExpert

load_dotenv()

TRIAGE_SYSTEM_PROMPT = """You are the Central Reasoning Agent for a near-closed-loop PV solar panel manufacturing system.
You are the first responder when a fault is detected anywhere on the production line.

Your role:
1. Receive the sensor snapshot from the manufacturing line
2. Quickly assess WHICH metrics are out of range and WHICH stage is affected
3. Determine the most likely fault category and explain your reasoning clearly
4. State which specialist expert(s) you are routing this to, and explain WHY that expert is the right choice
5. Provide a brief initial hypothesis about the root cause

You have access to 12 specialist experts:
  • Defect Reduction Expert       — tracks defect propagation across stages
  • Efficiency Expert             — diagnoses low conversion efficiency
  • Grain Optimization Expert     — handles grain growth failures
  • Uniformity Correction Expert  — handles deposition non-uniformity
  • Contamination Control Expert  — handles particle and chemical contamination
  • Temperature Stabilization Expert — handles thermal process deviations
  • Pressure Calibration Expert   — handles vacuum and sensor calibration issues
  • Activation Completion Expert  — handles CdCl₂ activation problems
  • Maintenance Expert (Human-in-Loop) — escalates equipment and human-factor issues
  • Throughput & Yield Expert     — handles production rate and yield loss
  • Cross-Process Optimization Expert — handles multi-stage systemic faults
  • End-to-End Quality Control Expert — runs comprehensive quality audit

Your communication style:
- Think out loud — the audience watching this demo can see your reasoning
- Use plain language: explain what each anomalous reading means physically
- Be decisive about which expert(s) to call and why
- Format your response with clear sections:
  ## Fault Assessment
  ## Why This Expert?
  ## Initial Hypothesis

Keep your triage response under 300 words. Be clear and confident."""

EXPERT_MAP = {
    "defect_reduction":          DefectReductionExpert,
    "efficiency":                EfficiencyExpert,
    "grain_optimization":        GrainOptimizationExpert,
    "uniformity_correction":     UniformityCorrectionExpert,
    "contamination_control":     ContaminationControlExpert,
    "temperature_stabilization": TemperatureStabilizationExpert,
    "pressure_calibration":      PressureCalibrationExpert,
    "activation_completion":     ActivationCompletionExpert,
    "maintenance":               MaintenanceExpert,
    "throughput":                ThroughputExpert,
    "cross_process":             CrossProcessExpert,
    "quality_control":           QualityControlExpert,
}


class TriageAgent:
    def __init__(self):
        self._client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self._model = os.getenv("MODEL_ID", "claude-sonnet-4-6")

    def analyze_stream(
        self, snapshot: SensorSnapshot, scenario: dict
    ) -> Generator[tuple[str, str], None, None]:
        """
        Stream the full analysis as (speaker, text_chunk) tuples.
        speaker is one of: 'triage', 'expert_primary', 'expert_secondary', 'system'
        """
        snapshot_str = format_snapshot_for_agent(snapshot)
        faulty_steps = get_faulty_steps(snapshot)

        # Phase 1: Triage assessment
        yield ("system", f"\n**Fault detected at Stage {scenario['stage']}: {scenario['stage_name']}**\n\n")
        yield ("system", f"*Initiating centralized reasoning agent...*\n\n")

        fault_summary = self._format_fault_summary(faulty_steps)
        triage_user_msg = (
            f"A fault has been detected on the PV manufacturing line.\n\n"
            f"ANOMALOUS METRICS:\n{fault_summary}\n\n"
            f"FULL SENSOR SNAPSHOT:\n{snapshot_str}\n\n"
            f"Please perform your triage assessment."
        )

        with self._client.messages.stream(
            model=self._model,
            max_tokens=600,
            system=TRIAGE_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": triage_user_msg}],
        ) as stream:
            for text in stream.text_stream:
                yield ("triage", text)

        # Phase 2: Primary expert
        primary_key = scenario.get("primary_expert", "quality_control")
        primary_expert = EXPERT_MAP[primary_key]()

        yield ("system", f"\n\n---\n\n**Routing to: {primary_expert.display_name}**\n\n")

        for chunk in primary_expert.analyze_stream(snapshot_str, faulty_steps):
            yield ("expert_primary", chunk)

        # Phase 3: Secondary expert (if different from primary)
        secondary_key = scenario.get("secondary_expert")
        if secondary_key and secondary_key != primary_key:
            secondary_expert = EXPERT_MAP[secondary_key]()
            yield ("system", f"\n\n---\n\n**Cross-checking with: {secondary_expert.display_name}**\n\n")

            for chunk in secondary_expert.analyze_stream(snapshot_str, faulty_steps):
                yield ("expert_secondary", chunk)

        yield ("system", "\n\n---\n\n*Analysis complete. Generating report...*")

    def run_full_analysis(self, snapshot: SensorSnapshot, scenario: dict) -> dict:
        """Run complete analysis and return structured result for report generation."""
        snapshot_str = format_snapshot_for_agent(snapshot)
        faulty_steps = get_faulty_steps(snapshot)

        triage_text = ""
        expert_primary_text = ""
        expert_secondary_text = ""

        primary_key = scenario.get("primary_expert", "quality_control")
        primary_expert = EXPERT_MAP[primary_key]()

        secondary_key = scenario.get("secondary_expert")
        secondary_expert = EXPERT_MAP[secondary_key]() if secondary_key and secondary_key != primary_key else None

        fault_summary = self._format_fault_summary(faulty_steps)
        triage_user_msg = (
            f"A fault has been detected on the PV manufacturing line.\n\n"
            f"ANOMALOUS METRICS:\n{fault_summary}\n\n"
            f"FULL SENSOR SNAPSHOT:\n{snapshot_str}"
        )

        triage_response = self._client.messages.create(
            model=self._model,
            max_tokens=600,
            system=TRIAGE_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": triage_user_msg}],
        )
        triage_text = triage_response.content[0].text

        expert_primary_text = primary_expert.analyze_full(snapshot_str, faulty_steps)

        if secondary_expert:
            expert_secondary_text = secondary_expert.analyze_full(snapshot_str, faulty_steps)

        return {
            "triage": triage_text,
            "expert_primary_name": primary_expert.display_name,
            "expert_primary_text": expert_primary_text,
            "expert_secondary_name": secondary_expert.display_name if secondary_expert else None,
            "expert_secondary_text": expert_secondary_text,
            "faulty_steps": faulty_steps,
            "scenario": scenario,
            "snapshot": snapshot,
        }

    @staticmethod
    def _format_fault_summary(faulty_steps: list[dict]) -> str:
        if not faulty_steps:
            return "No metrics in FAULT state."
        lines = []
        for f in faulty_steps:
            direction = "above" if f["direction"] == "above" else "below"
            lines.append(
                f"  [{f['step']}] {f['name']}: {f['value']} {f['unit']} "
                f"(threshold {direction} {f['threshold']}) at Stage {f['stage']}"
            )
        return "\n".join(lines)
