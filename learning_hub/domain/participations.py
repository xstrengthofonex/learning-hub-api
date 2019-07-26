from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class AssignmentParticipation:
    id: str
    assignment_id: str
    is_complete: bool = False


@dataclass(frozen=True)
class Participation:
    id: str
    path_id: str
    user_id: str
    assignments: List[AssignmentParticipation]


class Participations(ABC):
    @abstractmethod
    async def add(self, participation: Participation) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, id_: str) -> Participation:
        pass

    @abstractmethod
    async def find_participations_for_path_id(self, path_id: str) -> List[Participation]:
        pass
