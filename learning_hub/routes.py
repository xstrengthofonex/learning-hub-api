from learning_hub.apis.status_api import status_api
from learning_hub.apis.users_api import UsersAPI
from learning_hub.usecases.create_user import CreateUser


async def setup_routes(app):
    app["create_user"] = CreateUser()
    users_api = UsersAPI()
    app.router.add_get("/status", status_api)
    app.router.add_post("/users", users_api.register_user)
