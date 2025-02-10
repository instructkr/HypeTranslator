from contextlib import AbstractAsyncContextManager
from typing import Callable, List

from sqlalchemy.ext.asyncio import AsyncSession
from .repository import OrganizerRepository
from .dto import OrganizerDTO, CreateOrganizerDTO, from_model


class OrganizerService:
    def __init__(
        self,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
        repository: OrganizerRepository,
    ):
        self._session_factory = session_factory
        self.repository = repository

    async def create(self, dto: CreateOrganizerDTO) -> OrganizerDTO:
        async with self._session_factory() as session:
            return from_model(await self.repository.add(session, dto))

    async def get_by_id(self, organize_id: int) -> OrganizerDTO | None:
        async with self._session_factory() as session:
            result = await self.repository.get_by_id(session, organize_id)
            return from_model(result) if result is not None else None

    async def filter_by_names(self, names: List[str]) -> List[OrganizerDTO]:
        async with self._session_factory() as session:
            return list(
                map(from_model, await self.repository.filter_by_names(session, names))
            )
