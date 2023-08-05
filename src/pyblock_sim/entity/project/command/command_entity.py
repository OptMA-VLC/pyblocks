from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
from typing import Any, List

from src.pyblock_sim.entity.project.command.command_param_entity import CommandParamEntity


class CommandType(Enum):
    SIMULATE = 'simulate'
    SIMULATE_SWEEP = 'simulate_sweep'
    BLOCK_HELP = 'block_help'
    PLOT = 'plot'
    SAVE = 'save'


class CommandEntity(ABC):
    """
        Base class for command entities.
        list_params method MUST be implemented in derived classes
        An initializer MUST be implemented and call super().__init__(CommandType.MY_COMMAND)
    """
    type: CommandType
    params: List[CommandParamEntity]

    def __init__(self, cmd_type: CommandType):
        if cmd_type is None:
            raise RuntimeError(
                f'Class {type(self).__name__} could not be initialized because the required'
                f'parameter \'cmd_type\' has not been provided in super().__init__ call'
            )

        self.type = cmd_type
        self.params = self.list_params()

    @abstractmethod
    def list_params(self) -> List[CommandParamEntity]:
        pass

    def set_param(self, param_id: str, param_value: Any):
        for param in self.params:
            if param.id == param_id:
                param.value = param_value
                return

        raise KeyError(f"The command '{self.type}' does not have a parameter with id '{param_id}'")

    def get_param(self, param_id: str) -> Any:
        for param in self.params:
            if param.id == param_id:
                if param.value != CommandParamEntity.NO_VALUE:
                    return param.value

                if param.default != CommandParamEntity.NO_VALUE:
                    return param.default

                raise RuntimeError(
                    f"Attempt to access parameter '{param_id}' of command {self.type} "
                    "but no value has been provided for this parameter"
                )

        raise KeyError(f"No parameter with id '{param_id}' found in command {self.type}")

    def list_unfulfilled_params(self) -> List[CommandParamEntity]:
        unfulfilled = []

        for param in self.params:
            if param.is_unfulfilled():
                unfulfilled.append(param)

        return unfulfilled
