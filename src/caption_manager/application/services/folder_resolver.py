from pathlib import Path

from caption_manager.application.dto import FolderPath

class FolderResolverService:
    def __init__(self, base_dir: Path):
        self._base_dir = base_dir

    def resolve(self, folder: str) -> FolderPath:
        return FolderPath((self._base_dir / folder).resolve())
