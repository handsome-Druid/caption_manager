from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status
from pydantic import BaseModel

from caption_manager.application.ports.inbound import (
    CustomRemoveServicePort,
    FolderResolverServicePort,
)

router = APIRouter(route_class=DishkaRoute)


class CustomRemoveRequest(BaseModel):
    folder: str
    custom_tags: list[str]


@router.post("/custom_remove", status_code=status.HTTP_200_OK)
async def custom_remove(
    body: CustomRemoveRequest,
    service: FromDishka[CustomRemoveServicePort],
    folder_resolver: FromDishka[FolderResolverServicePort],
) -> dict[str, int]:
    return await service.run(folder_resolver.resolve(body.folder), body.custom_tags)