"""Fixtures for integration tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.dependencies import get_session
from app.main import app
from app.models.base import Base
from tests.integration.database import TestingSessionLocal, test_engine


def get_test_session() -> Generator[Session, None, None]:
    """Provide a database session for integration tests."""

    with TestingSessionLocal.begin() as session:
        yield session


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Provide a TestClient connected to the testing database."""

    previous_override = app.dependency_overrides.get(get_session)

    app.dependency_overrides[get_session] = get_test_session

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        if previous_override is None:
            app.dependency_overrides.pop(get_session, None)
        else:
            app.dependency_overrides[get_session] = previous_override


@pytest.fixture(autouse=True)
def reset_database() -> Generator[None, None, None]:
    """Automatically reset the database before and after each integration test."""

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)
