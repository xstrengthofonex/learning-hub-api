from typing import Dict

from learning_hub.domain.paths import Paths, Path


class InMemoryPaths(Paths):
    def __init__(self):
        self.paths: Dict[str, Path] = dict()

    async def find_by_id(self, path_id: str) -> Path:
        return self.paths.get(path_id)

    async def add(self, path: Path) -> None:
        self.paths[path.id] = path
