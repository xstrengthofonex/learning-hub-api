

async def test_register_user(client):
    data = dict(email="example@email.com", username="Username", password="12345678")
    response = await client.post("/users", json=data)
    assert response.status == 201
    assert response.content_type == "application/json"
    body = await response.json()
    token = body.get("token")
    assert token is not None
    assert body.get("userId") is not None

