from typing import Protocol

from caption_manager.domain.models import Captions

class CaptionReaderPort(Protocol):

    async def read_folder(self, folder: str) -> Captions:
        ...