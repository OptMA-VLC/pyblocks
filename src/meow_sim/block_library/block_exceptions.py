import pathlib


class BlockExceptions:
    class NotADir(Exception):
        def __init__(self, path: pathlib.Path):
            super().__init__(f'The provided path {path.resolve()} is not a directory')

    class NoBlockPyFile(Exception):
        def __init__(self, path: pathlib.Path):
            super().__init__(f'The provided path {path.resolve()} does not contain a block.py file')

    class LoadModuleFailed(Exception):
        def __init__(self, path: pathlib.Path):
            super().__init__(f'Error loading module block.py for block directory {path.resolve()}')

    class LoadBlockClassFailed(Exception):
        pass
