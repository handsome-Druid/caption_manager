from typing import Protocol

class CustomRemoveServicePort(Protocol):
    def run(self, folder: str, custom_tags: list[str]) -> None:
        ...