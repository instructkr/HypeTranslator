import asyncio
from contextlib import asynccontextmanager, AbstractAsyncContextManager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session, async_sessionmaker
from .models import Base

class Database:
    def __init__(self, connection_url: str):
        self._engine = create_async_engine(connection_url, echo=True)
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
            scopefunc=asyncio.current_task,
        )

    @asynccontextmanager
    async def session(self):
        session: AbstractAsyncContextManager[AsyncSession] = self._session_factory()
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def reset_database(self) -> None:
        '''
        Drop all tables and recreate them.
        Just for testing purposes.
        DO NOT USE IN PRODUCTION
        '''
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
