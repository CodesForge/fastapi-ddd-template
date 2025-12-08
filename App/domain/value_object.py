from dataclasses import dataclass

@dataclass(frozen=True)
class Email:
    value: str
    
    def __post_init__(self) -> None:
        if "@" not in self.value:
            raise ValueError("InvalidEmail")
    
    def __str__(self) -> str:
        return self.value

@dataclass(frozen=True)
class Hash:
    value: str
    
    def __post_init__(self) -> None:
        if "$argon" not in self.value:
            raise ValueError("InvalidPassword")
    
    def __str__(self) -> str:
        return self.value