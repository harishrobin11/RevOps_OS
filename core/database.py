import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import config

# Ensure data directory exists
os.makedirs(config.DATA_DIR, exist_ok=True)

# Create SQLAlchemy engine
engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},  # Required for SQLite in multi-thread / Streamlit
    echo=False
)

# Create SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative Base
Base = declarative_base()


@contextmanager
def get_db():
    """
    Context manager for database sessions.
    Ensures sessions are cleanly opened, committed, rolled back on error, and closed.
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    """
    Initialize database schema by creating all tables.
    Import models first so metadata is populated.
    """
    from core.models import Lead, Qualification, Activity, Outreach, Pipeline, Note  # noqa: F401
    Base.metadata.create_all(bind=engine)
