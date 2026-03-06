from __future__ import annotations

from celery import shared_task

from backend.benchmark import PromptBenchmark
from backend.optimizer import PromptOptimizationEngine


@shared_task(name="workers.tasks.run_benchmark")
def run_benchmark(prompt: str):
    return PromptBenchmark().benchmark(prompt).model_dump()


@shared_task(name="workers.tasks.run_optimization")
def run_optimization(task: str):
    return PromptOptimizationEngine().optimize(task).model_dump()
