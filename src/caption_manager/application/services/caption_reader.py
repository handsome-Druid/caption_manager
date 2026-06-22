from caption_manager.application.ports.outbound import CaptionReaderPort

class CaptionReaderService:

    def __init__(self, folder_path: str, caption_reader: CaptionReaderPort):
        self.folder_path = folder_path
        self.caption_reader = caption_reader

    async def read_captions(self):
        return await self.caption_reader.read_folder(self.folder_path)
    
    def refresh(self):
        self.caption_reader.refresh()