from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable, List
from sqlalchemy.orm import Session

from .model import Article

class ArticleRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def get_by_id(self, article_id: int) -> Article | None:
        with self.session_factory() as session:
            return session.query(Article).get(article_id)

    def filter_by_urls(self, urls: List[str]) -> List[Article]:
        with self.session_factory() as session:
            return session.query(Article).filter(Article.url.in_(urls)).all()

    def add(self, url: str, title: str | None, author: str, content: str, published_at: datetime) -> Article:
        article = Article(url=url, title=title, author=author, content=content, published_at=published_at)
        with self.session_factory() as session:
            session.add(article)
            session.commit()
            return article
