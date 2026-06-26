import asyncio
from pathlib import Path
from logging import getLogger
from portalocker import LOCK_SH, Lock

from caption_manager.domain.models import Captions
from caption_manager.domain.exceptions import NotDirectoryError
from caption_manager.application.dto import FolderPath

logger = getLogger(__name__)

IMAGE_SUFFIXES = frozenset({
    ".png", ".jpg", ".jpeg", ".jfif", ".webp", ".bmp", ".gif", ".tif", ".tiff", ".avif",
})

class CaptionReaderImpl:
    def __init__(self, semaphore: asyncio.Semaphore | int = 5):
        self._semaphore = (
            semaphore if isinstance(semaphore, asyncio.Semaphore)
            else asyncio.Semaphore(semaphore)
        )

    @staticmethod
    def _locked_read(file_path: Path) -> str:
        with Lock(file_path, "r", timeout=5, flags=LOCK_SH, encoding="utf-8") as f:
            content = f.read()
        return content

    async def _read_file(self, file_path: Path) -> str:
        async with self._semaphore:
            return await asyncio.to_thread(self._locked_read, file_path)

    async def read_folder(self, folder: FolderPath) -> Captions:
        if not folder.path.is_dir():
            raise NotDirectoryError(f"{folder.path} is not a valid directory.")

        caption_files = [
            txt_file
            for txt_file in folder.path.rglob('*.txt')
            if any(
                txt_file.with_suffix(suffix).is_file()
                for suffix in IMAGE_SUFFIXES
            )
        ]
        file_dict: dict[Path, list[str]] = {}
        caption_dict: dict[str, int] = {}

        task_list = [self._read_file(caption_file) for caption_file in caption_files]
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
        return Captions(file_dict=file_dict, caption_dict=caption_dict)