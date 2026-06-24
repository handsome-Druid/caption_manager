from typing import Protocol

from caption_manager.domain.models import CharacterTags

class CharacterTagsPort(Protocol):
    def read(self) -> CharacterTags:
        ...