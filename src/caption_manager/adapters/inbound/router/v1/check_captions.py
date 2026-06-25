from fastapi import APIRouter, Request, status

from caption_manager.application.ports.inbound import (
    CaptionReaderServicePort,
    FolderResolverServicePort,
)

router = APIRouter()


@router.get("/check_captions", status_code=status.HTTP_200_OK)
async def check_captions(folder: str, request: Request) -> dict[str, int]:
    service: CaptionReaderServicePort = request.app.state.caption_reader_service
    folder_resolver: FolderResolverServicePort = request.app.state.folder_resolver
    return await service.read(folder_resolver.resolve(folder))
