import asyncio
import sys
from pathlib import Path
from logging import getLogger

import aiofiles

from caption_manager.domain.models import Captions
from caption_manager.domain.exceptions import NotDirectoryError

logger = getLogger(__name__)

class CaptionReaderImpl:
    _cache: dict[str, Captions] = {}

    def __init__(self, semaphore: asyncio.Semaphore | int = asyncio.Semaphore(5)):
        if isinstance(semaphore, int):
            self.semaphore = asyncio.Semaphore(semaphore)
        else:
            self.semaphore = semaphore

    def refresh(self):
        self._cache.clear()

    async def _read_file(self, file_path: Path):
        async with self.semaphore, aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
            content = await file.read()
        return content
    
    async def read_folder(self, folder: str) -> Captions:
        if self._cache.get(folder):
            logger.debug(f"Cache hit for folder: {folder}")
            return self._cache[folder]
        folder_path = (
            Path(sys.argv[0]).parent / Path(folder)
            if "__compiled__" in globals() else
            Path(__file__).parents[4] / Path(folder)
        )
        if not folder_path.is_dir():
            raise NotDirectoryError(f"{folder_path} is not a valid directory.")
        
        caption_files = list(folder_path.glob('*.txt'))
        caption_dict: dict[Path, list[str]] = {}
        caption_list: list[str] = []

        task_list = [self._read_file(caption_file) for caption_file in caption_files]
        contents = await asyncio.gather(*task_list, return_exceptions=True)
        base_exceptions: list[BaseException] = []
        for caption_file, content in zip(caption_files, contents):
            match content:
                case Exception():
                    logger.exception(f"Failed to read {caption_file}")
                case asyncio.CancelledError():
                    raise content
                case BaseException():
                    base_exceptions.append(content)
                case _:
                    cleaned_items = [
                        item
                        for item in (s.strip() for s in content.replace('\n', ',').split(','))
                        if item
                    ]
                    caption_list.extend(cleaned_items)
                    caption_dict[caption_file] = cleaned_items
        if base_exceptions:
            raise BaseExceptionGroup("Multiple exceptions occurred while reading caption files.", base_exceptions)

        captions = Captions(caption_dict=caption_dict, caption_set=set(caption_list))
        self._cache[folder] = captions
        return captions