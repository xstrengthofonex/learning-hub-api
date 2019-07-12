from typing import List

from learning_hub.domain.users import Users, User


class InMemoryUsers(Users):
    def __init__(self):
        self.users: List[User] = list()

    async def add(self, user: User) -> None:
        self.users.append(user)

    async def find_by_id(self, user_id: str) -> User:
        return next((user for user in self.users if user.id == user_id), None)
