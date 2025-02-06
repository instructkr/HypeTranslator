from datetime import datetime
from dependency_injector import containers, providers
from twikit import asyncio

# Gateways Classes
from .database import Database
from .twikit import Twikit

# Containers Classes
from .article.container import ArticleContainer
from .collect_article.container import CollectArticleContainer

# for testing
from dependency_injector.wiring import inject, Provide

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
def test(
    twikit: Twikit = Provide[AppContainer.twikit],
) -> None:
    asyncio.new_event_loop()
    print(asyncio.run(twikit.client.get_latest_timeline()))

if __name__ == '__main__':
    container = AppContainer()
    container.init_resources()
    container.wire(modules=[__name__])
    container.database().create_database()
    test()
