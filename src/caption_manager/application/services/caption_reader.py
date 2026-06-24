from logging import getLogger

from caption_manager.application.ports.outbound import CaptionReaderPort

logger = getLogger(__name__)

class CaptionReaderService:

    def __init__(self, caption_reader: CaptionReaderPort):
        self.caption_reader = caption_reader

    async def read(self, folder: str):
        self._refresh_all()
        captions = await self.caption_reader.read_folder(folder)
        return captions.caption_dict

    def _refresh_all(self):
        self.caption_reader.refresh()
        logger.debug("Refreshed caption reader.")