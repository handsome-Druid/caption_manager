from fastapi import APIRouter, Request, status
from pydantic import BaseModel

from caption_manager.application.ports.inbound import AddPrefixServicePort

router = APIRouter()


class AddPrefixRequest(BaseModel):
    folder: str
    prefix: list[str]


@router.post("/add_prefix", status_code=status.HTTP_200_OK)
async def add_prefix(body: AddPrefixRequest, request: Request) -> dict[str, int]:
    service: AddPrefixServicePort = request.app.state.add_prefix_service
    return await service.run(body.folder, body.prefix)
