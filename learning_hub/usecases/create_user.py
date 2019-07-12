from dataclasses import dataclass

from learning_hub.domain.users import Users, User
from learning_hub.usecases.helpers import IdGenerator


@dataclass(frozen=True)
class CreateUserRequest:
    email: str
    username: str
    password: str


@dataclass
class CreateUserResponse:
    user_id: str


class CreateUser:
    def __init__(self, users: Users, id_generator: IdGenerator):
        self.users = users
        self.id_generator = id_generator

    async def execute(self, request: CreateUserRequest):
        user = User(id=self.id_generator.generate(),
                    email=request.email,
                    username=request.username,
                    password=request.password)
        await self.users.add(user)
        return CreateUserResponse(user_id=user.id)
