import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("username, password, status_code", [
    ("test", "$argon2id$v=19$m=65536,t=3,p=4$aY2xtjZmDOH8n7M2ZkwpxQ$JEemfX8E0xy4I91ETU8P0rsNT8bqrVqcNnq97o6UL1U", 201),
    ("test", "$argon2id$v=19$m=65536,t=3,p=4$aY2xtjZmDOH8n7M2ZkwpxQ$JEemfX8E0xy4I91ETU8P0rsNT8bqrVqcNnq97o6UL1U", 409),
    ("this name more than 30 symbol and catch error", "...", 409),

])
async def test_register_user(username, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth-microservice/register-user",
                             json={"username": username,
                                   "password": password})

    assert response.status_code == status_code


@pytest.mark.parametrize("username, password, status_code", [
    (
    "admin2", "$argon2id$v=19$m=65536,t=3,p=4$aY2xtjZmDOH8n7M2ZkwpxQ$JEemfX8E0xy4I91ETU8P0rsNT8bqrVqcNnq97o6UL1U", 201),
    (
    "admin2", "$argon2id$v=19$m=65536,t=3,p=4$aY2xtjZmDOH8n7M2ZkwpxQ$JEemfX8E0xy4I91ETU8P0rsNT8bqrVqcNnq97o6UL1U", 409),
    ("1"*31, "...", 409),

])
async def test_register_superuser(username, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth-microservice/register-super-user",
                             json={"username": username,
                                   "password": password})

    assert response.status_code == status_code


@pytest.mark.parametrize("username, password, status_code", [
    ("admin", "string", 200),
    ("admin", "invalid password", 409),

])
async def test_login_user(username, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth-microservice/login",
                             json={"username": username,
                                   "password": password})
    assert response.status_code == status_code

@pytest.mark.parametrize("token, status_code", [
    ("invalid token",409),
])
async def test_decode_jwt(token,status_code, ac: AsyncClient):
    response = await ac.post("/auth-microservice/decode-jwt",
                             json={"token": token})

    assert response.status_code == status_code
