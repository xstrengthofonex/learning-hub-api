from dataclasses import dataclass

from learning_hub.domain.participations import Participations, Participation, AssignmentParticipation
from learning_hub.domain.paths import Paths
from learning_hub.helpers import IdGenerator


class PathNotFound(RuntimeError):
    pass


@dataclass(frozen=True)
class CreateParticipationRequest:
    path_id: str
    user_id: str


@dataclass(frozen=True)
class CreateParticipationResponse:
    participation_id: str


class CreateParticipation:
    def __init__(self, participations: Participations, paths: Paths, ) -> None:
        self.paths = paths
        self.participations = participations
        self.id_generator = IdGenerator()

    async def execute(self, request: CreateParticipationRequest) -> CreateParticipationResponse:
        path = await self.paths.find_by_id(request.path_id)
        if not path:
            raise PathNotFound
        participation = Participation(
            id=self.id_generator.generate(),
            path_id=path.id,
            user_id=request.user_id,
            assignments=[AssignmentParticipation(
                id=self.id_generator.generate(), assignment_id=a.id)
                for a in path.assignments])
        await self.participations.add(participation)
        return CreateParticipationResponse(participation_id=participation.id)
