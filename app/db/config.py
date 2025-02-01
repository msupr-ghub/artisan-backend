from contextlib import contextmanager

from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "postgresql://:@localhost:5432/artisan"
engine = create_engine(DATABASE_URL, echo=True)

@contextmanager
def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


