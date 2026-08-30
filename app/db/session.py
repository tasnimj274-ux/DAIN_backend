from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True, echo=settings.debug)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """Yield one database session per request; routes will use this in later stages."""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def check_database_connection() -> None:
    """Raise an error if PostgreSQL cannot answer a minimal query."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
