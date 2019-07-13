from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: str
    email: str
    username: str
    password: str
    country: str = ""
    show_email: str = False


class Users(ABC):
    @abstractmethod
    async def add(self, user: User):
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


class UserValidator:
    def __init__(self, users: Users):
        self.users = users
        self.errors = []

    async def validate(self, user: User):
        self.errors = []
        await self.validate_email(user.email)
        await self.validate_username(user.username)
        await self.validate_password(user.password)
        if self.errors:
            raise ValueError(self.errors)

    async def validate_username(self, username):
        if not username:
            self.errors.append("Username is required")
        elif await self.users.username_exists(username):
            self.errors.append("Username already in use")

    async def validate_email(self, email):
        if not email:
            self.errors.append("Email is required")
        elif await self.users.email_exists(email):
            self.errors.append("Email already in use")

    async def validate_password(self, password):
        if not password:
            self.errors.append("Password is required")
