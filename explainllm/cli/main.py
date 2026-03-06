from __future__ import annotations

import json

import requests
import typer

app = typer.Typer(help="ExplainLLM CLI")
API_URL = "http://localhost:8000"


def post(path: str, payload: dict):
    response = requests.post(f"{API_URL}{path}", json=payload, timeout=30)
    response.raise_for_status()
    typer.echo(json.dumps(response.json(), indent=2))


@app.command()
def analyze(prompt: str):
    post("/analyze", {"prompt": prompt})


@app.command()
def fix(prompt: str):
    post("/fix", {"prompt": prompt})


@app.command()
def generate(task: str):
    post("/generate", {"task": task})


@app.command()
def benchmark(prompt: str):
    post("/benchmark", {"prompt": prompt})


@app.command()
def optimize(task: str):
    post("/optimize", {"task": task})


@app.command()
def scan(path: str = "."):
    response = requests.get(f"{API_URL}/scan", params={"path": path}, timeout=30)
    response.raise_for_status()
    typer.echo(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    app()
