from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.ports.output_port import OutputPort


class ConstantBlock(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id='com.pyblocks.basic.constant',
            name='Constant',
            description="This blocks produces a constant (set by the parameter 'constant') at its output"
        )

        self.constant = Parameter(param_id='constant', default=1)
        self.output = OutputPort(port_id='output')

    def run(self):
        value = self.constant.value
        self.output.signal = value
