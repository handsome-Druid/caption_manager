import sys
from pathlib import Path

from pydantic import BaseModel, Field, TypeAdapter

from caption_manager.domain.exceptions import NotFileError
from caption_manager.domain.models import OverlapTags


class _OverlapTagsSchema(BaseModel):
    query: str
    post_count: int
    overlap_tags: set[str] = Field(default_factory=set)
    group_tags: set[str] = Field(default_factory=set)
    related_tags: set[str] = Field(default_factory=set)
    wiki_tags: set[str] = Field(default_factory=set)
    has_overlap: set[str] = Field(default_factory=set)

class OverlapTagsImpl:
    _cache: list[OverlapTags] | None = None
    overlap_tags_list = TypeAdapter(list[_OverlapTagsSchema])

    def __init__(self, file: str):
        self.file_path = (
            Path(__file__).parents[4] / Path(f"filtering_tags/{file}")
            if "__compiled__" not in globals()
            else Path(sys.argv[0]).parent / Path(f"filtering_tags/{file}")
        )

    def read(self):
        if not self.file_path.is_file():
            raise NotFileError(f"{self.file_path} is not a valid file.")
        if self._cache:
            return self._cache
        with open(self.file_path, "r", encoding="utf-8") as file:
            parsed_list = self.overlap_tags_list.validate_json(file.read())
            self._cache = [
                OverlapTags(
                    query=parsed.query,
                    post_count=parsed.post_count,
                    has_overlap=frozenset(parsed.has_overlap),
                )
                for parsed in parsed_list
            ]
        return self._cache
    
    def refresh(self):
        self._cache = None
