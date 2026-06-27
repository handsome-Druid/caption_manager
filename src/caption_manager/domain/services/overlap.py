from logging import getLogger

from caption_manager.domain.models import OverlapTags, Captions

logger = getLogger(__name__)

class OverlapService:
    @staticmethod
    def _normalize(tag: str):
        return tag.replace("_", " ")

    @staticmethod
    def run(captions: Captions, overlap_tags_list: list[OverlapTags]):
        overlap_index = {
            OverlapService._normalize(overlap_tags.query): overlap_tags for overlap_tags in overlap_tags_list
        }
        removed_tags: set[str] = set()
        for key, caption_list in captions.file_dict.items():
            present = {OverlapService._normalize(caption) for caption in caption_list}
            kept: list[str] = []
            removed_in_key: list[str] = []
            for caption in caption_list:
                normalized = OverlapService._normalize(caption)
                overlap_tags = overlap_index.get(normalized)
                if overlap_tags is not None:
                    has_overlap = {OverlapService._normalize(tag) for tag in overlap_tags.has_overlap}
                    if not has_overlap.isdisjoint(present - {normalized}):
                        removed_in_key.append(caption)
                        continue
                kept.append(caption)
            captions.file_dict[key] = kept
            if removed_in_key:
                logger.debug(f"Removed {len(removed_in_key)} captions from '{key}' due to overlap tags.")
            removed_tags.update(removed_in_key)
        captions.caption_dict.clear()
        for caption_list in captions.file_dict.values():
            for caption in caption_list:
                captions.caption_dict[caption] = captions.caption_dict.get(caption, 0) + 1
        logger.info(f"{len(removed_tags)} captions removed using overlap tags")
        logger.debug(f"Removed captions: {removed_tags}")
