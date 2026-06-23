from pydantic import BaseModel, Field


class CharacterTags(BaseModel):
    whitelist: set[str] = Field(default_factory=set)
    suffixes: list[set[str]] = Field(default_factory=list[set[str]])
    prefixes: list[set[str]] = Field(default_factory=list[set[str]])