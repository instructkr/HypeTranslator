from dependency_injector import containers, providers

from .repository import ArticleRepository
from .service import ArticleService


class ArticleContainer(containers.DeclarativeContainer):
    database = providers.Dependency()
    organizer = providers.DependenciesContainer()

    repository = providers.Factory(
        ArticleRepository,
        organizer_repository=organizer.repository.provided,
    )

    service = providers.Factory(
        ArticleService,
        session_factory=database.provided.session,
        repository=repository,
        organizer_repository=organizer.repository.provided,
    )
