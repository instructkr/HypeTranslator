from dataclasses import dataclass
from typing import List, Iterable, Callable

from ..models import FollowXUserModel
from ..organizer.service import OrganizerService
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
        follow_x_user_id=model.follow_x_user_id,
        username=model.username,
        real_x_user_id=model.real_x_user_id,
        organizer=OrganizerDTO_from_model(model.related_to_organizer),
    )


async def dto_list_from_models(
    organizer_service: Callable[..., OrganizerService],
    models: Iterable[FollowXUserModel],
) -> List[FollowXUserDTO]:
    organizer_ids = [model.related_to_organizer.organizer_id for model in models]

    dto_list = [
        {
            "follow_x_user_id": model.follow_x_user_id,
            "username": model.username,
            "real_x_user_id": model.real_x_user_id,
            "organizer_id": model.related_to_organizer.organizer_id,
        }
        for model in models
    ]

    organizer_by_id = {
        org.organizer_id: org
        for org in await organizer_service().filter_by_ids(organizer_ids)
    }

    return list(
        map(
            lambda d: FollowXUserDTO(
                follow_x_user_id=d["follow_x_user_id"],
                username=d["username"],
                real_x_user_id=d["real_x_user_id"],
                organizer=organizer_by_id[d["organizer_id"]],
            ),
            dto_list,
        )
    )
