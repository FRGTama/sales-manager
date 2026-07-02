import os
from typing import AsyncGenerator

import httpx
from httpx import ASGITransport
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import get_db
from app.main import create_app
from app.models import Base

TEST_DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def sale_payload():
    return {"name": "Alice", "phone": "0909123456", "email": "alice@example.com", "status": "active"}


@pytest_asyncio.fixture
async def created_sale(client, sale_payload):
    response = await client.post("/api/sales", json=sale_payload)
    return response.json()


@pytest_asyncio.fixture
async def agency_payload():
    return {"name": "Agency A", "address": "123 Street", "area": "HCMC", "sale_id": 1}


@pytest_asyncio.fixture
async def created_agency(client, created_sale, agency_payload):
    response = await client.post("/api/agencies", json=agency_payload)
    return response.json()


@pytest_asyncio.fixture
async def track_record_payload():
    return {"customer_name": "Customer X", "expected_revenue": 5000, "status": "new", "agency_id": 1}


@pytest_asyncio.fixture
async def created_track_record(client, created_agency, track_record_payload):
    response = await client.post("/api/track-records", json=track_record_payload)
    return response.json()
