# test_user_api.py
import pytest
from httpx import AsyncClient
from app.main import app
test_id_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjZjZTExYWVjZjllYjE0MDI0YTQ0YmJmZDFiY2Y4YjMyYTEyMjg3ZmEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI4NzMzNjU1MTIwNzktZmRzYjV0aDhmdTJkYXZyODJhY3Zha3FrOGE5NDlyc2YuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI4NzMzNjU1MTIwNzktZmRzYjV0aDhmdTJkYXZyODJhY3Zha3FrOGE5NDlyc2YuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTE3ODM4MDE5ODU3MzIyODY2MDEiLCJlbWFpbCI6ImNsYWlyZTMyMjQ2MjIzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiQlhOZ19CN0NTQ1FWeG1EYS1TeXppQSIsIm5hbWUiOiJDbGFpcmUiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSUNya3kzTUlMcC1HUElQejlRQlJBN2xYdUk4ei01bzNLVTR0dF9Xby0tY2NZX0pFOC1PUT1zOTYtYyIsImdpdmVuX25hbWUiOiJDbGFpcmUiLCJpYXQiOjE3MTM0NTcwMDIsImV4cCI6MTcxMzQ2MDYwMn0.fWuwIOYENNNrZgDljRCbQrdS1e4gjVeD4cVsZCy9j8CCvf0CXVCBBQAOkQoihTGvpcrWAgaJo6zNhKaJcn1-J2mfc3r4mQj6VVffmFTl3zaS3kX3YiwfciiRWBvs2vWL7EtfKHjb4GIdS6RIslsjCg3QiAnRuH4bS534OOPQSt0QmBE3Qvge2BuNaPkcirCNxUOr7DqGKufo-ZFIOYBKZbADjkhxga5feetTyRbEKCQW7aWCwejI5b9Zk2iEQBR_frkld7H5u2YDflZn8f5JWngCik7Q9sfB0eEbZ7nLTT5LB4FG9nHYqBlk4IN2n1v0Wb6pLgETtFnBWEjCOQtJ5A"
headers = {"Authorization": f"Bearer {test_id_token}"}
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://localhost:8080") as ac:
        yield ac

@pytest.mark.anyio
async def test_login(client):
    response = await client.post("/api/v1/users/login", json={"idToken": test_id_token})
    assert response.status_code == 200
    assert "userId" in response.json()

@pytest.mark.anyio
async def test_update_user(client):
    response = await client.put("/api/v1/users/1", json={"name": "New Name", "email": "newemail@example.com"}, headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "User 1 updated successfully"
    }

@pytest.mark.anyio
async def test_upload_avatar(client):
    files = {'avatar': ('filename.jpg', b'this is test data', 'image/jpeg')}
    response = await client.post("/api/v1/users/avatar", files=files)
    assert response.status_code == 200
    assert "avatarUrl" in response.json()

@pytest.mark.anyio
async def test_follow_user(client):
    response = await client.post("/api/v1/users/1/follow", headers=headers)
    assert response.status_code == 201

@pytest.mark.anyio
async def test_unfollow_user(client):
    response = await client.delete("/api/v1/users/1/follow", headers=headers)
    assert response.status_code == 200

@pytest.mark.anyio
async def test_get_user_detail(client):
    response = await client.get("/api/v1/users/1")
    assert response.status_code == 200
    assert response.json()['id'] == 1

@pytest.mark.anyio
async def test_get_user_detail(client):
    response = await client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_user_diaries(client):
    response = await client.get("/api/v1/users/1/diaries")
    assert response.status_code == 200
    assert isinstance(response.json(), list)