from typing import Protocol

from caption_manager.application.dto import FolderPath

class FolderResolverServicePort(Protocol):
    def resolve(self, folder: str) -> FolderPath:
        ...
