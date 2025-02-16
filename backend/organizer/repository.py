from typing import Iterable, List, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models import OrganizerModel
from .dto import CreateOrganizerDTO


class OrganizerRepository:
    def __init__(self):
        pass

    async def get_by_id(
        self, session: AsyncSession, organizer_id: int
    ) -> OrganizerModel | None:
        return await session.get(OrganizerModel, organizer_id)

    async def filter_by_names(
        self, session: AsyncSession, names: List[str]
    ) -> Sequence[OrganizerModel]:
        query = select(OrganizerModel).filter(OrganizerModel.name.in_(names))
        result = await session.execute(query)
        return result.scalars().all()

    async def filter_by_ids(
        self, session: AsyncSession, ids: Iterable[int]
    ) -> Sequence[OrganizerModel]:
        query = select(OrganizerModel).filter(OrganizerModel.organizer_id.in_(ids))
        result = await session.execute(query)
        return result.scalars().all()

    async def add(
        self, session: AsyncSession, dto: CreateOrganizerDTO
    ) -> OrganizerModel:
        organizer = OrganizerModel(name=dto.name, articles=[], belongs_to_x_account=[])
        session.add(organizer)
        await session.flush()
        return organizer
