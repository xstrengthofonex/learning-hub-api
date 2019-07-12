from aiohttp import web

from learning_hub.auth import setup_auth
from learning_hub.routes import setup_routes


async def create_app():
    app = web.Application()
    await setup_auth(app)
    await setup_routes(app)
    return app


if __name__ == '__main__':
    web.run_app(create_app(), port=3000)
