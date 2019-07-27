from aiohttp import web
from datetime import datetime

from learning_hub.apis.base_api import BaseAPI
from learning_hub.usecases.create_path import CreatePathRequest, CreateAssignmentRequest
from learning_hub.usecases.update_path import UpdatePathRequest, UpdateAssignmentRequest


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

    async def get_path(self, request: web.Request) -> web.Response:
        path_id = request.match_info.get("path_id")
        paths = request.app.get("paths")
        path = await paths.find_by_id(path_id)
        if not path:
            return web.json_response(dict(message="Learning path not found"), status=404)
        return self.create_get_path_response(path)

    async def update_path(self, request: web.Request) -> web.Response:
        update_path = request.app.get("update_path")
        user_id = request.get("user_id")
        data = await request.json()
        if user_id != data.get("author"):
            return web.json_response(dict(message="Update Request Forbidden"), status=403)
        update_path_request = self.update_path_request_from(data)
        try:
            result = await update_path.execute(update_path_request)
        except ValueError as e:
            return self.create_error_response(list(e.args[0]), 400)
        if not result.path:
            return web.json_response(dict(message="Learning path not found"), status=404)
        return self.create_get_path_response(result.path)

    @staticmethod
    def update_path_request_from(data):
        return UpdatePathRequest(
            id=data.get("id", ""),
            title=data.get("title", ""),
            author=data.get("author", ""),
            created_on=datetime.fromtimestamp(data.get("created_on", 0.0)),
            updated_on=datetime.fromtimestamp(data.get("updated_on", 0.0)),
            description=data.get("description", ""),
            categories=data.get("categories", []),
            assignments=[UpdateAssignmentRequest(
                id=a.get("id", ""),
                name=a.get("name", ""),
                resource=a.get("resource", ""),
                instructions=a.get("instructions", "")
            ) for a in data.get("assignments", [])])

    @staticmethod
    def create_get_path_response(path):
        return web.json_response(dict(
            id=path.id,
            author=path.author,
            title=path.title,
            created_on=path.created_on.timestamp(),
            updated_on=path.updated_on.timestamp(),
            description=path.description,
            categories=path.categories,
            assignments=[dict(
                id=a.id,
                name=a.name,
                resource=a.resource,
                instructions=a.instructions)
                for a in path.assignments],
            ), status=200)

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


