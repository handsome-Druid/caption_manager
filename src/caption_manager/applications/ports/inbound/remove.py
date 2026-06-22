from typing import Protocol

class RemoveServicePort(Protocol):
    async def auto_remove(self, folder: str, flags: str) -> None:
        ...