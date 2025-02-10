from dataclasses import dataclass, field
from datetime import datetime


from ..models import ArticleModel, OrganizerModel
from ..organizer.dto import OrganizerDTO, from_model as organizer_from_model


@dataclass(frozen=True)
class CreateArticleDTO:
    url: str
    author: str
    published_at: datetime
    related_to_organizer: OrganizerDTO | int | None


@dataclass(frozen=True)
class ArticleDTO:
    article_id: int
    url: str
    author: str
    published_at: datetime
    related_to_organizer: OrganizerDTO | None = field(default=None)


async def from_model(model: ArticleModel) -> ArticleDTO:
    """
    Converts an ArticleModel instance to an ArticleDTO instance.
    Do not use this function outside of session context.
    """
    related_to_organizer: OrganizerModel = (
        await model.awaitable_attrs.related_to_organizer
    )
    return ArticleDTO(
        article_id=model.article_id,
        url=model.url,
        author=model.author,
        published_at=model.published_at,
        related_to_organizer=organizer_from_model(related_to_organizer)
        if related_to_organizer
        else None,
    )
