from typing import Protocol

from caption_manager.application.dto import FolderPath

class CustomRemoveServicePort(Protocol):
    async def run(self, folder: FolderPath, custom_tags: list[str]) -> dict[str, int]:
        ...