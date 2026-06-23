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

    def __init__(self, semaphore: asyncio.Semaphore | int = 5):
        # 不要在此处创建 asyncio.Semaphore，因为它会在首次使用时绑定到当时的事件循环。
        # 多次 asyncio.run() 会创建不同的事件循环，复用同一个信号量会触发
        # "bound to a different event loop" 错误。改为记录并发上限，按需在运行的事件循环中创建。
        if isinstance(semaphore, int):
            self._semaphore_value = semaphore
            self._provided_semaphore: asyncio.Semaphore | None = None
        else:
            self._semaphore_value = 0
            self._provided_semaphore = semaphore

    def refresh(self):
        self._cache.clear()

    async def _read_file(self, file_path: Path, semaphore: asyncio.Semaphore):
        async with semaphore, aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
            content = await file.read()
        return content
    
    async def read_folder(self, folder: str):
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
        caption_set: set[str] = set()

        # 在当前运行的事件循环中创建信号量，避免跨事件循环复用导致的错误。
        semaphore = self._provided_semaphore or asyncio.Semaphore(self._semaphore_value)
        task_list = [self._read_file(caption_file, semaphore) for caption_file in caption_files]
        contents = await asyncio.gather(*task_list, return_exceptions=True)
        base_exceptions: list[BaseException] = []
        for caption_file, content in zip(caption_files, contents):
            match content:
                case Exception():
                    logger.error("Failed to read %s", caption_file, exc_info=content)
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
                    caption_set.update(cleaned_items)
                    caption_dict[caption_file] = cleaned_items
        if base_exceptions:
            raise BaseExceptionGroup("Multiple exceptions occurred while reading caption files.", base_exceptions)

        captions = Captions(caption_dict=caption_dict, caption_set=caption_set)
        self._cache[folder] = captions
        return captions