from typing import Any

import sentinel


class CommandParamEntity:
    NO_VALUE = sentinel.create('NO_VALUE')

    id: str
    default: Any
    value: Any

    def __init__(self, param_id: str, default: Any = NO_VALUE):
        self.id = param_id
        self.default = default
        self.value = CommandParamEntity.NO_VALUE

    def is_unfulfilled(self) -> bool:
        return (
            self.default == CommandParamEntity.NO_VALUE
            and self.value == CommandParamEntity.NO_VALUE
        )
