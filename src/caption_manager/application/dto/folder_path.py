from pathlib import Path

class FolderPath:
    def __init__(self, path: Path):
        self.path = path

    def __hash__(self) -> int:
        return hash(self.path)

    def __eq__(self, other: object) -> bool:
        return self.path == other.path if isinstance(other, FolderPath) else False
