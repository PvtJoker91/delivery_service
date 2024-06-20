from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session

from app.settings.config import settings

engine = create_async_engine(url=settings.db.db_url, echo=settings.db.echo, )
session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# def init_async_session():
#     return session_factory()


@asynccontextmanager
async def init_async_session():
    session = async_scoped_session(
        session_factory=session_factory,
        scopefunc=current_task,
    )
    yield session
