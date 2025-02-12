from typing import Iterable, List, Callable
from contextlib import AbstractAsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import ArticleRepository
from .dto import ArticleDTO, CreateArticleDTO, from_model, model_list_to_dto_list
from ..organizer.service import OrganizerService


class ArticleService:
    def __init__(
        self,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
        repository: ArticleRepository,
        organizer_service: OrganizerService,
    ):
        self.repository = repository
        self._session_factory = session_factory
        self.organizer_service = organizer_service

    async def create(self, dto: CreateArticleDTO) -> ArticleDTO:
        async with self._session_factory() as session:
            return await from_model(await self.repository.add(session, dto))

    async def create_many(self, dtos: List[CreateArticleDTO]):
        async with self._session_factory() as session:
            await self.repository.add_many(session, dtos)

    async def get_by_id(self, id: int) -> ArticleDTO | None:
        async with self._session_factory() as session:
            result = await self.repository.get_by_id(session, id)
            return await from_model(result) if result is not None else None

    async def filter_by_url(self, urls: Iterable[str]) -> List[ArticleDTO]:
        async with self._session_factory() as session:
            return await model_list_to_dto_list(
                self.organizer_service,
                await self.repository.filter_by_urls(session, urls),
            )
