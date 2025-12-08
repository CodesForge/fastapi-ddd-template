from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from App.infrastructure.log.logger import logger
from App.infrastructure.db.models import Base

class DataBaseConfig:
    def __init__(self):
        self._url_db = "sqlite+aiosqlite:///database.db"
        self._async_engine: Optional[AsyncEngine] = None
        self._async_session: Optional[async_sessionmaker[AsyncSession]]
    
    @property
    def async_engine(self) -> AsyncEngine:
        try:
            if self._async_engine is None:
                self._async_engine = create_async_engine(
                    self._url_db,
                )
            return self._async_engine
        except SQLAlchemyError as e:
            logger.exception(f"Error in async-engine initialization: {e}")
            raise

    @property
    def async_session(self) -> async_sessionmaker[AsyncSession]:
        try:
            if self._async_session is None:
                self._async_session = async_sessionmaker(
                    self.async_engine, expire_on_commit=False,
                )
            return self._async_session
        except SQLAlchemyError as e:
            logger.exception(f"Error in async-session initialization: {e}")
            raise
    
    async def connect(self) -> None:
        try:
            async with self.async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                logger.info("The database has been successfully launched!")
        except SQLAlchemyError as e:
            logger.exception(f"Error in starting the database: {e}")
            raise
    
    async def disconnect(self) -> None:
        try:
            await self.async_engine.dispose()
            logger.info("The database has been successfully disabled!")
        except SQLAlchemyError as e:
            logger.exception(f"An error in disabling the database: {e}")
            raise
    
    