import json
import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport

from core.database import Base, engine, async_session_maker, env
from core.models.models import User
from sqlalchemy import insert
from core.main import app as fastapi_app


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    assert env("MODE") == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"core/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")

    async with async_session_maker() as session:
        insert_users = insert(User).values(users)
        await session.execute(insert_users)
        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac


