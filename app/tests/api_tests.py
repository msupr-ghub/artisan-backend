import uuid

from sqlmodel import SQLModel
from starlette.testclient import TestClient

from app.db.config import engine
from app.dependencies import get_user_repository
from app.main import app
from app.models.user import User

client = TestClient(app)


def setup_module():

    # drop any existing db
    SQLModel.metadata.drop_all(engine)

    # setup DB tables before running tests
    SQLModel.metadata.create_all(engine)

    user_repository = next(get_user_repository())
    # create system user, for test we have to do this , for other environments alembic migration will take care of it
    user = User()
    user.id = uuid.UUID("123e4567-e89b-12d3-a456-426614174001")
    user.username = "system"
    user.email = "system@artisan.ai"
    user.hashed_password = "$2a$12$IX2KjWj1v38GVCF8TFBRSe0CZy0o2/5Fkol41.2i.FaSuTk3UcuJG"
    user.is_active = True
    user.is_superuser = False
    user_repository.create(user)

    # create a user for test authentication
    user = User()
    user.username = "test_user"
    user.email = "test@test.com"
    user.hashed_password = "$2a$12$y6VrUyyFcjjOK2c5ef63V.dbZc9xRjr7VROC8owxyGbrH.1UDYVOm"
    user.is_active = True
    user.is_superuser = False
    user_repository.create(user)



def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_user_registration():
    response = client.post("/api/users/register",
                           json={"username": "test_user_1", "password": "test_password", "email": "test_1@test.com"})
    assert response.status_code == 200
    assert response.json()['username'] == "test_user"


def test_user_login():
    response = client.post("/token", data={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200
    assert response.json()['access_token']
    assert response.json()['token_type'] == "bearer"


def test_create_chat():
    # test create chat without login
    response = client.post("/api/chats/", json={"name": "test_chat"})
    assert response.status_code == 401

    response = client.post("/token", data={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200

    client.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    response = client.post("/api/chats/", json={"name": "test_chat"})
    assert response.status_code == 200
    assert response.json()['id'] is not None


def test_send_message():
    response = client.post("/token", data={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200

    client.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    response = client.post("/api/chats/", json={"name": "test_chat"})
    assert response.status_code == 200

    chat_id = response.json()['id']
    response = client.post(f"/api/chats/{chat_id}/messages/", json={"content": "test_message"})
    assert response.status_code == 200
    assert response.json()['response'] is not None


def test_delete_last_user_message():
    response = client.post("/token", data={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200

    client.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    response = client.post("/api/chats/", json={"name": "test_chat"})
    assert response.status_code == 200

    chat_id = response.json()['id']
    response = client.post(f"/api/chats/{chat_id}/messages/", json={"content": "test_message"})
    assert response.status_code == 200

    response = client.post(f"/api/chats/{chat_id}/messages/delete_last_user_message")
    assert response.status_code == 200


def test_update_last_user_message():
    response = client.post("/token", data={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200

    client.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    response = client.post("/api/chats/", json={"name": "test_chat"})
    assert response.status_code == 200

    chat_id = response.json()['id']
    response = client.post(f"/api/chats/{chat_id}/messages/", json={"content": "test_message"})
    assert response.status_code == 200

    previous_response_content = response.json()['response']

    response = client.post(f"/api/chats/{chat_id}/messages/update_last_user_message", json={"content": "test_message"})
    assert response.status_code == 200
    assert response.json()['response'] is not None

    assert response.json()['response'] != previous_response_content
