from copy import deepcopy
from logging import getLogger

from caption_manager.domain.models import Captions

logger = getLogger(__name__)

class RemoveService:
    
    @staticmethod
    def run(captions: Captions, remove_flags: list[str]):

        patched_captions = deepcopy(captions.caption_dict)
        for k, v in captions.caption_dict.items():
            for flag in remove_flags:
                for caption in v:
                    if flag in caption:
                        try:
                            patched_captions[k].remove(caption)
                            logger.debug(f"Removed caption '{caption}' from '{k}' due to flag '{flag}'.")
                        except ValueError:
                            logger.debug(f"Caption '{caption}' not found in '{k}' for removal.")

        return patched_captions