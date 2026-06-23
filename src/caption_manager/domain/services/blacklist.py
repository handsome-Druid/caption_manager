from logging import getLogger

from caption_manager.domain.models import Captions

logger = getLogger(__name__)

class BlacklistService:
    
    @staticmethod
    def run(captions: Captions, blacklist_tags: list[str]):
        removed_tags: set[str] = set()
        blacklist_set = set(blacklist_tags)

        for key, caption_list in captions.caption_dict.items():
            kept = [caption for caption in caption_list if caption not in blacklist_set]
            removed_in_key = [caption for caption in caption_list if caption in blacklist_set]
            captions.caption_dict[key] = kept
            removed_tags.update(removed_in_key)

            if removed_in_key:
                logger.debug(f"Removed {len(removed_in_key)} captions from '{key}' using blacklist.")

        captions.caption_set.clear()
        for caption_list in captions.caption_dict.values():
            captions.caption_set.update(caption_list)
        logger.info(f"Captions removed using blacklist: {removed_tags}")