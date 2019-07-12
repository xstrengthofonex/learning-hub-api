import pytest

from learning_hub.domain.users import User
from learning_hub.repositories.in_memory_users import InMemoryUsers


@pytest.fixture
def users():
    return InMemoryUsers()


async def test_get_users_by_id_returns_user(users):
    u1 = User(id="1", email="email1", username="username1", password="password1")
    u2 = User(id="2", email="email2", username="username2", password="password2")
    await users.add(u1)
    await users.add(u2)
    result = await users.find_by_id(u1.id)
    assert result == u1


async def test_username_exists_should_return_true(users):
    username = "username"
    u1 = User(id="1", email="email", username=username, password="password")
    assert await users.username_exists(username) is False
    await users.add(u1)
    assert await users.username_exists(username) is True


async def test_email_exists_should_return_true(users):
    email = "email"
    u1 = User(id="1", email=email, username="username", password="password")
    assert await users.email_exists(email) is False
    await users.add(u1)
    assert await users.email_exists(email) is True
