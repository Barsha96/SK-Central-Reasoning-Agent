"""Base class for all expert agents. Each expert streams its analysis directly via the Anthropic SDK."""
from __future__ import annotations

import os
from typing import Generator
import anthropic
from dotenv import load_dotenv

load_dotenv()


class BaseExpert:
    display_name: str = "Expert"
    loop_steps: str = ""
    system_prompt: str = ""

    def __init__(self):
        self._client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self._model = os.getenv("MODEL_ID", "claude-sonnet-4-6")

    def analyze_stream(self, sensor_snapshot_str: str, faulty_steps: list[dict]) -> Generator[str, None, None]:
        """Stream expert analysis as text chunks."""
        fault_summary = self._format_faults(faulty_steps)

        user_message = (
            f"You are being consulted about the following PV manufacturing fault.\n\n"
            f"FAULTY METRICS DETECTED:\n{fault_summary}\n\n"
            f"FULL SENSOR SNAPSHOT:\n{sensor_snapshot_str}\n\n"
            f"Please perform your specialist analysis following your assigned control loop: {self.loop_steps}"
        )

        with self._client.messages.stream(
            model=self._model,
            max_tokens=1200,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            for text in stream.text_stream:
                yield text

    def analyze_full(self, sensor_snapshot_str: str, faulty_steps: list[dict]) -> str:
        """Return complete analysis as a single string (used for report generation)."""
        return "".join(self.analyze_stream(sensor_snapshot_str, faulty_steps))

    @staticmethod
    def _format_faults(faulty_steps: list[dict]) -> str:
        if not faulty_steps:
            return "No metrics currently in FAULT state."
        lines = []
        for f in faulty_steps:
            direction = "above" if f["direction"] == "above" else "below"
            lines.append(
                f"  • [{f['step']}] {f['name']}: {f['value']} {f['unit']} "
                f"(threshold {direction} {f['threshold']}) — {f['error_type']}"
            )
        return "\n".join(lines)
