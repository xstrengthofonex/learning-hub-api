from typing import List

from aiohttp import web


class BaseAPI:
    @staticmethod
    def create_error_response(errors: List[str], status: int) -> web.Response:
        return web.json_response(dict(errors=errors), status=status)
