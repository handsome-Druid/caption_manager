from logging import getLogger

from caption_manager.domain.services import RemoveService as RemoveServiceDomain
from caption_manager.application.ports.outbound import CaptionReaderPort, FlagReaderPort, OverWritePort

logger = getLogger(__name__)

class RemoveService:
    def __init__(self, caption_reader: CaptionReaderPort, flag_reader: FlagReaderPort, over_write: OverWritePort):
        self.caption_reader = caption_reader
        self.flag_reader = flag_reader
        self.over_write = over_write

    async def auto_remove(self, folder: str, flags: str) -> None:
        captions = await self.caption_reader.read_folder(folder)
        remove_flags = self.flag_reader.read(flags)
        patched_captions = RemoveServiceDomain.run(captions, remove_flags)
        self.over_write.run(patched_captions)
