from datetime import datetime
from dependency_injector import containers, providers
from twikit import asyncio

# Gateways Classes
from .database import Database
from .twikit import Twikit

# Containers Classes
from .article.container import ArticleContainer
from .collect_article.container import CollectArticleContainer

# for initializing
from dependency_injector.wiring import inject, Provide

# for testing
from backend.article.dto import CreateArticleDTO

class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=['config.yaml'])

    # Gateways
    database = providers.Singleton(
        Database,
        connection_url=config.db.connection_url,
    )

    twikit = providers.Singleton(
        Twikit,
        id=config.twikit.id,
        email=config.twikit.email,
        password=config.twikit.pw,
    )

    # Containers
    article = providers.Container(
        ArticleContainer,
        database=database,
    )

    collectArticle = providers.Container(
        CollectArticleContainer,
        article=article.provided,
    )

@inject
async def init(
    twikit: Twikit = Provide[AppContainer.twikit],
    database: Database = Provide[AppContainer.database],
) -> None:
    db = database.create_database()
    login = twikit.login()
    await asyncio.gather(db, login)

@inject
async def test(
    article: ArticleContainer = Provide[AppContainer.article],
) -> None:
    await article.service().create_article(
        CreateArticleDTO(
            url="https://www.google.com",
            author="test",
            published_at=datetime.now(),
        )
    )

    print(list(await article.service().filter_by_url(["https://www.google.com"])))

async def main():
    await init()
    await test()

if __name__ == '__main__':
    container = AppContainer()
    container.init_resources()
    container.wire(modules=[__name__])
    asyncio.run(main())
