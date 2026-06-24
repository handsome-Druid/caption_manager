from typing import Protocol

class CustomRemoveServicePort(Protocol):
    async def run(self, folder: str, custom_tags: list[str]) -> dict[str, int]:
        ...