from dependency_injector import containers, providers
from .service import CollectArticleService
class CollectArticleContainer(containers.DeclarativeContainer):
    database = providers.Dependency()
    article = providers.Dependency()
    twikit = providers.Dependency()

    service = providers.Factory(CollectArticleService, 
                                twikit=twikit, 
                                article=article,
                                database=database,)
