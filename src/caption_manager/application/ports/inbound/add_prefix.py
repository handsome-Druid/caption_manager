from typing import Protocol

class AddPrefixServicePort(Protocol):
    async def run(self, folder: str, prefix: list[str]) -> dict[str, int]:
        ...