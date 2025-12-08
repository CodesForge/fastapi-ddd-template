from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from App.config.argon import get_argon_settings

from typing import Optional

class ArgonHashConfig:
    def __init__(self):
        self._setting = get_argon_settings()
        self._ph: Optional[PasswordHasher] = None
    
    @property
    def ph(self) -> PasswordHasher:
        if self._ph is None:
            self._ph = PasswordHasher(
                time_cost=self._setting.time_cost,
                parallelism=self._setting.parallelism,
                hash_len=self._setting.hash_len,
                salt_len=self._setting.salt_len,
                memory_cost=self._setting.memory_cost,
            )
        return self._ph
    
    async def hash_password(self, password: str) -> str:
        return self.ph.hash(password)
    
    async def verify_password(self, hashed_password: str, password: str) -> bool:
        try:
            return self.ph.verify(hashed_password, password)
        except VerifyMismatchError:
            return False