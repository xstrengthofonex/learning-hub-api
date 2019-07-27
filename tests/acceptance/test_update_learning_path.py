from tests.acceptance.dsl import (
    register_user, create_learning_path, get_learning_path, update_learning_path)


NEW_TITLE = "New Title"
NEW_ASSIGNMENT = dict(
    name="New Assignment",
    resource="http://new-resource.com",
    instructions="New instructions")


async def test_updated_learning_path(client):
    user = await register_user(client)
    path = await create_learning_path(client, user.get("token"), title="My Path")
    result = await get_learning_path(client, user.get("token"), path.get("pathId"))
    result["title"] = "New Title"
    result["assignments"].append(NEW_ASSIGNMENT)
    response = await update_learning_path(client, user.get("token"), result)
    assert response.get("title") == NEW_TITLE
    for assignment in response.get("assignments"):
        assert assignment.get("id") is not None


