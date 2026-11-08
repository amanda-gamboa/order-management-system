"""Database configuration for integration tests."""

import os

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER, DB_NAME

TEST_DB_NAME = os.getenv("TEST_DB_NAME")

if not TEST_DB_NAME:
    raise ValueError("Missing required environment variable: TEST_DB_NAME")

if TEST_DB_NAME == DB_NAME:
    raise ValueError("Test database cannot be the production database.")

TEST_DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=TEST_DB_NAME,
)


test_engine = create_engine(
    TEST_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)


TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)
