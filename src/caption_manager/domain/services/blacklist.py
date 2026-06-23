from logging import getLogger

from caption_manager.domain.models import Captions

logger = getLogger(__name__)

class BlacklistService:
    
    @staticmethod
    def run(captions: Captions, blacklist_tags: list[str]):
        removed_count = 0
        flag_set = set(blacklist_tags)

        for key, caption_list in captions.caption_dict.items():
            original_len = len(caption_list)
            captions.caption_dict[key] = [caption for caption in caption_list if caption not in flag_set]
            removed_in_key = original_len - len(captions.caption_dict[key])
            removed_count += removed_in_key

            if removed_in_key > 0:
                logger.debug(f"Removed {removed_in_key} captions from '{key}'.")

        logger.info(f"Total captions removed: {removed_count} using blacklist.")