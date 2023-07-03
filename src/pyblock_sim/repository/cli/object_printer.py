from abc import ABC
from typing import Any, Type


class ObjectPrinter(ABC):
    def get_type(self) -> Type:
        pass

    def print(self, obj: Any) -> str:
        """
            This function must return a string representing the object.
            Level tags will automatically be inserted before every line according
            to the level that was passed to the CLI print function
        """
        pass
