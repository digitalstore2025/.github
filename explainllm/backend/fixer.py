from __future__ import annotations

from backend.models import FixResult
from engine.prompt_optimizer import PromptOptimizer


class PromptFixer:
    def __init__(self) -> None:
        self.optimizer = PromptOptimizer()

    def fix(self, prompt: str) -> FixResult:
        improved = self.optimizer.improve(prompt)
        return FixResult(original=prompt, improved=improved)
