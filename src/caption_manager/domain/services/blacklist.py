from logging import getLogger

from caption_manager.domain.models import Captions

logger = getLogger(__name__)

class BlacklistService:

    @staticmethod
    def run(captions: Captions, blacklist_tags: list[str]):
        removed_tags: set[str] = set()
        blacklist_set = set(blacklist_tags)

        for key, caption_list in captions.file_dict.items():
            kept = [caption for caption in caption_list if caption not in blacklist_set]
            removed_in_key = [caption for caption in caption_list if caption in blacklist_set]
            captions.file_dict[key] = kept
            removed_tags.update(removed_in_key)

            if removed_in_key:
                logger.debug("Removed %d captions from '%s' using blacklist.", len(removed_in_key), key)

        captions.caption_dict.clear()
        for caption_list in captions.file_dict.values():
            for caption in caption_list:
                captions.caption_dict[caption] = captions.caption_dict.get(caption, 0) + 1
        logger.info("%d captions removed using blacklist", len(removed_tags))
        logger.debug("Removed captions: %s", removed_tags)