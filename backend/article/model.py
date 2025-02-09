from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base

class ArticleModel(Base):
    __tablename__ = "articles"

    article_id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String, unique=True)
    author: Mapped[str]
    published_at: Mapped[datetime] = mapped_column(DateTime)
