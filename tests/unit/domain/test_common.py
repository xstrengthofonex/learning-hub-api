import pytest

from learning_hub.domain.common import Entity, EntityValidator


async def test_validator_runs_all_validators():
    with pytest.raises(ValueError) as e:
        entity = Entity("")
        validator = EntityValidator()
        await validator.validate(entity)
    assert "Id cannot be blank" in str(e.value)
