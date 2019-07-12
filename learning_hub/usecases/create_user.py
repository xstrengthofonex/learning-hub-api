from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserRequest:
    email: str
    username: str
    password: str


@dataclass
class CreateUserResponse:
    user_id: str


class CreateUser:
    async def execute(self, request):
        raise NotImplementedError
