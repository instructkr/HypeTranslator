from dependency_injector import containers, providers

from .service import CollectArticleService


class CollectArticleContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[".fastapi"],
        auto_wire=False,
    )

    database = providers.Dependency()
    article = providers.DependenciesContainer()
    trackers = providers.Dependency()

    service = providers.Factory(
        CollectArticleService,
        article_service=article.provided.service,
        trackers=trackers,
    )
