import sys
from pathlib import Path

from pydantic import BaseModel, Field

from caption_manager.domain.exceptions import NotFileError
from caption_manager.domain.models import CharacterTags


class _CharacterTagsSchema(BaseModel):
    whitelist: set[str] = Field(default_factory=set)
    suffixes: list[set[str]] = Field(default_factory=list[set[str]])
    prefixes: list[set[str]] = Field(default_factory=list[set[str]])


class CharacterTagsImpl:
    def __init__(self, file: str):
        self.file_path = (
            Path(__file__).parents[4] / Path(f"filtering_tags/{file}")
            if "__compiled__" not in globals()
            else Path(sys.argv[0]).parent
            / Path(f"filtering_tags/{file}")
        )
    
    def read(self):
        if not self.file_path.is_file():
            raise NotFileError(f"{self.file_path} is not a valid file.")
        with open(self.file_path, "r", encoding="utf-8") as file:
            parsed = _CharacterTagsSchema.model_validate_json(file.read())
            return CharacterTags(
                whitelist=frozenset(parsed.whitelist),
                suffixes=tuple(frozenset(tags) for tags in parsed.suffixes),
                prefixes=tuple(frozenset(tags) for tags in parsed.prefixes),
            )