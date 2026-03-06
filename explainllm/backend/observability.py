from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from backend.models import MetricRecord


class ObservabilityStore:
    def __init__(self) -> None:
        self.records: List[MetricRecord] = []

    def record(self, endpoint: str, latency_ms: float) -> None:
        self.records.append(MetricRecord(endpoint=endpoint, latency_ms=latency_ms))

    def metrics(self) -> Dict[str, float | int]:
        by_endpoint = defaultdict(list)
        for record in self.records:
            by_endpoint[record.endpoint].append(record.latency_ms)

        response: Dict[str, float | int] = {"total_requests": len(self.records)}
        for endpoint, values in by_endpoint.items():
            response[f"{endpoint}_count"] = len(values)
            response[f"{endpoint}_avg_ms"] = round(sum(values) / len(values), 2)
        return response
