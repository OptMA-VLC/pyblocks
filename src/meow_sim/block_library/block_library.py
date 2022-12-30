import pathlib
from typing import List

from src.bdk.base_block import BaseBlock
from src.meow_sim.block_library.block_adapter import BlockAdapter
from src.meow_sim.logger import logger


class BlockLibrary:
    BLOCK_PATH = pathlib.Path('./blocks')

    _blocks: List[BaseBlock]

    def __init__(self):
        self._blocks = []

    def load_from_dir(self, path: pathlib.Path):
        logger.verbose(f'Checking {path.absolute()} for blocks')

        for block_dir in self._get_subdirectories(path):
            if block_dir.name.startswith('__'):
                logger.verbose(f'  /{block_dir.name.ljust(20)} - Skipping because it starts with __')
                continue

            try:
                adapter = BlockAdapter(block_dir)
                self._blocks.append(adapter)
                logger.verbose(f'  /{block_dir.name.ljust(20)} - [green]Loaded[/green]')
            except Exception as ex:
                logger.verbose(f'  /{block_dir.name.ljust(20)} - [red]Failed[/red]')
                logger.error(f'Error loading block from {block_dir.resolve()} - {str(ex)}')

    def len(self):
        return len(self._blocks)

    def __len__(self):
        return self.len()

    @staticmethod
    def _get_subdirectories(path: pathlib.Path) -> List[pathlib.Path]:
        return [path for path in path.iterdir() if path.is_dir()]

