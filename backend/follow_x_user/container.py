from dependency_injector import containers, providers

from .repository import FollowXUserRepository
from .service import FollowXUserService
from .tracker import FollowXUserTracker


class FollowXUserContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[".fastapi"],
        auto_wire=False,
    )

    twikit = providers.Dependency()
    database = providers.Dependency()
    organizer = providers.DependenciesContainer()

    repository = providers.Factory(
        FollowXUserRepository,
        twikitClient=twikit.provided.client,
        organizer_repository=organizer.repository.provided,
    )

    service = providers.Factory(
        FollowXUserService,
        session_factory=database.provided.session,
        repository=repository,
        organizer_repository=organizer.repository.provided,
    )

    tracker = providers.Factory(
        FollowXUserTracker,
        twikitClient=twikit.provided.client,
        service=service,
    )
