from fastapi import APIRouter, Request, status, HTTPException

from caption_manager.application.ports.inbound import CaptionReaderServicePort

router = APIRouter()


@router.get("/check_captions", status_code=status.HTTP_200_OK)
async def check_captions(folder: str, request: Request) -> set[str]:
    service: CaptionReaderServicePort = request.app.state.caption_reader_service
    try:
        if not (captions := await service.read(folder)):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return captions.caption_set
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
