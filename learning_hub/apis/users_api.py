from aiohttp import web

from learning_hub.usecases.create_user import CreateUserRequest


class UsersAPI:
    async def register_user(self, request):
        create_user = request.app.get("create_user")
        auth = request.app.get("auth")
        data = await request.json()
        create_user_request = CreateUserRequest(**data)
        result = await create_user.execute(create_user_request)
        token = auth.generate_token(result.user_id)
        return web.json_response(dict(
            userId=result.user_id,
            token=token),
            status=201)
