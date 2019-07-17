from tests.acceptance.dsl import register_user, create_learning_path


async def test_create_a_learning_path(client):
    response = await register_user(client)
    body = await response.json()
    await create_learning_path(client, body.get("token"))


async def test_returns_401_if_token_not_valid(client):
    response = await create_learning_path(client, "Invalid token")
    assert response.status == 401
    assert response.content_type == "application/json"
    body = await response.json()
    assert body.get("message") == "Token is not valid"


async def test_returns_400_if_request_data_is_invalid(client):
    response = await register_user(client)
    body = await response.json()
    response = await create_learning_path(client, body.get("token"), title="")
    assert response.status == 400
    assert response.content_type == "application/json"
    body = await response.json()
    assert "Title is required" in body.get("errors", [])
