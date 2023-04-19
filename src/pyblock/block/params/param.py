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
        try:
            if not isinstance(value, self.type):
                raise ValueError(f"Can't assign value of type '{type(value).__name__}' to param '{self.id}' which has "
                                 f"type '{self.type.__name__}'")
            self._value = value
        except TypeError as err:
            if 'Subscripted generics' in str(err):
                print('Warning: type checking for generic types is not currently supported')
                self._value = value
            else:
                raise
    def __init__(self, param_id: Union[ParamId, str], type: Type, default: Any = NO_VALUE):
        if isinstance(param_id, str):
            param_id = ParamId(param_id)

        if (default is not Param.NO_VALUE) and (not isinstance(default, type)):
            raise ValueError(f"The Param '{param_id}' is of type '{type.__name__}' but the provided "
                             f"default value is of type '{type(default).__name__}'")

        self.id = param_id
        self.type = type
        self.default = default
        self._value = Param.NO_VALUE
