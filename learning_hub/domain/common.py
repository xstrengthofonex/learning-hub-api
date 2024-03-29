from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Entity:
    id: str


class Validator:
    DEFAULT_MESSAGE = "{} if invalid"

    async def validate(self, entity: Entity) -> None:
        errors = []
        validator_names = self._get_all_validator_methods()
        for validator_name in validator_names:
            errors.extend(await self._run_validator(entity, validator_name))
        if errors:
            raise ValueError(errors)

    async def _run_validator(self, entity, validator_name) -> List[str]:
        errors = []
        attribute_name = validator_name.split("validate_")[1]
        attribute = getattr(entity, attribute_name)
        validator = getattr(self, validator_name)
        try:
            await validator(attribute)
        except AssertionError as e:
            if len(e.args) >= 1:
                errors.append(e.args[0])
            else:
                errors.append(self.DEFAULT_MESSAGE.format(attribute_name))
        return errors

    def _get_all_validator_methods(self) -> List[str]:
        return [m for m in dir(self) if m.startswith("validate_")]

    @staticmethod
    def assert_not_blank(attribute, message) -> None:
        assert attribute != "", message

