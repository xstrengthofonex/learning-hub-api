from tests.acceptance.dsl import register_user, create_learning_path


async def test_create_participation(client):
    creator_token = await get_user_token(client, email="creator@email.com", username="creator")
    participator_token = await get_user_token(client, email="participator@email.com", username="participator")
    path_id = await get_path_id(client, creator_token)
    response = await create_participation(client, participator_token, path_id)
    assert response.status == 201
    body = await response.json()
    assert body.get("participationId") is not None


async def test_learning_path_does_not_exist(client):
    participator_token = await get_user_token(client, email="participator@email.com", username="participator")
    response = await create_participation(client, token=participator_token, path_id="Does not exist")
    assert response.status == 404
    body = await response.json()
    assert body.get("message") == "Learning path not found"


async def create_participation(client, token, path_id):
    headers = {'Authorization': f"Bearer {token}"}
    return await client.post("/participations", headers=headers, json=dict(pathId=path_id))


async def get_path_id(client, creator_token):
    response = await create_learning_path(client, creator_token)
    body = await response.json()
    path_id = body.get("pathId")
    return path_id


async def get_user_token(client, **kwargs):
    response = await register_user(client, **kwargs)
    body = await response.json()
    token = body.get("token")
    return token
