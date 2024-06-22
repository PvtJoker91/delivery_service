from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.settings.config import settings

engine = create_async_engine(url=settings.db.db_url, echo=settings.db.echo, )
session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def init_async_session():
    return session_factory()
