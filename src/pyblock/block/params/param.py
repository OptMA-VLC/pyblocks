from typing import Any, Type, Union

import sentinel

from src.pyblock.block.params.param_id import ParamId


class Param:
    NO_VALUE = sentinel.create('NO_VALUE')

    id: ParamId
    type: Type
    default: Any
    _value: Any

    @property
    def value(self):
        if self._value is Param.NO_VALUE:
            if self.default is Param.NO_VALUE:
                raise ValueError(f"Illegal attempt to access the value of Param '{self.id}'. value has not been "
                                 f"assigned and there is no default value for this parameter.")
            else:
                return self.default
        return self._value

    @value.setter
    def value(self, value: Any):
        self._value = value

    def __init__(self, param_id: Union[ParamId, str], type: Type, default: Any = NO_VALUE):
        if isinstance(param_id, str):
            param_id = ParamId(param_id)

        self.id = param_id
        self.type = type
        self.default = default
        self._value = Param.NO_VALUE
