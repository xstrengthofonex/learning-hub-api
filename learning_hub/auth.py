from typing import Dict

import settings
import jwt


class JWTAuth:
    def __init__(self, secret):
        self.secret = secret

    def generate_token(self, user_id) -> str:
        return jwt.encode(dict(userId=user_id), self.secret, algorithm="HS256").decode()

    def get_payload(self, token: str) -> Dict[str, str]:
        return jwt.decode(token.encode(), self.secret, algorithms=["HS256"])


async def setup_auth(app):
    app["auth"] = JWTAuth(settings.SECRET_KEY)
