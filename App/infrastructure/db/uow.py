from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from App.application.unit_of_work import AbstractUnitOrWork
from App.infrastructure.db.session import DataBaseConfig
from App.infrastructure.security.argon_hasher import ArgonHashConfig
from App.infrastructure.db.repositories.user_repository import SQLAlchemyUserRepository
from typing import Optional

class SQLAlchemyUnitofWork(AbstractUnitOrWork):
    def __init__(
        self,
        session: async_sessionmaker[AsyncSession],
        argon_confin: ArgonHashConfig,
    ):
        self._async_factory = session
        self._argon = argon_confin
        self.session: Optional[AsyncSession] = None
    
    async def __aenter__(self):
        self.session = self._async_factory()
        self.users = SQLAlchemyUserRepository(self._async_factory)
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            await self.session.rollback()
        await self.session.close()
    
    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()