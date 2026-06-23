from typing import Protocol

from caption_manager.domain.models import OverlapTags

class OverlapTagsPort(Protocol):
    def read(self) -> list[OverlapTags]:
        ...

    def refresh(self) -> None:
        ...