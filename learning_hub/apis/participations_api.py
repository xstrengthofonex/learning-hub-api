from aiohttp import web

from learning_hub.usecases.create_participation import CreateParticipationRequest, PathNotFound


class ParticipationsAPI:
    async def create_participation(self, request: web.Request) -> web.Response:
        create_participation = request.app.get("create_participation")
        data = await request.json()
        path_id = data.get("pathId")
        user_id = request.get("user_id")
        create_participation_request = CreateParticipationRequest(
            path_id=path_id, user_id=user_id)
        try:
            result = await create_participation.execute(create_participation_request)
        except PathNotFound:
            return web.json_response(dict(message="Learning path not found"), status=404)
        return web.json_response(dict(
            participationId=result.participation_id), status=201)
