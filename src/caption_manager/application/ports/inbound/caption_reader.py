from typing import Protocol

class CaptionReaderServicePort(Protocol):
    async def read(self, folder: str) -> dict[str, int]:
        ...