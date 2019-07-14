from typing import Dict

from aiohttp import web

import settings
import jwt


class JWTAuth:
    def __init__(self, secret: str) -> None:
        self.secret = secret

    def generate_token(self, user_id) -> str:
        return jwt.encode(dict(userId=user_id), self.secret, algorithm="HS256").decode()

    def get_payload(self, token: str) -> Dict[str, str]:
        return jwt.decode(token.encode(), self.secret, algorithms=["HS256"])


async def setup_auth(app: web.Application) -> None:
    app["auth"] = JWTAuth(settings.SECRET_KEY)
