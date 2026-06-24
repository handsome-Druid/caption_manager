from logging import getLogger

from caption_manager.domain.models import Captions

logger = getLogger(__name__)

class PrefixService:
    @staticmethod
    def run(captions: Captions, prefix: list[str]):
        prefix_set = set(prefix)
        for key, caption_list in captions.file_dict.items():
            rest = [caption for caption in caption_list if caption not in prefix_set]
            captions.file_dict[key] = prefix + rest

        captions.caption_dict.clear()
        for caption_list in captions.file_dict.values():
            for caption in caption_list:
                captions.caption_dict[caption] = captions.caption_dict.get(caption, 0) + 1
        logger.info(f"Prefix tags applied to head of each caption: {prefix}")