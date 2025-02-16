from typing import List, Sequence, Iterable, Set
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models import ArticleModel
from ..organizer.repository import OrganizerRepository
from .dto import CreateArticleDTO


class ArticleRepository:
    def __init__(self, organizer_repository: OrganizerRepository):
        self.organizer_repository = organizer_repository

    async def get_by_id(
        self, session: AsyncSession, article_id: int
    ) -> ArticleModel | None:
        return await session.get(ArticleModel, article_id)

    async def filter_by_urls(
        self, session: AsyncSession, urls: Iterable[str]
    ) -> Sequence[ArticleModel]:
        query = select(ArticleModel).filter(ArticleModel.url.in_(urls))
        result = await session.execute(query)
        return result.scalars().all()

    async def add(self, session: AsyncSession, dto: CreateArticleDTO) -> ArticleModel:
        article = ArticleModel(
            **{
                key: value
                for key, value in dto.__dict__.items()
                if key != "related_to_organizer"
            }
        )

        if dto.related_to_organizer is not None:
            org = await self.organizer_repository.get_by_id(
                session,
                dto.related_to_organizer.organizer_id,
            )
            if org is not None:
                article.related_to_organizer_id = org.organizer_id
                article.related_to_organizer = org

        session.add(article)
        await session.flush()
        return article

    async def add_many(
        self, session: AsyncSession, dtos: Iterable[CreateArticleDTO]
    ) -> Sequence[ArticleModel]:
        organizer_ids: Set[int] = set()
        for dto in dtos:
            if dto.related_to_organizer is not None:
                organizer_ids.add(dto.related_to_organizer.organizer_id)

        organizers_by_id = {
            org.organizer_id: org
            for org in await self.organizer_repository.filter_by_ids(
                session, organizer_ids
            )
        }

        articles: List[ArticleModel] = []
        for dto in dtos:
            article = ArticleModel(
                **{
                    key: value
                    for key, value in dto.__dict__.items()
                    if key != "related_to_organizer"
                }
            )
            if dto.related_to_organizer is not None:
                org = organizers_by_id.get(dto.related_to_organizer.organizer_id)
                if org is not None:
                    article.related_to_organizer_id = org.organizer_id
                    article.related_to_organizer = org

            articles.append(article)

        session.add_all(articles)
        return articles
