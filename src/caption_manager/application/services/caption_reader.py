from logging import getLogger

from caption_manager.application.ports.outbound import CaptionReaderPort

logger = getLogger(__name__)

class CaptionReaderService:

    def __init__(self, caption_reader: CaptionReaderPort, debug: bool = False):
        self.caption_reader = caption_reader
        self.debug = debug

    async def read(self, folder: str):
        try:
            self._refresh_all()
            return await self.caption_reader.read_folder(folder)
        except Exception:
            if self.debug:
                raise
            logger.exception("Error occurred during caption reading.")
            return False
    
    def _refresh_all(self):
        self.caption_reader.refresh()
        logger.debug("Refreshed caption reader.")