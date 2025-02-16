import asyncio
from contextlib import asynccontextmanager
from dependency_injector import containers, providers
from fastapi import FastAPI
import uvicorn

# Gateways Classes
from .database import Database
from .twikit import Twikit

# Containers Classes
from .article.container import ArticleContainer
from .organizer.container import OrganizerContainer
from .follow_x_user.container import FollowXUserContainer
from .collect_article.container import CollectArticleContainer

# for initializing
from dependency_injector.wiring import inject, Provide

# for fastapi routers
from .organizer.fastapi import router as organizer_router
from .follow_x_user.fastapi import router as follow_x_user_router


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yaml"])

    # Gateways
    database = providers.Singleton(
        Database,
        connection_url=config.db.connection_url,
    )

    twikit = providers.Singleton(
        Twikit,
        id=config.twikit.id,
        second_auth=config.twikit.second_auth,
        password=config.twikit.pw,
    )

    # Containers
    organizer = providers.Container(
        OrganizerContainer,
        database=database,
    )

    article = providers.Container(
        ArticleContainer,
        database=database,
        organizer=organizer,
    )

    follow_x_user = providers.Container(
        FollowXUserContainer,
        twikit=twikit,
        database=database,
        organizer=organizer,
    )

    collectArticle = providers.Container(
        CollectArticleContainer,
        database=database,
        article=article,
    )


@inject
async def init(
    twikit: Twikit = Provide[AppContainer.twikit],
    database: Database = Provide[AppContainer.database],
) -> None:
    db = database.create_database()
    login = twikit.login()
    await asyncio.gather(db, login)


container = AppContainer()


@asynccontextmanager
async def fastapi_lifespan(_: FastAPI):
    container.init_resources()
    container.wire(modules=[".app"])
    container.organizer.container.wire()
    container.follow_x_user.container.wire()
    # Initialize Phase
    await init()
    yield


fastapi = FastAPI(lifespan=fastapi_lifespan)
fastapi.include_router(organizer_router)
fastapi.include_router(follow_x_user_router)

if __name__ == "__main__":
    uvicorn.run("backend.app:fastapi", host="0.0.0.0", port=8000, reload=True)
