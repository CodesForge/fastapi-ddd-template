from dataclasses import dataclass
from datetime import datetime
import uuid

from typing import Optional
from App.domain.value_object import Email, Hash

@dataclass
class User:
    id: Optional[str] = None
    email: Email
    password_hash: Hash
    
    is_active: bool = True
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.id is None:
            self.id = str(uuid.uuid4())
    
    def deactive(self):
        self.is_active = False