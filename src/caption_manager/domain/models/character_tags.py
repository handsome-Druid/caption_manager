from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class CharacterTags:
    whitelist: frozenset[str]
    suffixes: tuple[frozenset[str], ...]
    prefixes: tuple[frozenset[str], ...]