from typing import Protocol


class LLMClient(Protocol):
    def generate(self, text: str) -> str:
        ...
