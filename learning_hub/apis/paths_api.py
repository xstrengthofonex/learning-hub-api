from aiohttp import web

from learning_hub.apis.base_api import BaseAPI
from learning_hub.usecases.create_path import CreatePathRequest, CreateAssignmentRequest


class PathsAPI(BaseAPI):
    async def create_path(self, request: web.Request) -> web.Response:
        create_path = request.app.get("create_path")
        user_id = request.get("user_id")
        data = await request.json()
        create_path_request = self.create_path_request_from(data, user_id)
        try:
            result = await create_path.execute(create_path_request)
        except ValueError as e:
            return self.create_error_response(list(e.args[0]), 400)
        return web.json_response(dict(pathId=result.path_id), status=201)

    @staticmethod
    def create_path_request_from(data, user_id):
        return CreatePathRequest(
            title=data.get("title", ""),
            author=user_id,
            description=data.get("description", ""),
            categories=data.get("categories", []),
            assignments=[CreateAssignmentRequest(
                name=a.get("name", ""),
                resource=a.get("resource", ""),
                instructions=a.get("instructions", ""))
                for a in data.get("assignments", [])])