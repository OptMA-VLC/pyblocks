import pathlib
from typing import List

from src.meow_sim.block_library.block_adapter import BlockAdapter
from src.meow_sim.logger import logger


class BlockLibrary:
    BLOCK_PATH = './blocks'

    def __init__(self):
        block_path = pathlib.Path(BlockLibrary.BLOCK_PATH)

        logger.info(f'Checking {block_path.absolute()} for blocks')

        for path in self._get_subdirectories(block_path):
            if path.name.startswith('__'):
                logger.info(f'Skipping directory {path.name} for it starts with __')
                continue

            logger.info(f'Creating Adapter for potential block dir ${path.name}')
            adapter = BlockAdapter(path)
            # logger.info(f'{path} is a block')


        # goal: populate a List[BlockAdapter]
        #
        # BlockAdapter
        #   '''Objetivo: dar uma interface fácil para carregar e introspectar blocos; instanciar para a simulação'''
        #
        #   @classmethod is_block_dir(path):
        #   get_block_validation():
        #
        #   __init__(path):
        #   load_from_dir():
        #
        #   should maintain a reference to the block class
        #
        #   get_instance():
        #       """should provide a new instance for when the simulation is run"""


    @staticmethod
    def _get_subdirectories(path: pathlib.Path) -> List[pathlib.Path]:
        return [path for path in path.iterdir() if path.is_dir()]

