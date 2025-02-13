from typing import Any, Dict, List
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import DateTime, Integer, String, ForeignKey


class Base(AsyncAttrs, MappedAsDataclass, DeclarativeBase):
    def to_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class OrganizerModel(Base):
    __tablename__ = "organizers"

    organizer_id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String)
    articles: Mapped[List["ArticleModel"]] = relationship(
        back_populates="related_to_organizer"
    )


class ArticleModel(Base):
    __tablename__ = "articles"
    article_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        init=False,
    )
    url: Mapped[str] = mapped_column(String, unique=True)
    author: Mapped[str]
    published_at: Mapped[datetime] = mapped_column(DateTime)
    related_to_organizer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("organizers.organizer_id"),
        default=None,
        nullable=True,
    )
    related_to_organizer: Mapped["OrganizerModel"] = relationship(
        back_populates="articles",
        default=None,
    )
