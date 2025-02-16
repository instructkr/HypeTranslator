from collections.abc import Callable
from typing import List
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from .container import FollowXUserContainer
from .service import FollowXUserService
from .dto import FollowXUserDTO, NewFollowXUserDTO

router = APIRouter(prefix="/follow_x_user", tags=["follow_x_user"])


@router.put("/")
@inject
async def new_follow_x_users(
    new_follow_x_users: List[NewFollowXUserDTO],
    service: FollowXUserService = Depends(Provide[FollowXUserContainer.service]),
) -> List[FollowXUserDTO]:
    return await service.new_follow_x_users(new_follow_x_users)
