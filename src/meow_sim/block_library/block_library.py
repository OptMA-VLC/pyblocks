import os
import pathlib
from typing import List

from src.meow_sim.logger import logger


class BlockLibrary:
    BLOCK_PATH = './blocks'

    # test cases:
    #  - no block dir
    #  - invalid dir
    #  - multiple block dirs
    #
    #  If found dirs inside block dirs:
    #     - validate that a directory is a block

    def __init__(self):
        block_path = pathlib.Path(BlockLibrary.BLOCK_PATH)

        logger.info(f'Checking {block_path.absolute()} for blocks')
        for path in self._get_subdirectories(block_path):
            logger.info(f'    /{path.name}  --- is block: {self._is_block_dir(path)}')

    @staticmethod
    def is_block_dir(path: pathlib.Path) -> bool:
        return (path / 'block.py').exists()

    @staticmethod
    def _get_subdirectories(path: pathlib.Path) -> List[pathlib.Path]:
        return [path for path in path.iterdir() if path.is_dir()]

