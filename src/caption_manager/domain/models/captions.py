from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Captions:
    caption_dict: dict[Path, list[str]]
    caption_set: set[str]