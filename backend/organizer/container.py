from dependency_injector import containers, providers

from .repository import OrganizerRepository
from .service import OrganizerService


class OrganizerContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[".fastapi"],
        auto_wire=False,
    )

    database = providers.Dependency()

    repository = providers.Factory(
        OrganizerRepository,
    )

    service = providers.Factory(
        OrganizerService,
        session_factory=database.provided.session,
        repository=repository,
    )
