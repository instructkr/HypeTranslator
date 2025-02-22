from contextlib import AbstractAsyncContextManager
from typing import Iterable, Callable, List

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import FollowXUserRepository
from .dto import FollowXUserDTO, NewFollowXUserDTO, dto_list_from_models
from ..organizer.repository import OrganizerRepository


class FollowXUserService:
    def __init__(
        self,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
        repository: FollowXUserRepository,
        organizer_repository: OrganizerRepository,
    ):
        self._session = session_factory
        self._repository = repository
        self._organizer_repository = organizer_repository

    async def new_follow_x_users(
        self, new_follow_x_users: Iterable[NewFollowXUserDTO]
    ) -> List[FollowXUserDTO]:
        async with self._session() as session:
            return await dto_list_from_models(
                session,
                self._organizer_repository,
                await self._repository.new_follow_x_users(session, new_follow_x_users),
            )

    async def get_all_followed_x_users(self) -> List[FollowXUserDTO]:
        async with self._session() as session:
            return await dto_list_from_models(
                session,
                self._organizer_repository,
                await self._repository.get_all_followed_x_users(session),
            )
