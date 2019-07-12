from learning_hub.domain.users import User
from learning_hub.repositories.in_memory_users import InMemoryUsers


async def test_get_users_by_id_returns_user():
    users = InMemoryUsers()
    u1 = User(id="1", email="email1", username="username1", password="password1")
    u2 = User(id="2", email="email2", username="username2", password="password2")
    await users.add(u1)
    await users.add(u2)
    result = await users.find_by_id(u1.id)
    assert result == u1
