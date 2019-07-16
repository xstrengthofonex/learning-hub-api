EMAIL = "example@email.com"
USERNAME = "username"
PASSWORD = "12345678"
TITLE = "title"
DESCRIPTION = "description"
CATEGORIES = ["Category"]
ASSIGNMENT_NAME = "Assignment 1"
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


async def test_returns_401_if_token_not_valid(client):
    data = dict(token="Invalid Token",
                title=TITLE,
                description=DESCRIPTION,
                categories=CATEGORIES,
                assignments=ASSIGNMENTS)
    response = await client.post("/paths", json=data)
    assert response.status == 401
    assert response.content_type == "application/json"
    body = await response.json()
    assert body.get("message") == "Token is not valid"


async def test_returns_400_if_request_data_is_invalid(client):
    token = await register_user(client)
    data = dict(token=token,
                title="",
                description=DESCRIPTION,
                categories=CATEGORIES,
                assignments=ASSIGNMENTS)
    response = await client.post("/paths", json=data)
    assert response.status == 400
    assert response.content_type == "application/json"
    body = await response.json()
    print(body)
    assert "Title is required" in body.get("errors", [])


async def register_user(client):
    data = dict(email=EMAIL, username=USERNAME, password=PASSWORD)
    response = await client.post("/users", json=data)
    body = await response.json()
    return body.get("token", "")


