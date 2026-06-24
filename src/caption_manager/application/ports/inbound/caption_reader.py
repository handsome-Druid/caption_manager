from typing import Protocol

from caption_manager.domain.models import Captions

class CaptionReaderServicePort(Protocol):
    async def read(self, folder: str) -> Captions:
        ...