from datetime import datetime
from dependency_injector import containers, providers
from twikit import asyncio

from backend.article.dto import CreateArticleDTO

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
        database=database,
        article=article.provided,
        twikit=twikit,
    )

@inject
async def init(
    twikit: Twikit = Provide[AppContainer.twikit],
    article: ArticleContainer = Provide[AppContainer.article],
    database: Database = Provide[AppContainer.database],
) -> None:
    await database.create_database()
    await twikit.login()
    print(await twikit.client.get_latest_timeline())
    # await article.service().create_article(
    #     CreateArticleDTO(
    #         title=None,
    #         content="test",
    #         url="https://www.google.com",
    #         author="test",
    #         published_at=datetime.now(),
    #     )
    # )

@inject 
async def test_collect_articles(
    collect_article: CollectArticleContainer = Provide[AppContainer.collectArticle],
) -> None:
    service = collect_article.service()
    articles = await service.collect_articles_by_keyword("Donald Trump", 3)
    print(f"수집된 기사 수: {len(articles)}")

if __name__ == '__main__':
    container = AppContainer()
    container.init_resources()
    container.wire(modules=[__name__])
    
    # Combine both async operations into a single coroutine
    async def main():
        await init()
        await test_collect_articles()
    
    # Run everything in a single asyncio.run() call
    asyncio.run(main())
