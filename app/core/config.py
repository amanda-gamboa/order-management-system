import os

from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if value is None or not value.strip():
        raise ValueError(f"Missing required environment variable: {name}")

    return value


DB_USER = get_required_env("DB_USER").strip()
DB_PASSWORD = get_required_env("DB_PASSWORD")
DB_HOST = get_required_env("DB_HOST").strip()
DB_NAME = get_required_env("DB_NAME").strip()

_db_port = os.getenv("DB_PORT", "3306").strip()

try:
    DB_PORT = int(_db_port)
except ValueError as exc:
    raise ValueError("DB_PORT must be a valid integer") from exc

if not 1 <= DB_PORT <= 65535:
    raise ValueError("DB_PORT must be between 1 and 65535")
