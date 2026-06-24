import asyncio
from logging import getLogger

from caption_manager.application.ports.outbound import (
    CaptionReaderPort,
    OverWritePort,
)
from caption_manager.domain.services import CustomService

logger = getLogger(__name__)

class CustomRemoveService:
    def __init__(
        self,
        caption_reader: CaptionReaderPort,
        over_write: OverWritePort,
    ):
        self.caption_reader = caption_reader
        self.over_write = over_write

    def _refresh_all(self):
        self.caption_reader.refresh()
        logger.debug("Refreshed caption reader.")

    def run(self, folder: str, custom_tags: list[str]):
        captions = asyncio.run(self.caption_reader.read_folder(folder))
        CustomService.run(captions, custom_tags)
        asyncio.run(self.over_write.run(captions))