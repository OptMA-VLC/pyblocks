from typing import Type

from src.pyblock_sim.entity.block_library.indexing_result import IndexingResult, ResultItem
from src.pyblock_sim.repository.block_repository.block_repository_exceptions import NoBlockPyFile
from src.pyblock_sim.repository.cli.object_printer import ObjectPrinter
from src.pyblock_sim.util.logger import logger


class IndexingResultPrinter(ObjectPrinter):
    def get_type(self) -> Type:
        return IndexingResult

    def print(self, result: IndexingResult, **kwargs):
        s = ''
        s += f'Checked {result.indexed_path.absolute()} for blocks\n'

        for item in result.items:
            if item.outcome is ResultItem.ResultType.SUCCESS:
                s += f'  /{item.path.name.ljust(20)} - [green]Success[/green]\n'
            elif item.outcome is ResultItem.ResultType.FAILED:
                if isinstance(item.exception, NoBlockPyFile):
                    s += f'  /{item.path.name.ljust(20)} - [white]Not a Block[/white]\n'
                else:
                    s += f'  /{item.path.name.ljust(20)} - [red]Failed[/red]\n'
                    s += f'    (failed with exception {item.exception.__class__.__name__} - {item.exception})\n'
            elif item.outcome is ResultItem.ResultType.SKIPPED:
                s += f'  /{item.path.name.ljust(20)} - [white]Skipped[/white]\n'

        return s
