from uuid import uuid4

from datetime import datetime

from learning_hub.domain.paths import Path
from learning_hub.repositories.in_memory_paths import InMemoryPaths

PATH_ID = str(uuid4())
AUTHOR = str(uuid4())
TITLE = "Title"
DESCRIPTION = "Description"
CREATED_ON = datetime.now()
UPDATED_ON = datetime.now()
CATEGORIES = []
ASSIGNMENTS = []
PATH = Path(
    id=PATH_ID,
    title=TITLE,
    author=AUTHOR,
    description=DESCRIPTION,
    created_on=CREATED_ON,
    updated_on=UPDATED_ON,
    categories=CATEGORIES,
    assignments=ASSIGNMENTS)


async def test_find_by_id_returns_path():
    paths = InMemoryPaths()
    await paths.add(PATH)
    result = await paths.find_by_id(PATH_ID)
    assert result == PATH
