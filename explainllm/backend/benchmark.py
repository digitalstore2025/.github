from __future__ import annotations

from typing import Iterable, List

from backend.models import BenchmarkResult, BenchmarkSummary
from engine.prompt_simulator import PromptSimulator


DEFAULT_MODELS = ("gpt-4o-mini", "claude-3-haiku", "llama-3.1-8b")


class PromptBenchmark:
    def __init__(self) -> None:
        self.simulator = PromptSimulator()

    def benchmark(self, prompt: str, models: Iterable[str] = DEFAULT_MODELS) -> BenchmarkSummary:
        results: List[BenchmarkResult] = []
        for model in models:
            metric = self.simulator.run(model=model, prompt=prompt)
            results.append(BenchmarkResult(**metric))
        return BenchmarkSummary(prompt=prompt, results=results)
