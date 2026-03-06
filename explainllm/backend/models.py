from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1)


class TaskRequest(BaseModel):
    task: str = Field(..., min_length=1)


class AnalyzeResult(BaseModel):
    score: int
    findings: List[str]
    suggestions: List[str]


class FixResult(BaseModel):
    original: str
    improved: str


class GenerateResult(BaseModel):
    task: str
    variants: List[str]


class BenchmarkResult(BaseModel):
    model: str
    latency_ms: float
    token_usage: int
    response_length: int
    output: str


class BenchmarkSummary(BaseModel):
    prompt: str
    results: List[BenchmarkResult]


class OptimizeResult(BaseModel):
    original_prompt: str
    best_prompt: str
    leaderboard: List[Dict[str, float]]


class ScanResult(BaseModel):
    path: str
    line: int
    snippet: str


class MetricRecord(BaseModel):
    endpoint: str
    latency_ms: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class LibraryPrompt(BaseModel):
    id: int
    name: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SavePromptRequest(BaseModel):
    name: str
    content: str


class ErrorResponse(BaseModel):
    detail: str
    hint: Optional[str] = None
