from __future__ import annotations

import time

from fastapi import FastAPI, Query

from backend.analyzer import PromptAnalyzer
from backend.benchmark import PromptBenchmark
from backend.fixer import PromptFixer
from backend.generator import PromptGenerator
from backend.library import PromptLibrary
from backend.models import PromptRequest, SavePromptRequest, TaskRequest
from backend.optimizer import PromptOptimizationEngine
from backend.observability import ObservabilityStore
from backend.scanner import PromptScanner

app = FastAPI(title="ExplainLLM", version="0.1.0")

analyzer = PromptAnalyzer()
fixer = PromptFixer()
generator = PromptGenerator()
benchmarker = PromptBenchmark()
optimizer = PromptOptimizationEngine()
scanner = PromptScanner()
observability = ObservabilityStore()
library = PromptLibrary()


def timed(endpoint: str):
    def wrapper(fn):
        def inner(*args, **kwargs):
            start = time.perf_counter()
            result = fn(*args, **kwargs)
            observability.record(endpoint, (time.perf_counter() - start) * 1000)
            return result

        return inner

    return wrapper


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze")
@timed("analyze")
def analyze(req: PromptRequest):
    return analyzer.analyze(req.prompt)


@app.post("/fix")
@timed("fix")
def fix(req: PromptRequest):
    return fixer.fix(req.prompt)


@app.post("/generate")
@timed("generate")
def generate(req: TaskRequest):
    return generator.generate(req.task)


@app.post("/benchmark")
@timed("benchmark")
def benchmark(req: PromptRequest):
    return benchmarker.benchmark(req.prompt)


@app.post("/optimize")
@timed("optimize")
def optimize(req: TaskRequest):
    return optimizer.optimize(req.task)


@app.get("/scan")
@timed("scan")
def scan(path: str = Query(default=".")):
    return scanner.scan(path)


@app.get("/metrics")
def metrics():
    return observability.metrics()


@app.post("/library")
def save_prompt(req: SavePromptRequest):
    return library.add(name=req.name, content=req.content)


@app.get("/library")
def list_prompts():
    return library.list()
