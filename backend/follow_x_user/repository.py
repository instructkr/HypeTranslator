import asyncio
import random
from collections.abc import Iterable
from typing import Callable, List
from sqlalchemy.ext.asyncio import AsyncSession
from twikit import Client as TwikitClient, User as TwikitUser

from .dto import NewFollowXUserDTO
from ..organizer.repository import OrganizerRepository
from ..models import FollowXUserModel


async def action_delay():
    await asyncio.sleep(15 + random.uniform(-5, 15))


class FollowXUserRepository:
    def __init__(
        self,
        organizer_repository: Callable[..., OrganizerRepository],
        twikitClient: TwikitClient,
    ):
        self._organizer_repository = organizer_repository()
        self._twikitClient = twikitClient

    async def _follow_x_user(self, username: str) -> TwikitUser:
        user = await self._twikitClient.get_user_by_screen_name(username)
        await action_delay()
        result = await self._twikitClient.follow_user(user.id)
        await action_delay()
        return result

    async def new_follow_x_users(
        self, session: AsyncSession, new_follow_x_users: Iterable[NewFollowXUserDTO]
    ) -> List[FollowXUserModel]:
        organizers = await self._organizer_repository.filter_by_ids(
            session, set(map(lambda x: x.organizer.organizer_id, new_follow_x_users))
        )
        organizer_by_id = {org.organizer_id: org for org in organizers}

        result: List[FollowXUserModel] = []
        for new_follow_x_user in new_follow_x_users:
            followXUser = FollowXUserModel(
                username=new_follow_x_user.username,
                related_to_organizer_id=new_follow_x_user.organizer.organizer_id,
                related_to_organizer=organizer_by_id[
                    new_follow_x_user.organizer.organizer_id
                ],
            )

            session.add(followXUser)
            await self._follow_x_user(new_follow_x_user.username)
            await session.flush()
            result.append(followXUser)

        return result
