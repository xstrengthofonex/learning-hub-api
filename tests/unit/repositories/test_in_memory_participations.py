from learning_hub.repositories.in_memory_participations import InMemoryParticipations
from tests.unit.builders import ParticipationBuilder


async def test_participation_is_added():
    p = ParticipationBuilder("path1", "UserId1").build()
    participations = InMemoryParticipations()
    await participations.add(p)
    assert await participations.find_by_id(p.id) == p
