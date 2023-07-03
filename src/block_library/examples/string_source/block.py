from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.ports.output_port import OutputPort


class StringSourceBlock(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id='com.pyblocks.example.string_source'
        )
        self.value_param = Parameter(param_id='value', type=str)
        self.output = OutputPort(port_id='output', type=str)

    def run(self):
        self.output.signal = self.value_param.value
