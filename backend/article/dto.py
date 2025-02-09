from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class CreateArticleDTO:
    url: str
    author: str
    published_at: datetime

@dataclass(frozen=True)
class ArticleDTO:
    article_id: int
    url: str
    author: str
    published_at: datetime
