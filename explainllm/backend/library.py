from __future__ import annotations

from typing import List

from backend.models import LibraryPrompt


class PromptLibrary:
    def __init__(self) -> None:
        self._prompts: List[LibraryPrompt] = []
        self._counter = 1

    def add(self, name: str, content: str) -> LibraryPrompt:
        prompt = LibraryPrompt(id=self._counter, name=name, content=content)
        self._prompts.append(prompt)
        self._counter += 1
        return prompt

    def list(self) -> List[LibraryPrompt]:
        return self._prompts
