from typing import Optional
from sqlalchemy import select, insert
from App.domain.entities import User
from App.domain.repositories import UserRepositoryProtocol
from App.domain.value_object import Email, Hash
from App.infrastructure.db.models import UserModel
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from App.infrastructure.log.logger import logger

class SQLAlchemyUserRepository(UserRepositoryProtocol):
    def __init__(
        self, session: async_sessionmaker[AsyncSession],
    ) -> None:
        self._session = session
    
    async def add_user(self, user: User) -> None:
        try:
            async with self._session() as session:
                stmt = insert(UserModel).values(
                    {
                        "id": user.id,
                        "email": user.email.value,
                        "password_hash": user.password_hash.value,
                        "is_active": user.is_active,
                        "created_at": user.created_at,
                    }
                )
                await session.execute(stmt)
                await session.commit()
                logger.info("the data has been successfully filled into the database!")
        except Exception as e:
            logger.exception(f"Error: {e}")
    
    async def get_user_by_email(self, email: Email | str) -> Optional[User]:
        try:
            if isinstance(email, Email):
                email = email.value
            
            async with self._session() as session:
                stmt = select(UserModel).where(UserModel.email == email)
                result = await session.execute(stmt)
                user_model = result.scalar_one_or_none()
                
                if user_model is None:
                    return None
                
                return User(
                    id=user_model.id,
                    email=Email(user_model.email),
                    password_hash=Hash(user_model.password_hash),
                    is_active=user_model.is_active,
                    created_at=user_model.created_at,
                )
        except Exception as e:
            logger.exception(f"Error: {e}")
     
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        try:
            async with self._session() as session:
                stmt = select(UserModel).where(UserModel.id == user_id)
                result = await session.execute(stmt)
                user_model = result.scalar_one_or_none()
                
                if not user_model:
                    return None
                
                return User(
                    id=user_model.id,
                    email=Email(user_model.email),
                    password_hash=Hash(user_model.password_hash),
                    is_active=user_model.is_active,
                    created_at=user_model.created_at,
                )
        except Exception as e:
            logger.exception(f"Error: {e}")
            