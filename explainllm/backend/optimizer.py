from __future__ import annotations

from backend.benchmark import PromptBenchmark
from backend.generator import PromptGenerator
from backend.models import OptimizeResult


class PromptOptimizationEngine:
    def __init__(self) -> None:
        self.generator = PromptGenerator()
        self.benchmark = PromptBenchmark()

    def optimize(self, task_or_prompt: str) -> OptimizeResult:
        generated = self.generator.generate(task_or_prompt)
        candidates = [task_or_prompt, *generated.variants]
        leaderboard = []

        for candidate in candidates:
            summary = self.benchmark.benchmark(candidate)
            avg_latency = sum(item.latency_ms for item in summary.results) / len(summary.results)
            avg_tokens = sum(item.token_usage for item in summary.results) / len(summary.results)
            score = max(0.0, 1000 - (avg_latency * 2 + avg_tokens))
            leaderboard.append({"prompt": candidate, "score": round(score, 2)})

        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        best_prompt = leaderboard[0]["prompt"]
        return OptimizeResult(
            original_prompt=task_or_prompt,
            best_prompt=best_prompt,
            leaderboard=leaderboard,
        )
