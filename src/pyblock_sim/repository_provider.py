from pathlib import Path

from src.pyblock_sim.repository.block_repository.block_repository import BlockRepository
from src.pyblock_sim.repository.block_repository.block_repository_exceptions import NoBlockPyFile
from src.pyblock_sim.repository.block_repository.indexing_result import IndexingResult, ResultItem
from src.pyblock_sim.repository.project_repository.project_repository import ProjectRepository
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository
from src.pyblock_sim.util.logger import logger


class RepositoryProvider:
    block_repo: BlockRepository
    signal_repo: SignalRepository
    project_repo: ProjectRepository

    def __init__(self, library_path: Path):
        self.block_repo = BlockRepository(library_path)
        self.signal_repo = SignalRepository()
        self.project_repo = ProjectRepository()

        logger.info('Loading block library......... ', end='')
        indexing_result = self.block_repo.index_blocks()
        logger.info('[green]ok[/green]', no_tag=True)
        self._print_indexing_result(indexing_result)

    def _print_indexing_result(self, result: IndexingResult):
        logger.verbose(f'Checked {result.indexed_path.absolute()} for blocks')

        for item in result.items:
            if item.outcome is ResultItem.ResultType.SUCCESS:
                logger.verbose(f'  /{item.path.name.ljust(20)} - [green]Success[/green]')
            elif item.outcome is ResultItem.ResultType.FAILED:
                if isinstance(item.exception, NoBlockPyFile):
                    logger.verbose(f'  /{item.path.name.ljust(20)} - [white]Not a Block[/white]')
                else:
                    logger.verbose(f'  /{item.path.name.ljust(20)} - [red]Failed[/red]')
                    logger.verbose(f'    (failed with exception {item.exception.__class__.__name__} - {item.exception})')
            elif item.outcome is ResultItem.ResultType.SKIPPED:
                logger.verbose(f'  /{item.path.name.ljust(20)} - [white]Skipped[/white]')
