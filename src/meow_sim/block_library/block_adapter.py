import pathlib
from types import ModuleType

from src.bdk.base_block import BaseBlock
from src.meow_sim import util
from src.meow_sim.block_library.block_exceptions import BlockExceptions
from src.meow_sim.util import modules


class BlockAdapter:
    base_block_class = BaseBlock

    _block_class: BaseBlock

    def __init__(self, path: pathlib.Path):
        if not path.is_dir():
            raise BlockExceptions.NotADir(path)

        block_py_path = path/'block.py'
        if not block_py_path.exists():
            raise BlockExceptions.NoBlockPyFile(path)

        try:
            module = util.modules.load_module('block', block_py_path)
        except Exception as ex:
            raise BlockExceptions.LoadModuleFailed(path) from ex

        self._block_class = self._get_block_class(module)

    def _get_block_class(self, module: ModuleType) -> BaseBlock:
        try:
            classes = util.modules.get_classes(module)
            block_classes = util.modules.filter_subclasses_of(classes, BlockAdapter.base_block_class)
        except Exception as ex:
            raise BlockExceptions.LoadBlockClassFailed(
                f'Exception {type(ex).__name__} raised while getting classes in block.py module'
            ) from ex

        if len(block_classes) == 0:
            raise BlockExceptions.LoadBlockClassFailed(
                f'No class inheriting from {BlockAdapter.base_block_class.__name__} found in block.py file'
            )

        if len(block_classes) > 1:
            raise BlockExceptions.LoadBlockClassFailed(
                f'More than one class inheriting from {BlockAdapter.base_block_class.__name__} found in block.py file'
            )

        return block_classes[0]
