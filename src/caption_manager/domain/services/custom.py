from logging import getLogger

from caption_manager.domain.models import Captions

logger = getLogger(__name__)

class CustomService:
    
    @staticmethod
    def run(captions: Captions, custom_tags: list[str]):
        removed_tags: set[str] = set()
        custom_set = set(custom_tags)

        for key, caption_list in captions.file_dict.items():
            kept = [caption for caption in caption_list if caption not in custom_set]
            removed_in_key = [caption for caption in caption_list if caption in custom_set]
            captions.file_dict[key] = kept
            removed_tags.update(removed_in_key)

            if removed_in_key:
                logger.debug(f"Removed {len(removed_in_key)} captions from '{key}' using custom tags.")

        captions.caption_dict.clear()
        for caption_list in captions.file_dict.values():
            for caption in caption_list:
                captions.caption_dict[caption] = captions.caption_dict.get(caption, 0) + 1
        logger.info(f"{len(removed_tags)} captions removed using custom tags")
        logger.debug(f"Removed captions: {removed_tags}")