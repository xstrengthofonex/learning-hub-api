from aiohttp import web


async def status_api(request):
    return web.json_response(dict(status="OK"))

