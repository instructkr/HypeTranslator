from dependency_injector import containers, providers

from .repository import ArticleRepository
from .service import ArticleService

class ArticleContainer(containers.DeclarativeContainer):
    database = providers.Dependency()

    repository = providers.Factory(
        ArticleRepository,
        session_factory=database.provided.session,
    )

    service = providers.Factory(
        ArticleService,
        repository=repository,
    )
