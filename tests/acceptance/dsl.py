
EMAIL = "example@email.com"
USERNAME = "username"
PASSWORD = "12345678"
TITLE = "Title"
DESCRIPTION = "description"
CATEGORIES = ("Category",)
ASSIGNMENT_NAME = "Assignment 1"
ASSIGNMENT_RESOURCE = "http://resource.com"
ASSIGNMENT_INSTRUCTIONS = "So instructions"
ASSIGNMENTS = (dict(
    name=ASSIGNMENT_NAME,
    resource=ASSIGNMENT_RESOURCE,
    instructions=ASSIGNMENT_INSTRUCTIONS),)


async def register_user(client, email=EMAIL, username=USERNAME, password=PASSWORD, status=201):
    data = dict(email=email, username=username, password=password)
    response = await client.post("/users", json=data)
    assert response.status == status
    assert response.content_type == "application/json"
    return await response.json()


async def create_learning_path(client, token, title=TITLE, description=DESCRIPTION,
                               categories=CATEGORIES, assignments=ASSIGNMENTS, status=201):
    data = dict(title=title,
                description=description,
                categories=categories,
                assignments=assignments)
    headers = {'Authorization': f"Bearer {token}"}
    response = await client.post("/paths", headers=headers, json=data)
    assert response.status == status
    assert response.content_type == "application/json"
    return await response.json()


async def create_participation(client, token, path_id, status=201):
    headers = {'Authorization': f"Bearer {token}"}
    response = await client.post("/participations", headers=headers, json=dict(pathId=path_id))
    assert response.status == status
    assert response.content_type == "application/json"
    return await response.json()


async def get_learning_path(client, token, path_id, status=200):
    headers = {'Authorization': f"Bearer {token}"}
    response = await client.get(f"/paths/{path_id}", headers=headers)
    assert response.status == status
    assert response.content_type == "application/json"
    return await response.json()


async def update_learning_path(client, token, path, status=200):
    headers = {'Authorization': f"Bearer {token}"}
    response = await client.put(f"/paths/{path.get('id')}", headers=headers, json=path)
    assert response.status == status
    assert response.content_type == "application/json"
    return await response.json()
