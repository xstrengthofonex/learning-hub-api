from typing import Dict, Optional

from aiohttp import web
from aiohttp.web_middlewares import middleware

import settings
import jwt

WHITELIST_PATHS = ["/login", "/users", "/status"]
ALLOWED_METHODS = ["POST", "PUT", "DELETE", "GET"]


@middleware
async def auth_middleware(request: web.Request, handler):
    if request.path not in WHITELIST_PATHS and request.method in ALLOWED_METHODS:
        auth = request.app.get("auth")
        users = request.app.get("users")
        token = request.headers.get("Authorization")
        payload = auth.get_payload(token.replace("Bearer ", ""))
        if not payload:
            return web.json_response(dict(message="Token is not valid"), status=401)
        user_id = payload.get("userId")
        if not await users.find_by_id(user_id):
            return web.json_response(dict(message="User does not exist"), status=401)
        request["user_id"] = user_id
    return await handler(request)


class JWTAuth:
    def __init__(self, secret: str) -> None:
        self.secret = secret

    def generate_token(self, user_id) -> str:
        return jwt.encode(dict(userId=user_id), self.secret, algorithm="HS256").decode()

    def get_payload(self, token: str) -> Optional[Dict[str, str]]:
        try:
            payload = jwt.decode(token.encode(), self.secret, algorithms=["HS256"])
        except jwt.exceptions.DecodeError:
            return None
        return payload


async def setup_auth(app: web.Application) -> None:
    app["auth"] = JWTAuth(settings.SECRET_KEY)
