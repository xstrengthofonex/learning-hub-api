from tests.acceptance.dsl import create_learning_path, register_user, get_learning_path


async def test_get_learning_path(client):
    user = await register_user(client)
    path = await create_learning_path(client, user.get("token"), title="My path")
    result = await get_learning_path(client, user.get("token"), path.get("pathId"))
    assert result.get("title") == "My Path"
