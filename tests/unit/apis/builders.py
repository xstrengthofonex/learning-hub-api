from dataclasses import field, dataclass
from typing import List
from uuid import uuid4

from datetime import datetime

from learning_hub.usecases.create_path import CreateAssignmentRequest, CreatePathRequest
from learning_hub.usecases.create_user import CreateUserRequest
from learning_hub.usecases.update_path import UpdatePathRequest, UpdateAssignmentRequest


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


@dataclass
class UpdatePathRequestBuilder(CreatePathRequestBuilder):
    id: str = str(uuid4())
    created_on: datetime = datetime.now()
    updated_on: datetime = datetime.now()
    assignments: List[UpdateAssignmentRequest] = field(default_factory=list)

    def build(self):
        return UpdatePathRequest(
            id=self.id,
            created_on=self.created_on,
            updated_on=self.updated_on,
            title=self.title,
            author=self.author,
            description=self.description,
            categories=self.categories,
            assignments=self.assignments)
