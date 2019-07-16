from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from datetime import datetime

from learning_hub.domain.common import Entity, Validator


@dataclass(frozen=True)
class Assignment(Entity):
    name: str
    resource: str
    instructions: str


@dataclass(frozen=True)
class Path(Entity):
    title: str
    description: str
    author: str
    created_on: datetime
    updated_on: datetime
    categories: List[str]
    assignments: List[Assignment]


class PathValidator(Validator):
    @staticmethod
    async def validate_title(title: str) -> None:
        assert title != "", "Title is required"

    @staticmethod
    async def validate_description(description: str) -> None:
        assert description != "", "Description is required"

    @staticmethod
    async def validate_assignments(assignments: List[Assignment]) -> None:
        for assignment in assignments:
            assert assignment.name != "", "Assignment name is required"


class Paths(ABC):
    @abstractmethod
    async def add(self, path: Path) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, path_id: str) -> Path:
        pass

