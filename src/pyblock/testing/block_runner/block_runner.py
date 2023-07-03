import inspect
from typing import List, Any, Type, Dict

from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_distribution_id import BlockDistributionId
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.params.param_id import ParamId
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort
from src.pyblock.block.ports.port_id import PortId


class BlockRunner:
    distribution_id: BlockDistributionId
    _block_instance: BaseBlock

    _inputs: List[InputPort]
    _outputs: List[OutputPort]
    _params: List[Parameter]

    def __init__(self, block_class: Type[BaseBlock]):
        self._block_instance = block_class()

        self.distribution_id = self._block_instance.info.distribution_id
        self._inputs = self._find_inputs(self._block_instance)
        self._outputs = self._find_outputs(self._block_instance)
        self._params = self._find_params(self._block_instance)

    def set_parameter(self, param_id: str, value: Any):
        for block_param in self._params:
            if block_param.id == ParamId(param_id):
                block_param.value = value
                return

        raise KeyError(f"No parameter with Id '{param_id}' in block '{self.distribution_id}'")

    def set_input(self, port_id: str, value: Any):
        for block_input in self._inputs:
            if block_input.id == PortId(port_id):
                block_input.signal = value
                return

        raise KeyError(f"No input port with Id '{port_id}' in block '{self.distribution_id}'")

    def get_outputs(self) -> Dict:
        output_dict = {}
        for out_port in self._outputs:
            output_dict[out_port.id] = out_port.signal

        return output_dict

    def run(self):
        self._block_instance.run()

    def _find_inputs(self, block: BaseBlock) -> List[InputPort]:
        return self._find_attributes(block, matching_type=InputPort)

    def _find_outputs(self, block: BaseBlock) -> List[OutputPort]:
        return self._find_attributes(block, matching_type=OutputPort)

    def _find_params(self, block: BaseBlock) -> List[Parameter]:
        return self._find_attributes(block, matching_type=Parameter)

    def _find_attributes(self, obj: object, matching_type=object) -> List:
        def check_is_attr(x):
            return not inspect.isroutine(x)

        members = inspect.getmembers(obj, check_is_attr)

        result = []
        for (_, attr) in members:
            if isinstance(attr, matching_type):
                result.append(attr)

        return result
