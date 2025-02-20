import random
from collections.abc import Iterable
from typing import Callable, List, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from twikit import Client as TwikitClient, User as TwikitUser
from ..twikit import action_delay

from .dto import NewFollowXUserDTO
from ..organizer.repository import OrganizerRepository
from ..models import FollowXUserModel


class FollowXUserRepository:
    def __init__(
        self,
        organizer_repository: Callable[..., OrganizerRepository],
        twikitClient: TwikitClient,
    ):
        self._organizer_repository = organizer_repository()
        self._twikitClient = twikitClient

    async def _get_x_user_by_screen_name(self, username: str) -> TwikitUser:
        user = await self._twikitClient.get_user_by_screen_name(username)
        await action_delay()
        return user

    async def new_follow_x_users(
        self, session: AsyncSession, new_follow_x_users: Iterable[NewFollowXUserDTO]
    ) -> List[FollowXUserModel]:
        organizers = await self._organizer_repository.filter_by_ids(
            session, set(map(lambda x: x.organizer.organizer_id, new_follow_x_users))
        )
        organizer_by_id = {org.organizer_id: org for org in organizers}

        result: List[FollowXUserModel] = []
        # Shuffle the list to avoid following users in the same order
        new_follow_x_users = list(new_follow_x_users)
        random.shuffle(new_follow_x_users)
        for new_follow_x_user in new_follow_x_users:
            x_user = await self._get_x_user_by_screen_name(new_follow_x_user.username)
            followXUser = FollowXUserModel(
                username=new_follow_x_user.username,
                real_x_user_id=x_user.id,
                related_to_organizer_id=new_follow_x_user.organizer.organizer_id,
                related_to_organizer=organizer_by_id[
                    new_follow_x_user.organizer.organizer_id
                ],
            )

            result.append(followXUser)

        session.add_all(result)
        await session.flush()

        return result

    async def get_all_followed_x_users(
        self, session: AsyncSession
    ) -> Sequence[FollowXUserModel]:
        result = await session.execute(select(FollowXUserModel))
        return result.scalars().all()
