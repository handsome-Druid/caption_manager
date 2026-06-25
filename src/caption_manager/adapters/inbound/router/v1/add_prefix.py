from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status
from pydantic import BaseModel

from caption_manager.application.ports.inbound import (
    AddPrefixServicePort,
    FolderResolverServicePort,
)

router = APIRouter(route_class=DishkaRoute)


class AddPrefixRequest(BaseModel):
    folder: str
    prefix: list[str]


@router.post("/add_prefix", status_code=status.HTTP_200_OK)
async def add_prefix(
    body: AddPrefixRequest,
    service: FromDishka[AddPrefixServicePort],
    folder_resolver: FromDishka[FolderResolverServicePort],
) -> dict[str, int]:
    return await service.run(folder_resolver.resolve(body.folder), body.prefix)
