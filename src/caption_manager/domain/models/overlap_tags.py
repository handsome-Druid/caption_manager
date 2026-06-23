from pydantic import BaseModel, Field

class OverlapTags(BaseModel):
    query: str
    post_count: int
    overlap_tags: set[str] = Field(default_factory=set)
    group_tags: set[str] = Field(default_factory=set)
    related_tags: set[str] = Field(default_factory=set)
    wiki_tags: set[str] = Field(default_factory=set)
    has_overlap: set[str] = Field(default_factory=set)