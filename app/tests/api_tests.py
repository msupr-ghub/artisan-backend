from sqlmodel import SQLModel, Session
from starlette.testclient import TestClient

from app.db.config import get_session, engine
from app.main import app


client = TestClient(app)

def setup_module():
    # setup DB tables before running tests
    SQLModel.metadata.create_all(engine)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_user_registration():

    response = client.post("/api/users/register", json={"username": "test_user", "password": "test_password", "email": "test@test.com"})
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

