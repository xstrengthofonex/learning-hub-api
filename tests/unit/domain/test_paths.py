

import pytest
from datetime import datetime

from learning_hub.domain.paths import Path, PathValidator, Assignment

VALIDATION_ERROR = ValueError
EMPTY_PATH = Path(
    id="id",
    title="",
    description="",
    author="author_id",
    created_on=datetime.now(),
    updated_on=datetime.now(),
    categories=[],
    assignments=[])
EMPTY_ASSIGNMENT = Assignment(
    id="id",
    name="",
    resource="",
    instructions="")


async def test_path_validator_does_not_accept_title_name_or_description():
    with pytest.raises(VALIDATION_ERROR) as e:
        path_validator = PathValidator()
        await path_validator.validate(EMPTY_PATH)
    assert all([m in str(e.value) for m in [
        "Title is required",
        "Description is required"]])


async def test_path_validator_does_not_accept_any_assignments_with_blank_details():
    with pytest.raises(AssertionError) as e:
        path_validator = PathValidator()
        await path_validator.validate_assignments([EMPTY_ASSIGNMENT])
    assert "Assignment name is required" in str(e.value)
