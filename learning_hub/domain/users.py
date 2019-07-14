from abc import ABC, abstractmethod
from dataclasses import dataclass

from learning_hub.domain.common import Entity, Validator


@dataclass(frozen=True)
class User(Entity):
    email: str
    username: str
    password: str
    country: str = ""
    show_email: str = False


class Users(ABC):
    @abstractmethod
    async def add(self, user: User) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, id_: str) -> User:
        pass

    @abstractmethod
    async def username_exists(self, username: str) -> bool:
        pass

    @abstractmethod
    async def email_exists(self, email: str) -> bool:
        pass

    @abstractmethod
    async def find_by_credentials(self, email: str, password: str) -> User:
        pass


class UserValidator(Validator):
    def __init__(self, users: Users) -> None:
        self.users = users

    async def validate_username(self, username: str) -> None:
        self.assert_not_blank(username, "Username is required")
        assert await self.users.username_exists(username) is not True, "Username already in use"

    async def validate_email(self, email: str) -> None:
        self.assert_not_blank(email, "Email is required")
        assert await self.users.email_exists(email) is not True, "Email already in use"

    async def validate_password(self, password: str) -> None:
        self.assert_not_blank(password, "Password is required")
