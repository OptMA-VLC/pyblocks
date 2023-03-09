import copy
import pathlib
from types import ModuleType
from typing import Dict

from src.bdk.base_block import BaseBlock
import src.meow_sim.repository.block_repository.block_repository_helpers as helpers
import src.meow_sim.repository.block_repository.block_repository_exceptions as repo_exceptions
from src.bdk.block_distribution_id import BlockDistributionId
from src.meow_sim.entity.block_instance_id import BlockInstanceId
from src.meow_sim.repository.block_adapter.block_adapter import BlockAdapter
from src.meow_sim.repository.block_repository.indexing_result import IndexingResult, ResultItem


class BlockRepository:
    base_block_class = BaseBlock

    _indexed_blocks: Dict[BlockInstanceId, pathlib.Path]

    def __init__(self):
        self._indexed_blocks = {}

    def index_dir(self, path: pathlib.Path) -> IndexingResult:
        if not path.is_dir():
            raise repo_exceptions.NotADir(path)

        indexing_result = IndexingResult(path)
        for block_dir in helpers.get_subdirectories(path):
            if block_dir.name.startswith('__'):
                indexing_result.append(ResultItem.skipped(block_dir))
                continue

            try:
                dist_id = self.get_dist_id_from_path(block_dir)
                self._indexed_blocks[dist_id] = block_dir
                indexing_result.append(ResultItem.success(path, dist_id))
            except Exception as ex:
                indexing_result.append(ResultItem.failed(path, ex))

        return indexing_result

    def get_indexed_blocks(self) -> Dict[BlockDistributionId, pathlib.Path]:
        return copy.deepcopy(self._indexed_blocks)

    def get_class_from_dist_name(self, dist_name: BlockDistributionId) -> BaseBlock:
        try:
            path = self._indexed_blocks[dist_name]
        except KeyError:
            raise repo_exceptions.BlockDoesNotExist(dist_name)

        return self.get_class_from_path(path)

    def get_class_from_path(self, path: pathlib.Path) -> BaseBlock:
        if not path.is_dir():
            raise repo_exceptions.NotADir(path)

        block_py_path = path / 'block.py'
        if not block_py_path.exists():
            raise repo_exceptions.NoBlockPyFile(path)

        try:
            module = helpers.load_module('block', block_py_path)
        except Exception as ex:
            raise repo_exceptions.LoadModuleFailed(path) from ex

        return self._get_block_class(module)

    def get_dist_id_from_path(self, path: pathlib.Path) -> BlockInstanceId:
        block_class = self.get_class_from_path(path)
        adapter = BlockAdapter(block_class)
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
