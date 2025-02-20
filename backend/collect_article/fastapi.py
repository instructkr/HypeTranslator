from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from .container import CollectArticleContainer
from .service import CollectArticleService

router = APIRouter(prefix="/collect_article", tags=["collect_article"])


@router.get("/collect")
@inject
async def collect(
    service: CollectArticleService = Depends(Provide[CollectArticleContainer.service]),
):
    return await service.collect()
