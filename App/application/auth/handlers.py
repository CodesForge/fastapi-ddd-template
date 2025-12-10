from uuid import uuid4
from App.domain.entities import User
from App.domain.value_object import Email, Hash
from App.application.auth.commands import RegisterUserCommand
from App.application.auth.dto import AuthResultDTO
from App.application.unit_of_work import AbstractUnitOrWork

from typing import Protocol

class RabbitProtocol(Protocol):
    def send_message(self, message: str | dict, queue: str) -> None: ...

class HasherProtocol(Protocol):
    def hash(self, password: str) -> str: ...
    def verify(self, hashed_password: str, password: str) -> bool: ...

class RegisterUserHandler:
    def __init__(
        self,
        rabbit: RabbitProtocol,
        hasher: HasherProtocol,
        uow: AbstractUnitOrWork,
    ) -> AuthResultDTO:
        self._rabbit = rabbit
        self._hasher = hasher
        self._uow = uow
    
    async def handle(self, cmd: RegisterUserCommand, queue: str) -> None:
        async with self._uow:
            existing = await self._uow.users.get_user_by_email(cmd.email)
            if existing is not None:
                raise ValueError("Email already registered")
        
            password_hash = await self._hasher.hashed_password(cmd.password)
            user = User(
                id=None,
                email=Email(cmd.email),
                password_hash=Hash(password_hash),
            )
            await self._rabbit.send_message(
                {
                    "email": user.email.value,
                    "password_hash": password_hash,
                }, queue=queue,
            )
        
            await self._uow.users.add_user(user)
            await self._uow.commit()
        
        return AuthResultDTO(
            status="success", message="The account has been successfully registered!",
        )
        