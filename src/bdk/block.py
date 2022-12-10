from .params.param_bundle import ParamBundle
from .port import Port
from .signals.signal import Signal


class Block:
    def validate_inputs(self, inputs: [(Port, Signal)]):
        pass

    def run(self, inputs: [(Port, Signal)], params: ParamBundle) -> [(Port, Signal)]:
        pass
