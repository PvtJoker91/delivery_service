from asyncio import current_task
from contextlib import asynccontextmanager
from punq import Container
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, async_scoped_session
from sqlalchemy.orm import declarative_base

from app.di import _initialize_container
from app.settings.config import settings

test_engine = create_async_engine(
    url=f'mysql+aiomysql://test_user:test_password@{settings.db.mysql_host}:{settings.db.mysql_port}/test_db',
    echo=False,
)
test_session_factory = async_sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


@asynccontextmanager
async def init_async_test_session():
    Base = declarative_base()
    Base.metadata.create_all(test_engine)
    session = async_scoped_session(
        session_factory=test_session_factory,
        scopefunc=current_task,
    )
    yield session
    Base.metadata.drop_all(test_engine)


def init_dummy_container() -> Container:
    container = _initialize_container()

    container.register(AsyncSession, factory=init_async_test_session)

    return container
