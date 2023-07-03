from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort


class StringTransformBlock(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id='com.pyblocks.example.string_transform'
        )
        self.input = InputPort(port_id='input', type=str)
        self.output = OutputPort(port_id='output', type=str)
        self.transform_type = Parameter(param_id='transform', default='to_lower', type=str)

    def run(self):
        in_str: str = self.input.signal
        transform = self.transform_type.value

        if transform == 'to_lower':
            self.output.signal = in_str.lower()
        elif transform == 'to_upper':
            self.output.signal = in_str.upper()
        else:
            raise ValueError(f'Unsupported string transform: {transform}')
