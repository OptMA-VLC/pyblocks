from typing import Any, Type, Union

import sentinel

from src.pyblock.block.params.param_id import ParamId


class Parameter:
    NO_VALUE = sentinel.create('NO_VALUE')

    id: ParamId
    type: Type
    default: Any
    description: str
    _value: Any

    @property
    def value(self):
        if self._value is Parameter.NO_VALUE:
            if self.default is Parameter.NO_VALUE:
                raise ValueError(f"Illegal attempt to access the value of Parameter '{self.id}'. value has not been "
                                 f"assigned and there is no default value for this parameter.")
            else:
                return self.default
        return self._value

    @value.setter
    def value(self, value: Any):
        self._value = value

    def __init__(
            self,
            param_id: Union[ParamId, str],
            type: Type = Any,
            default: Any = NO_VALUE,
            description: str = ''
    ):
        if isinstance(param_id, str):
            param_id = ParamId(param_id)

        self.id = param_id
        self.type = type
        self.default = default
        self._value = Parameter.NO_VALUE
        self.description = description
