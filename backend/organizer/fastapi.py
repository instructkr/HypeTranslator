from typing import Callable
from dependency_injector.wiring import inject, Provider
from fastapi import APIRouter, Depends

from backend.organizer.container import OrganizerContainer

from .dto import CreateOrganizerDTO, OrganizerDTO
from .service import OrganizerService

router = APIRouter(prefix="/organizer", tags=["organizer"])


@router.get("/{organizer_id}")
@inject
async def get_organizer(
    organizer_id: int,
    service: Callable[..., OrganizerService] = Depends(
        Provider[OrganizerContainer.service]
    ),
) -> OrganizerDTO | None:
    return await service().get_by_id(organizer_id)


@router.put("/")
@inject
async def create_organizer(
    organizer: CreateOrganizerDTO,
    service: Callable[..., OrganizerService] = Depends(
        Provider[OrganizerContainer.service]
    ),
) -> OrganizerDTO:
    return await service().create(organizer)
