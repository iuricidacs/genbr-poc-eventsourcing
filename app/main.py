import os
import uvicorn
from contextlib import asynccontextmanager
from uuid import UUID
from eventsourcing.utils import get_topic
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field

from app.infrastructure.database import SessionLocal

from app.infrastructure.models.individual import Individual

# Configurar antes de instanciar a aplicação de Event Sourcing.
os.environ.setdefault(
    "PERSISTENCE_MODULE",
    "eventsourcing_sqlalchemy",
)

os.environ.setdefault(
    "SQLALCHEMY_URL",
    "postgresql+psycopg://postgres:genbrdb123@192.168.100.175:5432/individualdb",
)

from eventsourcing.application import AggregateNotFoundError

from app.application.individuals import Individual


class CreateIndividualRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class IndividualResponse(BaseModel):
    id: UUID
    name: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.individuals = Individual()
    yield


api = FastAPI(
    title="Individual API",
    version="1.0.0",
    lifespan=lifespan,
)


@api.post(
    "/individuals",
    response_model=IndividualResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_individual(
    request: CreateIndividualRequest,
) -> IndividualResponse:

    application: Individual = api.state.individuals
    #session: Session = api.state.session
    #with application.recorder.transaction() as session:

    individual = await application.create_individual(
        name=request.name,
    )

    return IndividualResponse(
        id=individual.id,
        name=individual.name,
    )


@api.get(
    "/individuals/{individual_id}",
    response_model=IndividualResponse,
)
def get_individual(individual_id: UUID) -> IndividualResponse:
    application = api.state.individuals

    try:
        individual = application.get_individual(individual_id)
    except AggregateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Individual não encontrado",
        )

    return IndividualResponse(
        id=individual.id,
        name=individual.name,
    )

@api.put(
    "/individuals/{individual_id}",
    response_model=IndividualResponse,
)
def get_individual(individual_id: UUID, name: str) -> IndividualResponse:
    application = api.state.individuals

    try:
        individual = application.set_individual(individual_id)
    except AggregateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Individual não encontrado",
        )

    return IndividualResponse(
        id=individual.id,
        name=individual.name,
    )

if __name__ == "__main__":
    uvicorn.run(api, host="127.0.0.1", port=5000)