from collections.abc import Generator
from typing import Any

from sqlalchemy import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from triangler_fastapi import config


def get_engine() -> Engine:
    return create_engine(
        config.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )


_engine = get_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

Base = declarative_base()


def run_migrations() -> None:
    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def get_db_session() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
