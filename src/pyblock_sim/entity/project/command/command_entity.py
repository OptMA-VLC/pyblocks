from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict


class CommandType(Enum):
    PLOT = 'plot'
    SAVE = 'save'


@dataclass
class CommandEntity(ABC):
    type: CommandType

    @staticmethod
    @abstractmethod
    def parse_args(args_json_dict: Dict) -> 'CommandEntity':
        pass
