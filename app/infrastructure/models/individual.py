from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()

class Individual(Base):

    __tablename__ = "individual"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(primary_key=True)

