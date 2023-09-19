import asyncio
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# _DB_CONN: Optional[aiomysql.Pool] = None
_ENGINE: AsyncEngine = None
_SESSION_FACTORY = None


# TODO: yeah, it would be like that: async def init_async_engine(Base=None). I dont like it.
async def init_engine() -> None:
    global _ENGINE
    global _SESSION_FACTORY

    if not _ENGINE:
        _ENGINE = create_async_engine('sqlite+aiosqlite:///./tes.sqlite', pool_recycle=3600)

    if not _SESSION_FACTORY:
        _SESSION_FACTORY = sessionmaker(_ENGINE, expire_on_commit=False, class_=AsyncSession)


async def stop_engine() -> None:
    global _ENGINE

    # log = logging.getLogger("cpanel")

    if _ENGINE:
        # log.debug("Stop DB engine")
        await _ENGINE.dispose()


async def get_engine() -> AsyncEngine:
    global _ENGINE
    if not _ENGINE:
        await init_engine()

    return _ENGINE


def get_session() -> AsyncSession:
    global _SESSION_FACTORY

    assert _SESSION_FACTORY

    return async_scoped_session(_SESSION_FACTORY, scopefunc=asyncio.current_task)()
