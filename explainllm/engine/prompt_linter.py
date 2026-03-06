from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class LintIssue:
    rule: str
    message: str


class PromptLinter:
    """Basic deterministic linter for prompt quality signals."""

    def lint(self, prompt: str) -> List[LintIssue]:
        prompt_lower = prompt.lower()
        issues: List[LintIssue] = []

        if len(prompt.split()) < 12:
            issues.append(LintIssue("vague", "Prompt is very short and may be vague."))

        if "example" not in prompt_lower:
            issues.append(LintIssue("missing_examples", "Prompt does not include explicit examples."))

        if not any(token in prompt_lower for token in ("audience", "for ", "as a ")):
            issues.append(LintIssue("missing_audience", "Prompt does not specify the audience."))

        if not any(token in prompt_lower for token in ("format", "json", "bullet", "table", "output")):
            issues.append(
                LintIssue(
                    "missing_output_structure",
                    "Prompt does not define a strict output structure.",
                )
            )

        return issues
