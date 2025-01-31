from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine, AsyncSession)
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra="allow")
    DEBUG: bool = True

    DB_NAME: str = "db_notes.sqlite"

    GOOGLE_CLIENT_ID: str = "your-google-client-id"
    GOOGLE_CLIENT_SECRET: str = "your-google-client-secret"
    GOOGLE_REDIRECT_URI: str = "your-google-redirect-uri"

    SECRET_KEY: str = "secret_key-123"
    ALGORITHM: str = "HS256"

    def sqlite_dsn(self) -> str:
        return f"sqlite:///{self.DB_NAME}"


class Base(DeclarativeBase):
    pass

settings_app = Settings()

DATABASE_URL = f"sqlite+aiosqlite:///{settings_app.DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
