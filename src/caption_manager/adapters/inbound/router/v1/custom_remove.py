from fastapi import APIRouter, Request, status
from pydantic import BaseModel

from caption_manager.application.ports.inbound import (
    CustomRemoveServicePort,
    FolderResolverServicePort,
)

router = APIRouter()


class CustomRemoveRequest(BaseModel):
    folder: str
    custom_tags: list[str]


@router.post("/custom_remove", status_code=status.HTTP_200_OK)
async def custom_remove(body: CustomRemoveRequest, request: Request) -> dict[str, int]:
    service: CustomRemoveServicePort = request.app.state.custom_remove_service
    folder_resolver: FolderResolverServicePort = request.app.state.folder_resolver
    return await service.run(folder_resolver.resolve(body.folder), body.custom_tags)