from typing import Protocol

from caption_manager.application.dto import FolderPath

class AddPrefixServicePort(Protocol):
    async def run(self, folder: FolderPath, prefix: list[str]) -> dict[str, int]:
        ...