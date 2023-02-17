from typing import Dict, Any

from src.bdk.params.parameter import ParamId, Parameter


class ParamBundle:
    params: Dict[ParamId, Parameter]

    def __init__(self, *args):
        self.params = {}

        for arg in args:
            if isinstance(arg, Parameter):
                self.params[arg.id] = arg
            else:
                assert TypeError('ParamBundle constructor takes Parameter objects as arguments')


    def get_param(self, param_id: ParamId) -> Any:
        param = self.params[param_id]
        if param.value is None:
            return param.default

        return param.value

    def set_param(self, param_id: ParamId, value: Any):
        param = self.params[param_id]
        param.value = value
