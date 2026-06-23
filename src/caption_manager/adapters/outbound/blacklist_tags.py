import sys
from pathlib import Path

from caption_manager.domain.exceptions import NotFileError
class BlacklistTagsImpl:
    _cache: list[str] = []
    def __init__(self, file: str):
        self.file_path = (
            Path(__file__).parents[4] / Path(f"filtering_tags/{file}")
            if "__compiled__" in globals()
            else Path(sys.argv[0]).parent
            / Path(f"filtering_tags/{file}")
        )


    def read(self):
        if not self.file_path.is_file():
            raise NotFileError(f"{self.file_path} is not a valid file.")
        if self._cache:
            return self._cache
        with open(self.file_path, "r", encoding="utf-8") as file:
            self._cache = [line.strip() for line in file.readlines()]
        return self._cache
    
    def refresh(self):
        self._cache = []

