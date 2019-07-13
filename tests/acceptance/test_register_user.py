EMAIL = "example@email.com"
USERNAME = "username"
PASSWORD = "12345678"


async def test_register_user(client):
    data = dict(email=EMAIL, username=USERNAME, password=PASSWORD)
    response = await client.post("/users", json=data)
    assert response.status == 201
    assert response.content_type == "application/json"
    body = await response.json()
    assert body.get("token") is not None
    assert body.get("userId") is not None
