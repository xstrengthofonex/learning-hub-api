from aiohttp import web


class PathsAPI:
    async def create_path(self, request: web.Request) -> web.Response:
        return web.json_response(dict())