from dataclasses import dataclass, field

from datetime import datetime
from typing import List, Optional

from learning_hub.domain.paths import Path
from learning_hub.usecases.create_path import CreatePathRequest, CreateAssignmentRequest


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
    async def execute(self, request: UpdatePathRequest) -> UpdatePathResponse:
        raise NotImplementedError
