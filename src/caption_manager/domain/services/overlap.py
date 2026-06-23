from logging import getLogger

from caption_manager.domain.models import OverlapTags, Captions

logger = getLogger(__name__)

class OverlapService:
    @staticmethod
    def run(captions: Captions, overlap_tags_list: list[OverlapTags]):
        overlap_index = {overlap_tags.query: overlap_tags for overlap_tags in overlap_tags_list}
        removed_tags: set[str] = set()
        for key, caption_list in captions.caption_dict.items():
            present = set(caption_list)
            kept: list[str] = []
            removed_in_key: list[str] = []
            for caption in caption_list:
                overlap_tags = overlap_index.get(caption)
                if overlap_tags is not None and not overlap_tags.has_overlap.isdisjoint(present - {caption}):
                    removed_in_key.append(caption)
                    continue
                kept.append(caption)
            captions.caption_dict[key] = kept
            if removed_in_key:
                logger.debug(f"Removed {len(removed_in_key)} captions from '{key}' due to overlap tags.")
            removed_tags.update(removed_in_key)
        captions.caption_set.clear()
        for caption_list in captions.caption_dict.values():
            captions.caption_set.update(caption_list)
        logger.info(f"Captions removed using overlap tags: {removed_tags}")
