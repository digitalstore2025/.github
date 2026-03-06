from __future__ import annotations

from backend.models import GenerateResult


class PromptGenerator:
    def generate(self, task: str) -> GenerateResult:
        base = task.strip()
        variants = [
            f"You are an expert assistant. Task: {base}. Return bullet points with rationale.",
            f"For a junior engineer, explain how to complete: {base}. Include pitfalls and examples.",
            f"Generate a JSON plan for: {base}. Keys: goals, steps, risks, success_criteria.",
        ]
        return GenerateResult(task=task, variants=variants)
