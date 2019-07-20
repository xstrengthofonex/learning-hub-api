from uuid import uuid4

import pytest
from asynctest import Mock

from learning_hub.domain.participations import Participations, Participation, AssignmentParticipation
from learning_hub.domain.paths import Paths
from learning_hub.helpers import IdGenerator
from learning_hub.usecases.create_participation import CreateParticipation, CreateParticipationRequest, PathNotFound
from tests.unit.builders import PathBuilder, AssignmentBuilder


USER_ID = str(uuid4())
PATH = PathBuilder(author=USER_ID, categories=["Category"], assignments=[AssignmentBuilder()])
PARTICIPATION_ID = str(uuid4())
CREATE_PARTICIPATION_REQUEST = CreateParticipationRequest(path_id=PATH.id, user_id=USER_ID)
ASSIGNMENT_PARTICIPATION_ID = str(uuid4())
PARTICIPATION = Participation(
    id=PARTICIPATION_ID,
    user_id=USER_ID,
    path_id=PATH.id,
    assignments=[AssignmentParticipation(
        id=ASSIGNMENT_PARTICIPATION_ID, assignment_id=a.id)
        for a in PATH.assignments])


async def test_create_new_participation():
    participations = Mock(Participations)
    paths = Mock(Paths)
    paths.find_by_id.return_value = PATH
    usecase = CreateParticipation(participations, paths)
    usecase.id_generator = Mock(IdGenerator)
    usecase.id_generator.generate.side_effect = [
        PARTICIPATION_ID, ASSIGNMENT_PARTICIPATION_ID]

    result = await usecase.execute(CREATE_PARTICIPATION_REQUEST)

    participations.add.assert_called_with(PARTICIPATION)
    assert result.participation_id == PARTICIPATION_ID


async def test_raises_path_not_found_if_path_does_not_exist():
    participations = Mock(Participations)
    paths = Mock(Paths)
    usecase = CreateParticipation(participations, paths)
    paths.find_by_id.return_value = None
    with pytest.raises(PathNotFound):
        await usecase.execute(CREATE_PARTICIPATION_REQUEST)
