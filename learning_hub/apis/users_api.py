from aiohttp import web

from learning_hub.usecases.create_user import CreateUserRequest


class UsersAPI:
    async def register_user(self, request):
        create_user = request.app.get("create_user")
        auth = request.app.get("auth")
        data = await request.json()
        create_user_request = self.create_user_request_from_json(data)
        try:
            result = await create_user.execute(create_user_request)
            token = auth.generate_token(result.user_id)
            return self.create_register_user_response(result, token)
        except ValueError as e:
            return self.create_error_response(list(e.args), 400)

    @staticmethod
    def create_user_request_from_json(data):
        return CreateUserRequest(
            email=data.get("email", ""),
            username=data.get("username", ""),
            password=data.get("password", ""))

    @staticmethod
    def create_register_user_response(result, token):
        return web.json_response(dict(
            userId=result.user_id,
            token=token),
            status=201)

    async def login(self, request):
        users = request.app.get("users")
        auth = request.app.get("auth")
        data = await request.json()
        user = await users.find_by_credentials(data.get("email", ""), data.get("password", ""))
        if not user:
            return self.create_error_response(["Invalid login credentials"], 400)
        token = auth.generate_token(user.id)
        return web.json_response(dict(userId=user.id, token=token))

    @staticmethod
    def create_error_response(errors, status):
        return web.json_response(dict(errors=errors), status=status)
