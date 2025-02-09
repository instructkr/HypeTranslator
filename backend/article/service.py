from typing import List, Iterable
from .repository import ArticleRepository
from .dto import ArticleDTO, CreateArticleDTO

class ArticleService:
    def __init__(self, repository: ArticleRepository):
        self.repository = repository

    async def create_article(self, dto: CreateArticleDTO) -> ArticleDTO:
        return await self.repository.add(dto)

    async def get_article(self, id: int) -> ArticleDTO | None:
        return await self.repository.get_by_id(id)

    async def filter_by_url(self, urls: List[str]) -> Iterable[ArticleDTO]:
        return await self.repository.filter_by_urls(urls)
