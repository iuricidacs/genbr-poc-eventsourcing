from uuid import UUID, uuid4

from eventsourcing.application import Application

from app.domain.individual import Individual as IndividualAggr

from app.infrastructure.models.individual import Individual as IndividualModel


class Individual(Application):

    async def create_individual(
        self,
        name: str,
        individual_id: UUID | None = None,
    ) -> Individual:
        individual = IndividualAggr(
            id=individual_id or uuid4(),
            name=name,
        )

        with self.recorder.transaction() as session:

            # Save aggregate event
            self.save(individual)

            # Save aggregate projection
            session.add(IndividualModel(id=individual.id, name=individual.name))

            # Save aggregate outbox



        return individual

    def get_individual(self, individual_id: UUID) -> IndividualAggr:
        return self.repository.get(individual_id)

    def set_individual(self, individual_id: UUID, name: str) -> IndividualAggr:
        return self.repository .set (individual_id)
