import importlib
import inspect
import pathlib
from types import ModuleType
from typing import Any, List


def load_module(name: str, path: pathlib.Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def get_classes(module: ModuleType) -> List[Any]:
    module_classes = []
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            is_declared_in_this_module = (obj.__module__ == module.__name__)
            if is_declared_in_this_module:
                module_classes.append(obj)

    return module_classes


def filter_subclasses_of(classes: List[Any], base_class: Any):
    filtered = []
    for cls in classes:
        if issubclass(cls, base_class):
            filtered.append(cls)

    return filtered

