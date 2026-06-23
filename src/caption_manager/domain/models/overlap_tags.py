from pydantic import BaseModel, Field


class OverlapTags(BaseModel):
    query: str
    post_count: int
    overlap_tags: list[str] = Field(default_factory=list)
    group_tags: list[str] = Field(default_factory=list)
    related_tags: list[str] = Field(default_factory=list)
    wiki_tags: list[str] = Field(default_factory=list)
    has_overlap: list[str] = Field(default_factory=list)