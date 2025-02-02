from contextlib import contextmanager

from sqlmodel import  Session, create_engine

from app.config_vars import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

@contextmanager
def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


