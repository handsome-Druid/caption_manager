import sys
from portalocker import LOCK_SH, Lock
from pathlib import Path
from logging import getLogger

logger = getLogger(__name__)

from caption_manager.domain.exceptions import NotFileError
class BlacklistTagsImpl:
    def __init__(self, file: str):
        self.file_path = (
            Path(__file__).parents[4] / Path(f"filtering_tags/{file}")
            if "__compiled__" not in globals()
            else Path(sys.argv[0]).parent
            / Path(f"filtering_tags/{file}")
        )


    def read(self):
        if not self.file_path.is_file():
            raise NotFileError(f"{self.file_path} is not a valid file.")
        with Lock(self.file_path, "r", timeout=5, flags=LOCK_SH, encoding="utf-8") as file:
            logger.debug("Locked file: %s", self.file_path)
            blacklist_tags = [line.strip() for line in file.readlines()]
        logger.debug("Unlocked file: %s", self.file_path)
        return blacklist_tags
