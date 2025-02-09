from typing import List
from .repository import ArticleRepository
from .model import Article
from .dto import CreateArticleDTO, SearchArticleDTO

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
    
    async def save_search_article(self, dto: SearchArticleDTO) -> Article:
        # URLs가 있는 경우 첫 번째 URL 사용
        url = dto.urls[0] if dto.urls else None
        # breakpoint()
        return await self.repository.add(
            url=url,
            title=dto.content[:10],  # 임시로 content의 첫 100자를 title로 사용
            author=dto.author,
            content=dto.content,
            published_at=dto.published_at,
        )
