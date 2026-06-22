from typing import Protocol

class FlagReaderPort(Protocol):
    def read(self, file: str) -> list[str]:
        ...