import os

from sqlmodel import create_engine, SQLModel, Session
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

DATABASE_USERNAME= os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD= os.environ.get("DATABASE_PASSWORD")
DATABASE_HOSTNAME= os.environ.get("DATABASE_HOSTNAME")

DATABASE_URL = os.environ.get("DATABASE_URL")
DBURL = f'postgresql+asyncpg://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:5432/fastapi_eshop'

engine = AsyncEngine(create_engine(DBURL,echo=True, future=True))

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def getSession() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session