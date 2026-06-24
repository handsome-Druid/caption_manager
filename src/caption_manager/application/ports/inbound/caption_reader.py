from typing import Protocol, Literal

from caption_manager.domain.models import Captions

class CaptionReaderServicePort(Protocol):
    async def read(self, folder: str) -> Captions | Literal[False]:
        ...