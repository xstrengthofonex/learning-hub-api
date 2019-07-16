from dataclasses import dataclass
from typing import List

from learning_hub.domain.paths import Path, Assignment, PathValidator
from learning_hub.helpers import IdGenerator, Clock


@dataclass(frozen=True)
class CreatePathResponse:
    path_id: str


@dataclass(frozen=True)
class CreateAssignmentRequest:
    name: str
    resource: str
    instructions: str


@dataclass(frozen=True)
class CreatePathRequest:
    title: str
    author: str
    description: str
    categories: List[str]
    assignments: List[CreateAssignmentRequest]


class CreatePath:
    def __init__(self, paths):
        self.paths = paths
        self.path_validator = PathValidator()
        self.id_generator = IdGenerator()
        self.clock = Clock()

    async def execute(self, create_path_request: CreatePathRequest) -> CreatePathResponse:
        path = self.path_from_request(create_path_request)
        await self.path_validator.validate(path)
        await self.paths.add(path)
        return CreatePathResponse(path_id=path.id)

    def path_from_request(self, create_path_request):
        return Path(
            id=self.id_generator.generate(),
            title=create_path_request.title,
            author=create_path_request.author,
            created_on=self.clock.now(),
            updated_on=self.clock.now(),
            description=create_path_request.description,
            categories=create_path_request.categories,
            assignments=[Assignment(
                id=self.id_generator.generate(),
                name=a.name,
                resource=a.resource,
                instructions=a.instructions)
                for a in create_path_request.assignments])
