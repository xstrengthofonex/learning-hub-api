EMAIL = "example@email.com"
USERNAME = "username"
PASSWORD = "12345678"
TITLE = "title"
DESCRIPTION = "description"
CATEGORIES = ["Category"]
ASSIGNMENT_NAME = "Assignement 1"
ASSIGNMENT_RESOURCE = "http://resource.com"
ASSIGNMENT_INSTRUCTIONS = "So instructions"
ASSIGNMENTS = [dict(
    name=ASSIGNMENT_NAME,
    resource=ASSIGNMENT_RESOURCE,
    instructions=ASSIGNMENT_INSTRUCTIONS)]


async def test_create_a_learning_path(client):
    token = await register_user(client)
    data = dict(token=token,
                title=TITLE,
                description=DESCRIPTION,
                categories=CATEGORIES,
                assignments=ASSIGNMENTS)
    response = await client.post("/paths", json=data)
    assert response.status == 201
    assert response.content_type == "application/json"
    body = await response.json()
    assert body.get("pathId") is not None


async def register_user(client):
    data = dict(email=EMAIL, username=USERNAME, password=PASSWORD)
    response = await client.post("/users", json=data)
    body = await response.json()
    return body.get("token")

