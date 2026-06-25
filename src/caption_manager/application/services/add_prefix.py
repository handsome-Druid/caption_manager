import asyncio
from collections.abc import Hashable
from weakref import WeakValueDictionary
from logging import getLogger

from caption_manager.domain.services import PrefixService
from caption_manager.application.ports.outbound import (
    CaptionReaderPort,
    OverWritePort,
)
from caption_manager.application.dto import FolderPath

logger = getLogger(__name__)

class AddPrefixService:
    def __init__(
        self,
        *,
        caption_reader: CaptionReaderPort,
        over_write: OverWritePort,
        lock: WeakValueDictionary[Hashable, asyncio.Lock],
    ):
        self.caption_reader = caption_reader
        self.over_write = over_write
        self._lock = lock

    async def run(self, folder: FolderPath, prefix: list[str]):
        if (lock := self._lock.get(folder)) is None:
            self._lock[folder] = lock = asyncio.Lock()
        async with lock:
            captions = await self.caption_reader.read_folder(folder)
            PrefixService.run(captions, prefix)
            await self.over_write.run(captions)
        return captions.caption_dict