from logging import getLogger
from pathlib import Path

import aiofiles
import asyncio

logger = getLogger(__name__)

class OverWriteImpl:

    def __init__(self, semaphore: asyncio.Semaphore | int = asyncio.Semaphore(5)):
        if isinstance(semaphore, int):
            self.semaphore = asyncio.Semaphore(semaphore)
        else:
            self.semaphore = semaphore

    async def _write_caption_file(self, caption_file: Path, captions: list[str]):
        async with self.semaphore, aiofiles.open(caption_file, mode='w', encoding='utf-8') as f:
            await f.write(','.join(captions))
        logger.debug(f"Overwritten {caption_file} with {len(captions)} captions.")

    async def run(self, patched_captions: dict[Path, list[str]]):
        tasks: list[asyncio.Task[None]] = []
        tasks.extend(
            asyncio.create_task(self._write_caption_file(caption_file, captions))
            for caption_file, captions in patched_captions.items()
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
        logger.info(f"Successfully overwritten {len(patched_captions)} caption files.")
