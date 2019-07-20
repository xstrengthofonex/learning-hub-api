from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import uuid4

from learning_hub.domain.participations import AssignmentParticipation, Participation
from learning_hub.domain.paths import Assignment, Path


@dataclass
class AssignmentBuilder:
    id: str = str(uuid4())
    name: str = "Assignment"
    resource: str = "http://resource.com"
    instructions: str = "Some instructions"

    def build(self):
        return Assignment(
            id=self.id,
            name=self.name,
            resource=self.resource,
            instructions=self.instructions)


@dataclass
class PathBuilder:
    author: str
    id: str = str(uuid4())
    title: str = "Title"
    description: str = "Some description"
    created_on: datetime = datetime.now()
    updated_on: datetime = datetime.now()
    categories: List[str] = field(default_factory=list)
    assignments: List[AssignmentBuilder] = field(default_factory=list)

    def build(self):
        return Path(
            id=self.id,
            title=self.title,
            description=self.description,
            author=self.author,
            created_on=self.created_on,
            updated_on=self.updated_on,
            categories=self.categories,
            assignments=[a.build() for a in self.assignments])


@dataclass
class AssignmentParticipationBuilder:
    assignment_id: str
    id: str = str(uuid4())
    is_complete: bool = False

    def build(self):
        return AssignmentParticipation(
            id=self.id,
            assignment_id=self.assignment_id,
            is_complete=self.is_complete)


@dataclass
class ParticipationBuilder:
    path_id: str
    user_id: str
    id: str = str(uuid4())
    assignments: List[AssignmentParticipationBuilder] = field(default_factory=list)

    def build(self):
        return Participation(
            id=self.id, path_id=self.path_id, user_id=self.user_id,
            assignments=[a.build() for a in self.assignments])
