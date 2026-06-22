from logging import getLogger
from pathlib import Path

logger = getLogger(__name__)

class OverWriteImpl:
    def run(self, patched_captions: dict[Path, list[str]]):
        for caption_file, captions in patched_captions.items():
            with open(caption_file, mode='w', encoding='utf-8') as f:
                f.write('\n'.join(captions))
            logger.debug(f"Overwritten {caption_file} with {len(captions)} captions.")
        logger.info(f"Successfully overwritten {len(patched_captions)} caption files.")