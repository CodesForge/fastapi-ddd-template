from dataclasses import dataclass

@dataclass
class AuthResultDTO:
    status: str
    message: str