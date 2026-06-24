from logging import getLogger

from caption_manager.domain.models import Captions, CharacterTags

logger = getLogger(__name__)

class CharacterService:
    @staticmethod
    def _matches_prefix(caption: str, prefix: str):
        return caption == prefix or caption.startswith(f"{prefix} ")

    @staticmethod
    def _matches_suffix(caption: str, suffix: str):
        return caption == suffix or caption.endswith(f" {suffix}")

    @staticmethod
    def _is_kept(caption: str, character_tags: CharacterTags, index: int):
        return caption in character_tags.whitelist or (
            all(
                not CharacterService._matches_prefix(caption, prefix)
                for prefix in character_tags.prefixes[index]
            )
            and all(
                not CharacterService._matches_suffix(caption, suffix)
                for suffix in character_tags.suffixes[index]
            )
        )

    @staticmethod
    def run(captions: Captions, character_tags: CharacterTags, index: int):
        removed_tags: set[str] = set()

        for key, caption_list in captions.file_dict.items():
            kept: list[str] = []
            removed_in_key: list[str] = []
            for caption in caption_list:
                if CharacterService._is_kept(caption, character_tags, index):
                    kept.append(caption)
                else:
                    removed_in_key.append(caption)
            captions.file_dict[key] = kept
            removed_tags.update(removed_in_key)

            if removed_in_key:
                logger.debug(f"Removed {len(removed_in_key)} captions from '{key}' using character tags at index {index}.")

        captions.caption_dict.clear()
        for caption_list in captions.file_dict.values():
            for caption in caption_list:
                captions.caption_dict[caption] = captions.caption_dict.get(caption, 0) + 1
        logger.info(f"{len(removed_tags)} captions removed using character tags at index {index}")
        logger.debug(f"Removed captions: {removed_tags}")
