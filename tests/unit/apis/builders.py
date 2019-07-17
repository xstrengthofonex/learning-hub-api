from dataclasses import field, dataclass
from typing import List

from learning_hub.usecases.create_path import CreateAssignmentRequest, CreatePathRequest
from learning_hub.usecases.create_user import CreateUserRequest


@dataclass
class CreateAssignmentRequestBuilder:
    name: str = "Name"
    resource: str = "http://resource.com"
    instructions: str = "Some Instructions"

    def build(self):
        return CreateAssignmentRequest(
            name=self.name,
            resource=self.resource,
            instructions=self.instructions)


@dataclass
class CreatePathRequestBuilder:
    author: str
    title: str = "Title"
    description: str = "Description"
    categories: List[str] = field(default_factory=list)
    assignments: List[CreateAssignmentRequest] = field(default_factory=list)

    def build(self):
        return CreatePathRequest(
            title=self.title,
            author=self.author,
            description=self.description,
            categories=self.categories,
            assignments=self.assignments)


@dataclass
class CreateUserRequestBuilder:
    username: str = "Username"
    password: str = "Password"
    email: str = "example@email.com"

    def build(self):
        return CreateUserRequest(
            username=self.username,
            password=self.password,
            email=self.email)
