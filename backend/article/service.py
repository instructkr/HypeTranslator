from typing import List
from .repository import ArticleRepository
from .model import Article
from .dto import CreateArticleDTO

class ArticleService:
    def __init__(self, repository: ArticleRepository):
        self.repository = repository

    async def create_article(self, dto: CreateArticleDTO) -> Article:
        return await self.repository.add(
                dto.url,
                dto.title,
                dto.author,
                dto.content,
                dto.published_at)

    async def get_article(self, id: int) -> Article:
        return await self.repository.get_by_id(id)

    async def filter_by_url(self, urls: List[str]) -> List[Article]:
        return await self.repository.filter_by_urls(urls)
