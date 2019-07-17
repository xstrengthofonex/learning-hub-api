
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


async def register_user(client, email=EMAIL, username=USERNAME, password=PASSWORD):
    data = dict(email=email, username=username, password=password)
    return await client.post("/users", json=data)


async def create_learning_path(client, token, title=TITLE, description=DESCRIPTION,
                               categories=CATEGORIES, assignments=ASSIGNMENTS):
    data = dict(token=token,
                title=title,
                description=description,
                categories=categories,
                assignments=assignments)
    return await client.post("/paths", json=data)

