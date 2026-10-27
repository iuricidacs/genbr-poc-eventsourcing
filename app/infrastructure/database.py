from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


# Exemplo de banco PostgreSQL (ou mude para seu banco de preferência)
DATABASE_URL = "postgresql+asyncpg://postgres:genbrdb123@192.168.100.175:5432/individualdb"

# 1. Customizar parâmetros do Engine (opcional)
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=1800,

)

SessionLocal = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False  # Exemplo de parâmetro customizado
    )
)