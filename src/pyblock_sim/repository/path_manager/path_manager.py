import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PathManager:
    run_path: Path
    project_rel_path: Path
    block_library_rel_path: Path

    def get_project_absolute_path(self) -> Path:
        return Path(os.path.relpath(self.project_rel_path, self.run_path)).resolve()

    def get_block_library_absolute_path(self) -> Path:
        return Path(os.path.relpath(self.block_library_rel_path, self.run_path)).resolve()

    def resolve_relpath_from_project(self, rel_path: Path) -> Path:
        project_folder = self.get_project_absolute_path().parent
        return (project_folder / rel_path).resolve()
