from uuid import uuid4

from app.domain.individual import Individual


def test_individual_creation():
    individual_id = uuid4()

    individual = Individual(
        id=individual_id,
        name="Maria Silva",
    )

    assert individual.id == individual_id
    assert individual.name == "Maria Silva"