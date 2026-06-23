from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class OverlapTags:
    query: str
    post_count: int
    has_overlap: frozenset[str]