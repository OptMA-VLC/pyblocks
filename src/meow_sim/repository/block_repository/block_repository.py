import copy
import pathlib
from types import ModuleType
from typing import Dict

from src.bdk.base_block import BaseBlock
import src.meow_sim.repository.block_repository.block_repository_helpers as helpers
import src.meow_sim.repository.block_repository.block_repository_exceptions as repo_exceptions
from src.bdk.block_distribution_id import BlockDistributionId
from src.meow_sim.entity.block_id import BlockId
from src.meow_sim.logger import logger
from src.meow_sim.repository.block_adapter.block_adapter import BlockAdapter


class BlockRepository:
    base_block_class = BaseBlock

    _indexed_blocks: Dict[BlockId, pathlib.Path]

    def __init__(self):
        self._indexed_blocks = {}

    def index_dir(self, path: pathlib.Path, raise_exceptions=False):
        if not path.is_dir():
            raise repo_exceptions.NotADir(path)

        logger.verbose(f'Checking {path.absolute()} for blocks')

        for block_dir in helpers.get_subdirectories(path):
            if block_dir.name.startswith('__'):
                logger.verbose(f'  /{block_dir.name.ljust(20)} - Skipping because it starts with __')
                continue

            try:
                dist_name = self.get_dist_name_from_path(block_dir)
                self._indexed_blocks[dist_name] = block_dir
                logger.verbose(f'  /{block_dir.name.ljust(20)} - [green]Indexed[/green]')
            except Exception as ex:
                logger.verbose(f'  /{block_dir.name.ljust(20)} - [red]Failed[/red]  ({ex})')
                if raise_exceptions:
                    raise

    def get_indexed_blocks(self) -> Dict[BlockDistributionId, pathlib.Path]:
        return copy.deepcopy(self._indexed_blocks)

    def load_by_dist_name(self, dist_name: BlockDistributionId) -> BlockAdapter:
        try:
            path = self._indexed_blocks[dist_name]
        except KeyError:
            raise repo_exceptions.BlockDoesNotExist(dist_name)

        return self.load_from_path(path)

    def load_from_path(self, path: pathlib.Path):
        if not path.is_dir():
            raise repo_exceptions.NotADir(path)

        block_py_path = path / 'block.py'
        if not block_py_path.exists():
            raise repo_exceptions.NoBlockPyFile(path)

        try:
            module = helpers.load_module('block', block_py_path)
        except Exception as ex:
            raise repo_exceptions.LoadModuleFailed(path) from ex

        block_class = self._get_block_class(module)

        return BlockAdapter(block_class)

    def get_dist_name_from_path(self, path: pathlib.Path) -> BlockId:
        adapter = self.load_from_path(path)
        name = adapter.distribution_id
        del adapter
        return name

    def _get_block_class(self, module: ModuleType) -> BaseBlock:
        try:
            classes = helpers.get_classes(module)
            block_classes = helpers.filter_subclasses_of(classes, BlockRepository.base_block_class)
        except Exception as ex:
            raise repo_exceptions.LoadBlockClassFailed(
                f'Exception {type(ex).__name__} raised while getting classes in block.py module'
            ) from ex

        if len(block_classes) == 0:
            raise repo_exceptions.NoBlockClassFound()

        if len(block_classes) > 1:
            raise repo_exceptions.MultipleBlockClassesInFile()

        return block_classes[0]
