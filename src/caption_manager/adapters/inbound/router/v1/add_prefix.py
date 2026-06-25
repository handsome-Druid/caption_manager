from fastapi import APIRouter, Request, status
from pydantic import BaseModel

from caption_manager.application.ports.inbound import (
    AddPrefixServicePort,
    FolderResolverServicePort,
)

router = APIRouter()


class AddPrefixRequest(BaseModel):
    folder: str
    prefix: list[str]


@router.post("/add_prefix", status_code=status.HTTP_200_OK)
async def add_prefix(body: AddPrefixRequest, request: Request) -> dict[str, int]:
    service: AddPrefixServicePort = request.app.state.add_prefix_service
    folder_resolver: FolderResolverServicePort = request.app.state.folder_resolver
    return await service.run(folder_resolver.resolve(body.folder), body.prefix)
