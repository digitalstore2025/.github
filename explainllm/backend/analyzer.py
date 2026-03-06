from __future__ import annotations

from backend.models import AnalyzeResult
from engine.prompt_linter import PromptLinter


class PromptAnalyzer:
    def __init__(self) -> None:
        self.linter = PromptLinter()

    def analyze(self, prompt: str) -> AnalyzeResult:
        issues = self.linter.lint(prompt)
        findings = [issue.message for issue in issues]
        suggestions = [
            "Add 1-2 concrete examples.",
            "Define the intended audience explicitly.",
            "Specify output schema (JSON/table/bullets).",
        ]
        score = max(0, 100 - len(issues) * 20)
        return AnalyzeResult(score=score, findings=findings, suggestions=suggestions)
