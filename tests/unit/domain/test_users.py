import pytest
from asynctest import Mock

from learning_hub.domain.users import UserValidator, User, Users

EMPTY_USER = User(id="1", email="", username="", password="")
DUPLICATE_USER = User(id="1", email="example@email.com", username="duplicate", password="password")
VALIDATION_ERROR = ValueError


@pytest.fixture
def users():
    users = Mock(Users)
    users.username_exists.return_value = False
    users.email_exists.return_value = False
    return users


@pytest.fixture
def validator(users):
    return UserValidator(users)


async def test_user_validator_does_not_accept_empty_username_password_or_email(validator):
    with pytest.raises(VALIDATION_ERROR) as e:
        await validator.validate(EMPTY_USER)
    assert all([m in str(e.value) for m in [
        "Email is required", "Username is required", "Password is required"]])


async def test_user_validator_does_not_accept_duplicate_usernames(validator, users):
    users.username_exists.return_value = True
    with pytest.raises(VALIDATION_ERROR) as e:
        await validator.validate(DUPLICATE_USER)
    assert "Username already in use" in str(e.value)


async def test_user_validator_does_not_accept_duplicate_emails(validator, users):
    users.email_exists.return_value = True
    with pytest.raises(VALIDATION_ERROR) as e:
        await validator.validate(DUPLICATE_USER)
    assert "Email already in use" in str(e.value)
