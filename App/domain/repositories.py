from typing import Protocol, Optional
from App.domain.entities import User

class UserRepositoryProtocol(Protocol):
    async def add_user(self, user: User) -> Optional[User]:
        ...

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        ...
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        ...