from typing import List
from .repository import ArticleRepository
from .model import Article
from .dto import CreateArticleDTO

class ArticleService:
    def __init__(self, repository: ArticleRepository):
        self.repository = repository

    def create_article(self, dto: CreateArticleDTO) -> Article:
        return self.repository.add(
                dto.url,
                dto.title,
                dto.author,
                dto.content,
                dto.published_at)

    def get_article(self, id: int) -> Article:
        return self.repository.get_by_id(id)

    def filter_by_url(self, urls: List[str]) -> List[Article]:
        return self.repository.filter_by_urls(urls)
