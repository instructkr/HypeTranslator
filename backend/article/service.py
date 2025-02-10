from typing import List, Callable
from contextlib import AbstractAsyncContextManager
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import ArticleRepository
from .dto import ArticleDTO, CreateArticleDTO, from_model

class ArticleService:
    def __init__(self,
                 session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
                 repository: ArticleRepository):
        self.repository = repository
        self._session_factory = session_factory

    async def create(self, dto: CreateArticleDTO) -> ArticleDTO:
        async with self._session_factory() as session:
            return await from_model(await self.repository.add(session, dto))

    async def get_by_id(self, id: int) -> ArticleDTO | None:
        async with self._session_factory() as session:
            result = await self.repository.get_by_id(session, id)
            return await from_model(result) if result is not None else None

    async def filter_by_url(self, urls: List[str]) -> List[ArticleDTO]:
        async with self._session_factory() as session:
            return await asyncio.gather(*map(
                from_model,
                await self.repository.filter_by_urls(session, urls)
            ))
