from tests.acceptance.dsl import register_user, create_learning_path


async def test_create_a_learning_path(client):
    user = await register_user(client)
    await create_learning_path(client, user.get("token"))


async def test_returns_401_if_token_not_valid(client):
    result = await create_learning_path(client, "Invalid token", status=401)
    assert result.get("message") == "Token is not valid"


async def test_returns_400_if_request_data_is_invalid(client):
    user = await register_user(client)
    result = await create_learning_path(client, user.get("token"), title="", status=400)
    assert "Title is required" in result.get("errors", [])
