from learning_hub.apis.status_api import status_api
from learning_hub.apis.users_api import UsersAPI
from learning_hub.repositories.in_memory_users import InMemoryUsers
from learning_hub.usecases.create_user import CreateUser
from learning_hub.usecases.helpers import IdGenerator


async def setup_usecases(app):
    users = InMemoryUsers()
    id_generator = IdGenerator()
    app["create_user"] = CreateUser(users, id_generator)


async def setup_routes(app):
    await setup_usecases(app)
    users_api = UsersAPI()
    app.router.add_get("/status", status_api)
    app.router.add_post("/users", users_api.register_user)
