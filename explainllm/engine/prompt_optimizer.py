from __future__ import annotations

from typing import List


class PromptOptimizer:
    def improve(self, prompt: str) -> str:
        sections: List[str] = [
            "Role: You are a senior domain expert.",
            f"Task: {prompt.strip()}",
            "Audience: Intermediate software developer.",
            "Constraints: Be specific, avoid ambiguity, provide edge cases.",
            "Output format: Return a concise markdown response with bullet points.",
            "Example: Input='Build API', Output='1) requirements 2) endpoints 3) validation'.",
        ]
        return "\n".join(sections)
