from pathlib import Path
from typing import Protocol

from caption_manager.domain.models import Captions
from caption_manager.application.dto import FolderPath

class CaptionReaderPort(Protocol):

    async def read_folder(self, folder: FolderPath) -> Captions:
        ...