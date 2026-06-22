from typing import Protocol

from caption_manager.domain.models import Captions

class CaptionReaderServicePort(Protocol):
    async def read_captions(self) -> Captions:
        ...

    def refresh(self) -> None:
        ...