from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from starlette.testclient import TestClient

from app.db.config import get_session, engine
from app.main import app


client = TestClient(app)
# start SQL lite db before tests
def setup_module(module):
    SQLModel.metadata.create_all(engine)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_user_registration():
    with Session(engine) as session:
        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        response = client.post("/api/users/register", json={"username": "test_user", "password": "test_password", "email": "test@test.com"})
        assert response.status_code == 200
        assert response.json()['username'] == "test_user"

