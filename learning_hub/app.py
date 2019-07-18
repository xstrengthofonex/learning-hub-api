from aiohttp import web
from aiohttp.web_middlewares import middleware

from learning_hub.auth import setup_auth, auth_middleware
from learning_hub.routes import setup_routes


@middleware
async def cors_middleware(request: web.Request, handler) -> web.Response:
    response = await handler(request)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, DELETE, PUT, PATCH, OPTIONS")
    return response


async def create_app() -> web.Application:
    app = web.Application(middlewares=[auth_middleware, cors_middleware])
    await setup_auth(app)
    await setup_routes(app)
    return app


if __name__ == '__main__':
    web.run_app(create_app(), port=3000)
