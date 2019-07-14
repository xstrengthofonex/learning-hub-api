import pytest

from learning_hub.domain.common import Entity, Validator


class EntityValidator(Validator):
    async def validate_id(self, entity_id: str) -> None:
        self.assert_not_blank(entity_id, "Id cannot be blank")


async def test_validator_runs_all_validators():
    with pytest.raises(ValueError) as e:
        entity = Entity("")
        validator = EntityValidator()
        await validator.validate(entity)
    assert "Id cannot be blank" in str(e.value)


