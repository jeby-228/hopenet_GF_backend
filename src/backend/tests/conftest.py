"""
Pytest configuration and fixtures for the test suite.

This module contains shared fixtures and configuration for all tests.
"""

import asyncio
import typing as t
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from app.dependencies.database_dependency import get_async_session
from app.main import app
from app.models.task_model import Task
from app.models.user_model import User


# Test database URL - adjust according to your test environment
TEST_DATABASE_URL = 'postgresql+asyncpg://test_user:test_password@localhost:5432/test_db'


@pytest.fixture(scope='session')
def event_loop():
    """Create an event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def test_engine():
    """Create a test database engine and setup/teardown tables."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope='function')
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session_maker = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope='function')
async def client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with database session override."""

    async def override_get_async_session():
        yield test_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_session: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        email='test@example.com',
        hashed_password='$2b$12$fake_hashed_password',  # This should be a real bcrypt hash in production
        is_active=True,
        is_superuser=False,
        is_verified=False,
    )

    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)

    return user


@pytest.fixture
async def test_superuser(test_session: AsyncSession) -> User:
    """Create a test superuser."""
    user = User(
        email='admin@example.com',
        hashed_password='$2b$12$fake_hashed_password',
        is_active=True,
        is_superuser=True,
        is_verified=True,
    )

    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)

    return user


@pytest.fixture
async def auth_headers(test_user: User) -> dict[str, str]:
    """Create authentication headers with a test JWT token.

    Note: In a real implementation, you would generate a proper JWT token here.
    This is a simplified version for demonstration purposes.
    """
    # TODO: Implement proper JWT token generation using fastapi-users
    token = 'test_jwt_token_replace_with_real_token'
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
async def test_task(test_session: AsyncSession, test_user: User) -> Task:
    """Create a test task."""
    task = Task(
        title='測試任務',
        description='這是一個測試任務',
        creator_id=test_user.id,
        weight=50,
        is_deleted=False,
    )

    test_session.add(task)
    await test_session.commit()
    await test_session.refresh(task)

    return task


@pytest.fixture
async def test_tasks(test_session: AsyncSession, test_user: User) -> list[Task]:
    """Create multiple test tasks."""
    tasks = [
        Task(title=f'任務 {i}', description=f'描述 {i}', creator_id=test_user.id, weight=50)
        for i in range(1, 6)
    ]

    for task in tasks:
        test_session.add(task)

    await test_session.commit()

    for task in tasks:
        await test_session.refresh(task)

    return tasks
