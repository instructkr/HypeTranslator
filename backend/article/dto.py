from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, List

from sqlalchemy.ext.asyncio import AsyncSession


from ..models import ArticleModel, OrganizerModel
from ..organizer.dto import OrganizerDTO, from_model as organizer_from_model
from ..organizer.repository import OrganizerRepository


@dataclass(frozen=True)
class CreateArticleDTO:
    url: str
    author: str
    published_at: datetime
    related_to_organizer: OrganizerDTO | None
    title: str | None = field(default=None)
    content: str | None = field(default=None)


@dataclass(frozen=True)
class ArticleDTO:
    article_id: int
    url: str
    author: str
    published_at: datetime
    related_to_organizer: OrganizerDTO | None = field(default=None)
    title: str | None = field(default=None)
    content: str | None = field(default=None)


async def from_model(model: ArticleModel) -> ArticleDTO:
    """
    Converts an ArticleModel instance to an ArticleDTO instance.
    Do not use this function outside of session context.
    """
    related_to_organizer: OrganizerModel = (
        await model.awaitable_attrs.related_to_organizer
    )
    return ArticleDTO(
        **{
            k: v
            for k, v in model.to_dict().items()
            if k not in {"related_to_organizer"}
        },
        related_to_organizer=organizer_from_model(related_to_organizer),
    )


async def model_list_to_dto_list(
    session: AsyncSession,
    organizerRepository: OrganizerRepository,
    models: Iterable[ArticleModel],
) -> List[ArticleDTO]:
    """
    Converts a list of ArticleModel instances to a list of ArticleDTO instances.
    Do not use this function outside of session context.

    First, should get all related organizers by their ids.
    Because, when use another session opened by another service, it will expired the current session.
    So, it raises an error when try to access article's attributes.
    """
    articles_with_org_id = [
        (
            ArticleDTO(
                **{
                    k: v
                    for k, v in model.to_dict().items()
                    if k not in {"related_to_organizer", "related_to_organizer_id"}
                }
            ),
            model.related_to_organizer_id,
        )
        for model in models
    ]

    organizer_ids = set(map(lambda model: model.related_to_organizer_id, models))
    organizer_by_id = {
        organizer.organizer_id: organizer
        for organizer in await organizerRepository.filter_by_ids(session, organizer_ids)
    }
    return [
        ArticleDTO(
            **{
                k: v
                for k, v in article.__dict__.items()
                if k not in {"related_to_organizer"}
            },
            related_to_organizer=organizer_from_model(organizer_by_id[org_id]),
        )
        for (article, org_id) in articles_with_org_id
    ]
