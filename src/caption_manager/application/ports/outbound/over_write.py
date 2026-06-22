from typing import Protocol
from pathlib import Path

class OverWritePort(Protocol):
    def run(self, patched_captions: dict[Path, list[str]]) -> None:
        ...