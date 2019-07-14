from aiohttp import web


async def status_api(request: web.Request) -> web.Response:
    return web.json_response(dict(status="OK"))

