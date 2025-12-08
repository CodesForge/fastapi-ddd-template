from App.application.unit_of_work import AbstractUnitOrWork
from App.infrastructure.db.session import DataBaseConfig
from App.infrastructure.security.argon_hasher import ArgonHashConfig
from App.infrastructure.db.repositories.user_repository import SQLAlchemyUserRepository

class SQLAlchemyUnitofWork(AbstractUnitOrWork):
    def __init__(
        self,
        db_config: DataBaseConfig,
        argon_confin: ArgonHashConfig,
    ):
        self._db = db_config
        self._argon = argon_confin
        self.session = None
    
    async def __aenter__(self):
        self.session = self._db.async_session()
        self.users = SQLAlchemyUserRepository(self.session)
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            await self.session.rollback()
        await self.session.close()
    
    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()