from typing import Protocol

class BlacklistTagsPort(Protocol):
    def read(self) -> list[str]:
        ...