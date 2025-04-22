from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASS: str
    NAME: str

    @property
    def DATABASE_URL(self):
        """Асинхронная URL для приложения."""
        return f"postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"

    @property
    def SYNC_DATABASE_URL(self):
        """Синхронная URL для миграций."""
        return f"postgresql+psycopg2://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_", extra="ignore")


class Base(DeclarativeBase):
    pass


settings = Settings()  # type: ignore
engine = create_async_engine(url=settings.DATABASE_URL, echo=False)

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with async_session() as session:
        yield session
