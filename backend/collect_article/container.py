from dependency_injector import containers, providers


class CollectArticleContainer(containers.DeclarativeContainer):
    database = providers.Dependency()
    article = providers.Dependency()
