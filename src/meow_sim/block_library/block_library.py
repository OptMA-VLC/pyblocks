import importlib.util
import inspect
import pathlib
from types import ModuleType
from typing import List, Any

from src.bdk.base_block import BaseBlock
from src.meow_sim.logger import logger


class BlockAdapter:
    @staticmethod
    def is_block_dir(path: pathlib.Path):
        if not path.is_dir():
            return False

        if not (path/'block.py').exists():
            return False

        try:
            module = BlockAdapter._load_module('block', path/'block.py')
        except Exception as ex:
            logger.error(f'Error loading block.py for block directory /{path.name}')
            logger.error(ex)
            raise

        try:
            classes = BlockAdapter._get_classes(module)
            block_classes = BlockAdapter._filter_subclasses_of(classes, BaseBlock)
            assert(len(classes) == 1, 'File block.py should only declare one subclass of BaseBlock')
            logger.info(f'I have class {block_classes[0]}')
            block_class = block_classes[0]
            block = block_class()
            block.run(None, None)
        except Exception as ex:
            logger.error(f'Error loading classes in /{path.name}/block.py')
            logger.error(ex)
            raise

        return True

    @staticmethod
    def _load_module(name: str, path: pathlib.Path) -> ModuleType:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module

    @staticmethod
    def _get_classes(module: ModuleType) -> List[Any]:
        module_classes = []
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                is_declared_in_this_module = (obj.__module__ == module.__name__)
                if is_declared_in_this_module:
                    module_classes.append(obj)

        return module_classes

    @staticmethod
    def _filter_subclasses_of(classes: List[Any], base_class: Any):
        filtered = []
        for cls in classes:
            if issubclass(cls, base_class):
                filtered.append(cls)
        return filtered


class BlockLibrary:
    BLOCK_PATH = './blocks'

    def __init__(self):
        block_path = pathlib.Path(BlockLibrary.BLOCK_PATH)

        logger.info(f'Checking {block_path.absolute()} for blocks')

        # goal: populate a dict
        # [
        #   { 'com.org.block_1' : BlockAdapter }
        # ]
        #
        # BlockAdapter
        #   validate_if_dir_is_a_block():
        #   load_from_dir():
        #
        #   should maintain a reference to the block class
        #
        #   get_instance():
        #       """should provide a new instance for when the simulation is run"""

        for path in self._get_subdirectories(block_path):
            if BlockAdapter.is_block_dir(path):
                logger.info(f'{path} is a block')

    @staticmethod
    def _get_subdirectories(path: pathlib.Path) -> List[pathlib.Path]:
        return [path for path in path.iterdir() if path.is_dir()]

