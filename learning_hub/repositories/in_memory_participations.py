from typing import Dict, List

from learning_hub.domain.participations import Participations, Participation


class InMemoryParticipations(Participations):
    def __init__(self):
        self.participations: Dict[str, Participation] = dict()

    async def add(self, participation: Participation) -> None:
        self.participations[participation.id] = participation

    async def find_by_id(self, id_: str) -> Participation:
        return self.participations.get(id_, None)

    async def find_participations_for_path_id(self, path_id: str) -> List[Participation]:
        return [p for p in self.participations.values() if p.path_id == path_id]
