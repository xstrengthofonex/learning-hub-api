from dataclasses import dataclass

from learning_hub.domain.users import Users, User, UserValidator
from learning_hub.helpers import IdGenerator


@dataclass(frozen=True)
class CreateUserRequest:
    email: str = ""
    username: str = ""
    password: str = ""


@dataclass
class CreateUserResponse:
    user_id: str


class CreateUser:
    def __init__(self, users: Users) -> None:
        self.users = users
        self.id_generator = IdGenerator()
        self.user_validator = UserValidator(self.users)

    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        user = self.user_from_request(request)
        await self.user_validator.validate(user)
        await self.users.add(user)
        return CreateUserResponse(user_id=user.id)

    def user_from_request(self, request) -> User:
        return User(id=self.id_generator.generate(),
                    email=request.email,
                    username=request.username,
                    password=request.password)
