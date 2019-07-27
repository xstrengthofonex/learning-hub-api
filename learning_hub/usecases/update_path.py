from dataclasses import dataclass

from datetime import datetime
from typing import List, Optional

from learning_hub.domain.paths import Path, PathValidator, Assignment
from learning_hub.helpers import IdGenerator, Clock
from learning_hub.usecases.create_path import CreatePathRequest, CreateAssignmentRequest


class PathNotFound(RuntimeError):
    pass


@dataclass(frozen=True)
class UpdateAssignmentRequest(CreateAssignmentRequest):
    id: Optional[str] = None


@dataclass(frozen=True)
class UpdatePathRequest(CreatePathRequest):
    id: str
    created_on: datetime
    updated_on: datetime
    assignments: List[UpdateAssignmentRequest]


@dataclass(frozen=True)
class UpdatePathResponse:
    path: Path


class UpdatePath:
    def __init__(self, paths):
        self.paths = paths
        self.path_validator = PathValidator()
        self.id_generator = IdGenerator()
        self.clock = Clock()

    async def execute(self, request: UpdatePathRequest) -> UpdatePathResponse:
        if not await self.paths.find_by_id(request.id):
            raise PathNotFound
        path = Path(
            id=request.id,
            title=request.title,
            created_on=request.created_on,
            updated_on=self.clock.now(),
            author=request.author,
            description=request.description,
            categories=request.categories,
            assignments=[Assignment(
                id=a.id or self.id_generator.generate(),
                name=a.name,
                resource=a.resource,
                instructions=a.instructions)
                for a in request.assignments])
        await self.path_validator.validate(path)
        await self.paths.add(path)
        return UpdatePathResponse(path)
