from typing import Any

import sentinel


class CommandParamEntity:
    NO_VALUE = sentinel.create('NO_VALUE')

    id: str
    default: Any
    description: str
    value: Any

    def __init__(self, param_id: str, description: str = '', default: Any = NO_VALUE):
        self.id = param_id
        self.description = description
        self.default = default
        self.value = CommandParamEntity.NO_VALUE

    def is_unfulfilled(self) -> bool:
        return (
            self.default == CommandParamEntity.NO_VALUE
            and self.value == CommandParamEntity.NO_VALUE
        )
