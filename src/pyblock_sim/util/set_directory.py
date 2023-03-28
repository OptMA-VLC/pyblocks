from contextlib import contextmanager
from pathlib import Path

import os
from typing import Union


@contextmanager
def set_directory(path: Union[str, Path]):
    """Sets the cwd within the context and restores previous cwd on exit"""

    origin = Path().absolute()
    try:
        if isinstance(path, str):
            path = Path(path)
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)

