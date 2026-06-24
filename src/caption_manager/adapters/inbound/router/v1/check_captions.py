from fastapi import APIRouter, Request, status

from caption_manager.application.ports.inbound import CaptionReaderServicePort

router = APIRouter()


@router.get("/check_captions", status_code=status.HTTP_200_OK)
async def check_captions(folder: str, request: Request) -> set[str]:
    service: CaptionReaderServicePort = request.app.state.caption_reader_service
    captions = await service.read(folder)
    return captions.caption_set
