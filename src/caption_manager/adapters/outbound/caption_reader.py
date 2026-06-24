import asyncio
import sys
from pathlib import Path
from logging import getLogger

import aiofiles

from caption_manager.domain.models import Captions
from caption_manager.domain.exceptions import NotDirectoryError

logger = getLogger(__name__)

IMAGE_SUFFIXES = frozenset({
    ".png", ".jpg", ".jpeg", ".jfif", ".webp", ".bmp", ".gif", ".tif", ".tiff", ".avif",
})

class CaptionReaderImpl:
    _cache: dict[str, Captions] = {}

    def __init__(self, semaphore: asyncio.Semaphore | int = 5):
        self._semaphore = (
            semaphore if isinstance(semaphore, asyncio.Semaphore)
            else asyncio.Semaphore(semaphore)
        )

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

        # 递归展开所有子文件夹查找 txt，仅当同目录存在同名图片文件时才读取对应的 txt。
        caption_files = [
            txt_file
            for txt_file in folder_path.rglob('*.txt')
            if any(
                txt_file.with_suffix(suffix).is_file()
                for suffix in IMAGE_SUFFIXES
            )
        ]
        file_dict: dict[Path, list[str]] = {}
        caption_dict: dict[str, int] = {}

        task_list = [self._read_file(caption_file, self._semaphore) for caption_file in caption_files]
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
                    logger.debug("Read %s with %d captions.", caption_file, len(cleaned_items))
                    for caption in cleaned_items:
                        caption_dict[caption] = caption_dict.get(caption, 0) + 1
                    file_dict[caption_file] = cleaned_items
        if base_exceptions:
            raise BaseExceptionGroup("Multiple exceptions occurred while reading caption files.", base_exceptions)
        logger.info("Read %d caption files with a total of %d unique captions.", len(file_dict), len(caption_dict))
        captions = Captions(file_dict=file_dict, caption_dict=caption_dict)
        self._cache[folder] = captions
        return captions