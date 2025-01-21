from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine, AsyncSession)
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra="allow")
    DEBUG: bool = True

    DB_USER: str = 'postgres'
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "db_notes"

    GOOGLE_CLIENT_ID: str = "your-google-client-id"
    GOOGLE_CLIENT_SECRET: str = "your-google-client-secret"
    GOOGLE_REDIRECT_URI: str = "your-google-redirect-uri"

    SECRET_KEY: str = "secret_key-123"
    ALGORITHM: str = "HS256"

    def pg_dsn(self, engine_="asyncpg") -> PostgresDsn:
        return (
            f"postgresql+{engine_}://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@"
            f"localhost:5432/{self.DB_NAME}")

class Base(DeclarativeBase):
    pass

settings_app = Settings()

DATABASE_URL = settings_app.pg_dsn()
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
