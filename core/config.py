import environ
import logging
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(BASE_DIR / '.env')

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{env('DB_USER')}:{env('DB_PASS')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}"

    @property
    def TEST_DATABASE_URL(self):
        return f"postgresql+asyncpg://{env('TEST_DB_USER')}:{env('TEST_DB_PASS')}@{env('TEST_DB_HOST')}:{env('TEST_DB_PORT')}/{env('TEST_DB_NAME')}"


settings = Settings()
