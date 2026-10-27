from uuid import UUID

from eventsourcing.domain import Aggregate, event


class Individual(Aggregate):

    _name: str

    @event("Created")
    def __init__(self, id: UUID, name: str):
        self._name = name


    @property
    def name(self) -> str:
        return self._name

    @name.setter
    @event("NameChanged")
    def name(self, value: str) -> None:
        self._name = value