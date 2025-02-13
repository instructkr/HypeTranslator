from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, List


from ..models import ArticleModel, OrganizerModel
from ..organizer.dto import OrganizerDTO, from_model as organizer_from_model
from ..organizer.service import OrganizerService


@dataclass(frozen=True)
class CreateArticleDTO:
    url: str
    author: str
    published_at: datetime
    related_to_organizer: OrganizerDTO | None


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


async def model_list_to_dto_list(
    organizerService: OrganizerService, models: Iterable[ArticleModel]
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
                article_id=model.article_id,
                url=model.url,
                author=model.author,
                published_at=model.published_at,
            ),
            model.related_to_organizer_id,
        )
        for model in models
    ]

    organizer_ids = set(map(lambda model: model.related_to_organizer_id, models))
    organizer_by_id = {
        organizer.organizer_id: organizer
        for organizer in await organizerService.filter_by_ids(organizer_ids)
    }
    return [
        ArticleDTO(
            article_id=article.article_id,
            url=article.url,
            author=article.author,
            published_at=article.published_at,
            related_to_organizer=organizer_by_id.get(org_id),
        )
        for (article, org_id) in articles_with_org_id
    ]
