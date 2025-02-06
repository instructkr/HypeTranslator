from datetime import datetime
from dependency_injector.wiring import inject, Provide
from dependency_injector import containers, providers

from .database import Database

from .article.container import ArticleContainer
from .collect_article.container import CollectArticleContainer

from .article.service import ArticleService
from .article.dto import CreateArticleDTO

class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=['config.yaml'])

    # Gateways
    database = providers.Singleton(
        Database,
        connection_url=config.db.connection_url,
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
        service: ArticleService = Provide[AppContainer.article.service],
) -> None:
    service.create_article(
        CreateArticleDTO(
            url='https://example.com/1',
            title='Example',
            author='Author',
            content='Content',
            published_at=datetime.now(),
        )
    )

if __name__ == '__main__':
    container = AppContainer()
    container.init_resources()
    container.wire(modules=[__name__])
    container.database().create_database()
    test()
