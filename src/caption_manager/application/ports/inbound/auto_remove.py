from typing import Protocol

from caption_manager.application.dto import AutoRemoveConfig, FolderPath

class AutoRemoveServicePort(Protocol):
    async def run(self, config: AutoRemoveConfig, folder: FolderPath) -> dict[str, int]:
        ...