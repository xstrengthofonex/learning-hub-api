from uuid import uuid4

import pytest
from asynctest import Mock

from learning_hub.domain.users import Users, User
from learning_hub.usecases.create_user import CreateUser, CreateUserRequest


USER_ID = str(uuid4())
CREATE_USER_REQUEST = CreateUserRequest(
    email="example@email.com",
    username="username",
    password="password")
USER = User(
    id=USER_ID,
    email=CREATE_USER_REQUEST.email,
    username=CREATE_USER_REQUEST.username,
    password=CREATE_USER_REQUEST.password)


@pytest.fixture(autouse=True)
def setup(id_generator):
    id_generator.generate.return_value = USER_ID


@pytest.fixture
def users():
    return Mock(Users)


async def test_create_user_saves_the_user(id_generator, users):
    create_user = CreateUser(users, id_generator)
    await create_user.execute(CREATE_USER_REQUEST)
    users.add.assert_called_with(USER)


async def test_create_user_returns_user_id_for_created_user(id_generator, users):
    create_user = CreateUser(users, id_generator)
    result = await create_user.execute(CREATE_USER_REQUEST)
    assert result.user_id == USER_ID
