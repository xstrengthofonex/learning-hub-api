from tests.acceptance.dsl import (
    create_learning_path, register_user, get_learning_path, create_participation)


async def test_get_learning_path(client):
    user = await register_user(client)
    path = await create_learning_path(client, user.get("token"), title="My Path")
    await create_participation(client, user.get("token"), path.get("pathId"))
    result = await get_learning_path(client, user.get("token"), path.get("pathId"))
    assert result.get("title") == "My Path"
    assert result.get("participants") == 1


async def test_learning_path_does_not_exist(client):
    user = await register_user(client, email="participator@email.com", username="participator")
    result = await get_learning_path(client, user.get("token"), "Unknown", status=404)
    assert result.get("message") == "Learning path not found"

