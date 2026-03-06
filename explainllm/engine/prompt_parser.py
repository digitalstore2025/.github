from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class PromptParts:
    objective: str
    constraints: List[str]
    output_hints: List[str]


class PromptParser:
    def parse(self, prompt: str) -> PromptParts:
        lines = [line.strip() for line in prompt.splitlines() if line.strip()]
        objective = lines[0] if lines else prompt.strip()
        constraints = [line for line in lines if any(k in line.lower() for k in ("must", "should", "do not"))]
        output_hints = [line for line in lines if any(k in line.lower() for k in ("output", "format", "json", "table"))]
        return PromptParts(objective=objective, constraints=constraints, output_hints=output_hints)
