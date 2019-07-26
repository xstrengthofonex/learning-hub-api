from learning_hub.repositories.in_memory_participations import InMemoryParticipations
from tests.unit.builders import ParticipationBuilder


async def test_participation_is_added():
    p = ParticipationBuilder("path1", "UserId1").build()
    participations = InMemoryParticipations()
    await participations.add(p)
    assert await participations.find_by_id(p.id) == p


async def test_find_participants_for_path_id():
    p1 = ParticipationBuilder(id="1", path_id="path1", user_id="UserId1").build()
    p2 = ParticipationBuilder(id="2", path_id="path1", user_id="UserId2").build()
    participations = InMemoryParticipations()
    await participations.add(p1)
    await participations.add(p2)
    result = await participations.find_participations_for_path_id(p1.path_id)
    assert len(result) == 2
