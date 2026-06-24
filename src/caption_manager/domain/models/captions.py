from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Captions:
    file_dict: dict[Path, list[str]]
    caption_dict: dict[str, int]