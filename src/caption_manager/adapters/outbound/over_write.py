from logging import getLogger
from pathlib import Path
from portalocker import Lock

import asyncio

from caption_manager.domain.models import Captions

logger = getLogger(__name__)

class OverWriteImpl:

    def __init__(self, semaphore: asyncio.Semaphore | int = 5):
        self._semaphore = (
            semaphore if isinstance(semaphore, asyncio.Semaphore)
            else asyncio.Semaphore(semaphore)
        )

    @staticmethod
    def _locked_write(caption_file: Path, captions: list[str]) -> None:
        with Lock(caption_file, "w", timeout=5, encoding="utf-8") as f:
            logger.debug("Locked file with write mode: %s", caption_file)
            f.write(','.join(captions))
        logger.debug("Unlocked file with write mode: %s", caption_file)

    @classmethod
    async def _write_caption_file(cls, caption_file: Path, captions: list[str], semaphore: asyncio.Semaphore):
        async with semaphore:
            await asyncio.to_thread(cls._locked_write, caption_file, captions)
        logger.debug("Overwritten %s with %d captions.", caption_file, len(captions))

    async def run(self, captions: Captions):
        tasks: list[asyncio.Task[None]] = []
        tasks.extend(
            asyncio.create_task(self._write_caption_file(caption_file, captions, self._semaphore))
            for caption_file, captions in captions.file_dict.items()
        )
        results = await asyncio.gather(*tasks, return_exceptions=True)
        base_exceptions: list[BaseException] = []
        for result in results:
            match result:
                case Exception():
                    logger.exception("An error occurred while overwriting caption files.")
                case asyncio.CancelledError():
                    raise result
                case BaseException():
                    base_exceptions.append(result)
                case _:
                    ...
        if base_exceptions:
            raise BaseExceptionGroup("Multiple exceptions occurred while overwriting caption files.", base_exceptions)
        logger.info("Overwritten %d caption files.", len(captions.file_dict))
