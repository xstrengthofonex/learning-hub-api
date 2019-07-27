from aiohttp import web

from learning_hub.apis.participations_api import ParticipationsAPI
from learning_hub.apis.paths_api import PathsAPI
from learning_hub.apis.status_api import status_api
from learning_hub.apis.users_api import UsersAPI
from learning_hub.repositories.in_memory_participations import InMemoryParticipations
from learning_hub.repositories.in_memory_paths import InMemoryPaths
from learning_hub.repositories.in_memory_users import InMemoryUsers
from learning_hub.usecases.create_participation import CreateParticipation
from learning_hub.usecases.create_path import CreatePath
from learning_hub.usecases.create_user import CreateUser
from learning_hub.usecases.update_path import UpdatePath


async def setup_usecases(app: web.Application) -> None:
    users = InMemoryUsers()
    paths = InMemoryPaths()
    participations = InMemoryParticipations()
    app["users"] = users
    app["paths"] = paths
    app["participations"] = participations
    app["create_participation"] = CreateParticipation(participations, paths)
    app["create_user"] = CreateUser(users)
    app["create_path"] = CreatePath(paths)
    app["update_path"] = UpdatePath(paths)


async def setup_routes(app: web.Application) -> None:
    await setup_usecases(app)
    users_api = UsersAPI()
    paths_api = PathsAPI()
    participations_api = ParticipationsAPI()

    app.router.add_get("/status", status_api)
    app.router.add_post("/users", users_api.register_user)
    app.router.add_post("/login", users_api.login)
    app.router.add_post("/paths", paths_api.create_path)
    app.router.add_get("/paths/{path_id}", paths_api.get_path)
    app.router.add_put("/paths/{path_id}", paths_api.update_path)
    app.router.add_post("/participations", participations_api.create_participation)
