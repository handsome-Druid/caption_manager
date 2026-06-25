from fastapi import APIRouter, Request, status
from pydantic import BaseModel

from caption_manager.application.dto import AutoRemoveConfig
from caption_manager.application.ports.inbound import (
    AutoRemoveServicePort,
    FolderResolverServicePort,
)

router = APIRouter()


class AutoRemoveRequest(BaseModel):
    folder: str
    overlap: bool = False
    character_range: int = 0


@router.post("/auto_remove", status_code=status.HTTP_200_OK)
async def auto_remove(body: AutoRemoveRequest, request: Request) -> dict[str, int]:
    service: AutoRemoveServicePort = request.app.state.auto_remove_service
    folder_resolver: FolderResolverServicePort = request.app.state.folder_resolver
    config = AutoRemoveConfig(overlap=body.overlap, character_range=body.character_range)
    return await service.run(config, folder_resolver.resolve(body.folder))