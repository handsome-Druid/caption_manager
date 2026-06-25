from typing import Protocol

from caption_manager.application.dto import FolderPath

class CaptionReaderServicePort(Protocol):
    async def read(self, folder: FolderPath) -> dict[str, int]:
        ...