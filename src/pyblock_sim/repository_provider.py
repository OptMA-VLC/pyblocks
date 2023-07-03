from src.pyblock_sim.repository.block_repository.block_repository import BlockRepository
from src.pyblock_sim.repository.cli.cli import CLI
from src.pyblock_sim.repository.project_repository.project_repository import ProjectRepository
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository


class RepositoryProvider:
    block_repo: BlockRepository
    signal_repo: SignalRepository
    project_repo: ProjectRepository
    cli: CLI

    def __init__(self):
        self.cli = CLI()
        self.block_repo = BlockRepository()
        self.signal_repo = SignalRepository()
        self.project_repo = ProjectRepository()

