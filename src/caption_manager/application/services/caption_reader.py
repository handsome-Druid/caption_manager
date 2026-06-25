import asyncio
from collections.abc import Hashable
from weakref import WeakValueDictionary
from logging import getLogger

from caption_manager.application.ports.outbound import CaptionReaderPort
from caption_manager.application.dto import FolderPath

logger = getLogger(__name__)

class CaptionReaderService:

    def __init__(self, caption_reader: CaptionReaderPort, lock: WeakValueDictionary[Hashable, asyncio.Lock]):
        self.caption_reader = caption_reader
        self._lock = lock

    async def read(self, folder: FolderPath):
        if (lock := self._lock.get(folder)) is None:
            self._lock[folder] = lock = asyncio.Lock()
        async with lock:
            captions = await self.caption_reader.read_folder(folder)
        return captions.caption_dict