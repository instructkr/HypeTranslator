from dataclasses import dataclass

from ..models import OrganizerModel


@dataclass(frozen=True)
class CreateOrganizerDTO:
    name: str


@dataclass(frozen=True)
class OrganizerDTO:
    organizer_id: int
    name: str


def from_model(model: OrganizerModel) -> OrganizerDTO:
    """
    Converts an OrganizerModel instance to an OrganizerDTO instance.
    Do not use this function outside of session context.
    """
    return OrganizerDTO(**{k: v for k, v in model.to_dict().items() if k != "articles"})
