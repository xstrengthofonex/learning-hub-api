from aiohttp import web

from learning_hub.apis.paths_api import PathsAPI
from learning_hub.apis.status_api import status_api
from learning_hub.apis.users_api import UsersAPI
from learning_hub.repositories.in_memory_paths import InMemoryPaths
from learning_hub.repositories.in_memory_users import InMemoryUsers
from learning_hub.usecases.create_path import CreatePath
from learning_hub.usecases.create_user import CreateUser


async def setup_usecases(app: web.Application) -> None:
    users = InMemoryUsers()
    paths = InMemoryPaths()
    app["users"] = users
    app["create_user"] = CreateUser(users)
    app["create_path"] = CreatePath(paths)


async def setup_routes(app: web.Application) -> None:
    await setup_usecases(app)
    users_api = UsersAPI()
    paths_api = PathsAPI()
    app.router.add_get("/status", status_api)
    app.router.add_post("/users", users_api.register_user)
    app.router.add_post("/login", users_api.login)
    app.router.add_post("/paths", paths_api.create_path)
