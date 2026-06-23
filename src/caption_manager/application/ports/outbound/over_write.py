from typing import Protocol

from caption_manager.domain.models import Captions

class OverWritePort(Protocol):
    async def run(self, captions: Captions) -> None:
        ...