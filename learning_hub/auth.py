

class JWTAuthentication:
    def generate_token(self, user_id):
        raise NotImplementedError


async def setup_auth(app):
    app["auth"] = JWTAuthentication()
