from logging import getLogger
from pathlib import Path

import aiofiles
import asyncio

from caption_manager.domain.models import Captions

logger = getLogger(__name__)

class OverWriteImpl:

    def __init__(self, semaphore: asyncio.Semaphore | int = 5):
        if isinstance(semaphore, int):
            self._semaphore_value = semaphore
            self._provided_semaphore: asyncio.Semaphore | None = None
        else:
            self._semaphore_value = 0
            self._provided_semaphore = semaphore

    async def _write_caption_file(self, caption_file: Path, captions: list[str], semaphore: asyncio.Semaphore):
        async with semaphore, aiofiles.open(caption_file, mode='w', encoding='utf-8') as f:
            await f.write(','.join(captions))
        logger.debug(f"Overwritten {caption_file} with {len(captions)} captions.")

    async def run(self, captions: Captions):
        tasks: list[asyncio.Task[None]] = []
        semaphore = self._provided_semaphore or asyncio.Semaphore(self._semaphore_value)
        tasks.extend(
            asyncio.create_task(self._write_caption_file(caption_file, captions, semaphore))
            for caption_file, captions in captions.caption_dict.items()
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
        logger.info(f"Successfully overwritten {len(captions.caption_dict)} caption files.")
