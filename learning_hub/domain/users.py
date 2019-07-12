from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: str
    email: str
    username: str
    password: str


class Users(ABC):
    @abstractmethod
    async def add(self, user: User):
        pass

    @abstractmethod
    async def find_by_id(self, id_: str) -> User:
        pass
