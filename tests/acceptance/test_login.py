from tests.acceptance.dsl import register_user


async def test_login(client):
    await register_user(client)
    response = await client.post("/login", json=dict(email="example@email.com", password="12345678"))
    assert response.status == 200
    assert response.content_type == "application/json"
    body = await response.json()
    assert body.get("token") is not None
    assert body.get("userId") is not None
