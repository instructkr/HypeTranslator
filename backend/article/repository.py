from contextlib import AbstractAsyncContextManager
from typing import Callable, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .model import ArticleModel
from .dto import ArticleDTO, CreateArticleDTO

class ArticleRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def get_by_id(self, article_id: int) -> ArticleDTO | None:
        async with self.session_factory() as session:
            article = await session.get(ArticleModel, article_id)
            if article is None:
                return None
            return ArticleDTO(**article.to_dict())

    async def filter_by_urls(self, urls: List[str]) -> List[ArticleDTO]:
        async with self.session_factory() as session:
            query = select(ArticleModel).filter(ArticleModel.url.in_(urls))
            result = await session.execute(query)
            articles = result.scalars().all()
            return list(map(lambda a: ArticleDTO(**a.to_dict()), articles))

    async def add(self, dto: CreateArticleDTO) -> ArticleDTO:
        article = ArticleModel(**dto.__dict__)
        async with self.session_factory() as session:
            session.add(article)
            await session.commit()
            await session.refresh(article)
            return ArticleDTO(**article.to_dict())
