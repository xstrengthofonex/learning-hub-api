from learning_hub.apis.status_api import status_api


async def setup_routes(app):
    app.router.add_get("/status", status_api)


