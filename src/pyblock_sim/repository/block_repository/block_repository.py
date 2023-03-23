import copy
import pathlib
from types import ModuleType
from typing import Dict

import src.pyblock_sim.repository.block_repository.block_repository_exceptions as repo_exceptions
import src.pyblock_sim.repository.block_repository.block_repository_helpers as helpers
from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_distribution_id import BlockDistributionId
from src.pyblock_sim.block_runtime.block_runtime.block_runtime import BlockRuntime
from src.pyblock_sim.entity.block.block_entity import BlockEntity
from src.pyblock_sim.entity.block.interface_block_runtime import IBlockRuntime
from src.pyblock_sim.repository.block_repository.indexing_result import IndexingResult, ResultItem
from src.pyblock_sim.repository.block_repository.interface_block_repository import IBlockRepository


class BlockRepository(IBlockRepository):
    _indexed_blocks: Dict[BlockDistributionId, pathlib.Path]
    _block_library_path: pathlib.Path

    def __init__(self, block_library_path: pathlib.Path):
        self._block_library_path = block_library_path
        self._indexed_blocks = {}

    def index_blocks(self) -> IndexingResult:
        if not self._block_library_path.is_dir():
            raise repo_exceptions.NotADir(self._block_library_path)

        indexing_result = IndexingResult(self._block_library_path)
        for block_dir in helpers.get_subdirectories(self._block_library_path):
            if block_dir.name.startswith('__'):
                indexing_result.append(ResultItem.skipped(block_dir))
                continue

            try:
                dist_id = self._get_dist_id_from_path(block_dir)
                self._indexed_blocks[dist_id] = block_dir
                indexing_result.append(ResultItem.success(block_dir, dist_id))
            except Exception as ex:
                indexing_result.append(ResultItem.failed(block_dir, ex))

        return indexing_result

    def list_blocks(self) -> Dict[BlockDistributionId, pathlib.Path]:
        return copy.deepcopy(self._indexed_blocks)

    def is_block_known(self, distribution_id: BlockDistributionId) -> bool:
        return distribution_id in self._indexed_blocks

    def get_runtime(self, dist_id: BlockDistributionId) -> IBlockRuntime:
        if isinstance(dist_id, str):
            dist_id = BlockDistributionId(dist_id)

        try:
            path = self._indexed_blocks[dist_id]
        except KeyError:
            raise repo_exceptions.BlockDoesNotExist(dist_id)

        block_class = self._get_class_from_path(path)
        return BlockRuntime(block_class)

    def _get_dist_id_from_path(self, path: pathlib.Path) -> BlockDistributionId:
        block_class = self._get_class_from_path(path)
        runtime = BlockRuntime(block_class)
        distribution_id = runtime.distribution_id
        del runtime
        return distribution_id

    def _get_class_from_path(self, path: pathlib.Path) -> BaseBlock:
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

    def _get_block_class(self, module: ModuleType) -> BaseBlock:
        try:
            classes = helpers.get_classes(module)
            block_classes = helpers.filter_subclasses_of(classes, BaseBlock)
        except Exception as ex:
            raise repo_exceptions.LoadBlockClassFailed(
                f'Exception {type(ex).__name__} raised while getting classes in block.py module'
            ) from ex

        if len(block_classes) == 0:
            raise repo_exceptions.NoBlockClassFound()

        if len(block_classes) > 1:
            raise repo_exceptions.MultipleBlockClassesInFile()

        return block_classes[0]
