from typing import Any, Type, Union

import sentinel

from src.bdk.params.param_id import ParamId


class Parameter:
    NO_VALUE = sentinel.create('NO_VALUE')

    id: ParamId
    type: Type
    default: Any
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
        if not isinstance(value, self.type):
            raise ValueError(f"Can't assign value of type '{type(value).__name__}' to param '{self.id}' which has "
                             f"type '{type(self.type).__name__}'")
        self._value = value

    def __init__(self, param_id: Union[ParamId, str], param_type: Type, default: Any = NO_VALUE):
        if isinstance(param_id, str):
            param_id = ParamId(param_id)

        if (default is not Parameter.NO_VALUE) and (not isinstance(default, param_type)):
            raise ValueError(f"The Parameter '{param_id}' is of type '{param_type.__name__}' but the provided "
                             f"default value is of type '{type(default).__name__}'")

        self.id = param_id
        self.type = param_type
        self.default = default
        self._value = Parameter.NO_VALUE
