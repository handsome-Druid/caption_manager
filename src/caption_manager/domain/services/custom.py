from logging import getLogger

from caption_manager.domain.models import Captions

logger = getLogger(__name__)

class CustomService:
    
    @staticmethod
    def run(captions: Captions, custom_tags: list[str]):
        removed_tags: set[str] = set()
        custom_set = set(custom_tags)

        for key, caption_list in captions.caption_dict.items():
            kept = [caption for caption in caption_list if caption not in custom_set]
            removed_in_key = [caption for caption in caption_list if caption in custom_set]
            captions.caption_dict[key] = kept
            removed_tags.update(removed_in_key)

            if removed_in_key:
                logger.debug(f"Removed {len(removed_in_key)} captions from '{key}' using custom tags.")

        captions.caption_set.clear()
        for caption_list in captions.caption_dict.values():
            captions.caption_set.update(caption_list)
        logger.info(f"Captions removed using custom tags: {removed_tags}")