from contextlib import AbstractAsyncContextManager
from datetime import datetime
from typing import Callable, List, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .model import Article

class ArticleRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def get_by_id(self, article_id: int) -> Article | None:
        async with self.session_factory() as session:
            return await session.get(Article, article_id)

    async def filter_by_urls(self, urls: List[str]) -> Sequence[Article]:
        async with self.session_factory() as session:
            query = select(Article).filter(Article.url.in_(urls))
            result = await session.execute(query)
            return result.scalars().all()

    async def add(self, url: str, title: str | None, author: str, content: str, published_at: datetime) -> Article:
        article = Article(url=url, title=title, author=author, content=content, published_at=published_at)
        async with self.session_factory() as session:
            session.add(article)
            await session.commit()
            return article
