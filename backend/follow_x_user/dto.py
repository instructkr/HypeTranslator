from dataclasses import dataclass
from typing import List, Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import FollowXUserModel
from ..organizer.repository import OrganizerRepository
from ..organizer.dto import OrganizerDTO, from_model as OrganizerDTO_from_model


@dataclass
class FollowXUserDTO:
    follow_x_user_id: int
    real_x_user_id: str
    username: str
    organizer: OrganizerDTO


@dataclass
class NewFollowXUserDTO:
    username: str
    organizer: OrganizerDTO


async def from_model(model: FollowXUserModel) -> FollowXUserDTO:
    await model.awaitable_attrs.related_to_organizer
    return FollowXUserDTO(
        **{
            k: v
            for k, v in model.to_dict().items()
            if k not in {"related_to_organizer"}
        },
        organizer=OrganizerDTO_from_model(model.related_to_organizer),
    )


async def dto_list_from_models(
    session: AsyncSession,
    organizer_repository: OrganizerRepository,
    models: Iterable[FollowXUserModel],
) -> List[FollowXUserDTO]:
    organizer_ids = set([model.related_to_organizer_id for model in models])

    dto_list = [
        {k: v for k, v in model.to_dict().items() if k not in {"related_to_organizer"}}
        for model in models
    ]

    organizer_by_id = {
        org.organizer_id: org
        for org in await organizer_repository.filter_by_ids(session, organizer_ids)
    }

    return list(
        map(
            lambda d: FollowXUserDTO(
                **{k: v for k, v in d.items() if k not in {"related_to_organizer_id"}},
                organizer=OrganizerDTO_from_model(
                    organizer_by_id[d["related_to_organizer_id"]]
                ),
            ),
            dto_list,
        )
    )
