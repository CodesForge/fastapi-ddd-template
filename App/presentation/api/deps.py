from fastapi import Depends
from App.infrastructure.db.repositories.user_repository import SQLAlchemyUserRepository
from App.infrastructure.messaging.rabbit_config import RabbitMQConfig
from App.infrastructure.db.session import DataBaseConfig
from App.infrastructure.security.argon_hasher import ArgonHashConfig
from App.domain.repositories import UserRepositoryProtocol
from App.application.auth.handlers import RegisterUserHandler
from App.infrastructure.db.uow import SQLAlchemyUnitofWork
from typing import Annotated
from functools import lru_cache

@lru_cache
def get_db_config() -> DataBaseConfig:
    return DataBaseConfig()

@lru_cache
def get_rabbit_config() -> RabbitMQConfig:
    return RabbitMQConfig()

def get_user_repository(
    db: Annotated[DataBaseConfig, Depends(get_db_config)],
) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db.async_session)

@lru_cache
def get_argon_config() -> ArgonHashConfig:
    return ArgonHashConfig()

def get_uow(
    db: Annotated[DataBaseConfig, Depends(get_db_config)],
    hasher: Annotated[ArgonHashConfig, Depends(get_argon_config)],
) -> SQLAlchemyUnitofWork:
    return SQLAlchemyUnitofWork(db.async_session, hasher)

def get_register_user_handler(
    rabbit: Annotated[RabbitMQConfig, Depends(get_rabbit_config)],
    uow: Annotated[SQLAlchemyUnitofWork, Depends(get_uow)],
    hasher: Annotated[ArgonHashConfig, Depends(get_argon_config)],
) -> RegisterUserHandler:
    return RegisterUserHandler(rabbit, hasher, uow)