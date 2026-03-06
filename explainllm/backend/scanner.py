from __future__ import annotations

from pathlib import Path
from typing import List

from backend.models import ScanResult


PROMPT_MARKERS = ("prompt", "system:", "user:", "assistant:", "instruction")


class PromptScanner:
    def scan(self, repo_path: str) -> List[ScanResult]:
        results: List[ScanResult] = []
        root = Path(repo_path)
        for file in root.rglob("*"):
            if not file.is_file() or file.suffix.lower() not in {".py", ".ts", ".tsx", ".js", ".md", ".txt"}:
                continue
            try:
                for i, line in enumerate(file.read_text(errors="ignore").splitlines(), start=1):
                    if any(marker in line.lower() for marker in PROMPT_MARKERS):
                        results.append(ScanResult(path=str(file), line=i, snippet=line.strip()[:200]))
            except OSError:
                continue
        return results[:200]
