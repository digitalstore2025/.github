from __future__ import annotations

import random
import time
from typing import Dict


class PromptSimulator:
    """Simulates model responses and metrics without requiring external LLM APIs."""

    def run(self, model: str, prompt: str) -> Dict[str, float | int | str]:
        started = time.perf_counter()
        synthetic_delay = random.uniform(0.03, 0.2)
        time.sleep(synthetic_delay)
        latency_ms = (time.perf_counter() - started) * 1000

        token_usage = max(12, int(len(prompt.split()) * random.uniform(1.1, 1.8)))
        response = f"[{model}] Simulated response for: {prompt[:90]}"
        return {
            "model": model,
            "latency_ms": round(latency_ms, 2),
            "token_usage": token_usage,
            "response_length": len(response),
            "output": response,
        }
