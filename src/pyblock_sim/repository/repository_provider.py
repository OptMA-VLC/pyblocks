from src.pyblock_sim.repository.block_repository.block_repository import BlockRepository
from src.pyblock_sim.repository.cli.cli import CLI
from src.pyblock_sim.repository.path_manager.path_manager import PathManager
from src.pyblock_sim.repository.project_repository.project_repository import ProjectRepository
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository


class RepositoryProvider:
    cli: CLI
    block_repo: BlockRepository
    signal_repo: SignalRepository
    project_repo: ProjectRepository
    path_manager: PathManager

    def __init__(
            self,
            cli: CLI = CLI(),
            block_repo: BlockRepository = BlockRepository(),
            signal_repo: SignalRepository = SignalRepository(),
            project_repo: ProjectRepository = ProjectRepository(),
            path_manager: PathManager = None
    ):
        self.cli = cli
        self.block_repo = block_repo
        self.signal_repo = signal_repo
        self.project_repo = project_repo
        self.path_manager = path_manager

