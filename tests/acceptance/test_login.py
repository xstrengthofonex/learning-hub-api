EMAIL = "example@email.com"
USERNAME = "username"
PASSWORD = "12345678"


async def test_login(client):
    await register_user(client)
    response = await client.post("/login", json=dict(email=EMAIL, password=PASSWORD))
    assert response.status == 200
    assert response.content_type == "application/json"
    body = await response.json()
    assert body.get("token") is not None
    assert body.get("userId") is not None


async def register_user(client):
    data = dict(email=EMAIL, username=USERNAME, password=PASSWORD)
    await client.post("/users", json=data)
