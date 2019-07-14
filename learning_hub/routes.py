from aiohttp import web

from learning_hub.apis.status_api import status_api
from learning_hub.apis.users_api import UsersAPI
from learning_hub.repositories.in_memory_users import InMemoryUsers
from learning_hub.usecases.create_user import CreateUser


async def setup_usecases(app: web.Application) -> None:
    users = InMemoryUsers()
    app["users"] = users
    app["create_user"] = CreateUser(users)


async def setup_routes(app: web.Application) -> None:
    await setup_usecases(app)
    users_api = UsersAPI()
    app.router.add_get("/status", status_api)
    app.router.add_post("/users", users_api.register_user)
    app.router.add_post("/login", users_api.login)
