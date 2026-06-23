from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class AutoRemoveConfig:
    overlap: bool
    character_range: int