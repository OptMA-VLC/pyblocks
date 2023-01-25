import pathlib

from src.bdk.base_block import BaseBlock


class BlockRepositoryException(Exception):
    pass


class BlockDoesNotExist(BlockRepositoryException):
    def __init__(self, name: str):
        super().__init__(f'No block with distribution name {name} is known to the BlockRepository')


class NotADir(BlockRepositoryException):
    def __init__(self, path: pathlib.Path):
        super().__init__(f'The provided path {path.resolve()} is not a directory')


class NoBlockPyFile(BlockRepositoryException):
    def __init__(self, path: pathlib.Path):
        super().__init__(f'The provided path {path.resolve()} does not contain a block.py file')


class LoadModuleFailed(BlockRepositoryException):
    def __init__(self, path: pathlib.Path):
        super().__init__(f'Error loading module block.py for block directory {path.resolve()}')


class NoBlockClassFound(BlockRepositoryException):
    def __init__(self):
        super().__init__(f'No class inheriting from {BaseBlock.__name__} found in block.py file')


class MultipleBlockClassesInFile(BlockRepositoryException):
    def __init__(self):
        super().__init__(f'More than one class inheriting from {BaseBlock.__name__} found in '
                         f'block.py file')


class LoadBlockClassFailed(BlockRepositoryException):
    pass
