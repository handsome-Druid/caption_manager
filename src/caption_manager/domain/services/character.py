from logging import getLogger

from caption_manager.domain.models import Captions, CharacterTags

logger = getLogger(__name__)

class CharacterService:
    @staticmethod
    def _matches_prefix(caption: str, prefix: str) -> bool:
        return caption == prefix or caption.startswith(f"{prefix} ")

    @staticmethod
    def _matches_suffix(caption: str, suffix: str) -> bool:
        return caption == suffix or caption.endswith(f" {suffix}")

    @staticmethod
    def _is_kept(caption: str, character_tags: CharacterTags, index: int) -> bool:
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

        for key, caption_list in captions.caption_dict.items():
            kept: list[str] = []
            removed_in_key: list[str] = []
            for caption in caption_list:
                if CharacterService._is_kept(caption, character_tags, index):
                    kept.append(caption)
                else:
                    removed_in_key.append(caption)
            captions.caption_dict[key] = kept
            removed_tags.update(removed_in_key)

            if removed_in_key:
                logger.debug(f"Removed {len(removed_in_key)} captions from '{key}' using character tags at index {index}.")

        captions.caption_set.clear()
        for caption_list in captions.caption_dict.values():
            captions.caption_set.update(caption_list)
        logger.info(f"Captions removed using character tags at index {index}: {removed_tags}")