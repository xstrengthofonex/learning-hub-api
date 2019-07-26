from tests.acceptance.dsl import register_user, create_learning_path, create_participation


async def test_create_participation(client):
    creator = await register_user(client, email="creator@email.com", username="creator")
    participator = await register_user(client, email="participator@email.com", username="participator")
    path = await create_learning_path(client, creator.get("token"))
    result = await create_participation(client, participator.get("token"), path.get("pathId"))
    assert result.get("participationId") is not None


async def test_learning_path_does_not_exist(client):
    participator = await register_user(client, email="participator@email.com", username="participator")
    result = await create_participation(
        client, token=participator.get("token"), path_id="Does not exist", status=404)
    assert result.get("message") == "Learning path not found"
