from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_distribution_id import BlockDistributionId
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.param_id import ParamId
from src.pyblock.block.params.param import Param
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort
from src.pyblock_sim.block_runtime.block_runtime.block_runtime import BlockRuntime


class TestBlockRuntime:
    def test_applies_parameters(self):
        runtime = BlockRuntime(TestBlock)
        block: TestBlock = runtime._block_instance

        runtime.set_parameter(ParamId('param_1'), 'Hello')

        assert block.param_1.value == 'Hello'

    def test_applies_input(self):
        runtime = BlockRuntime(TestBlock)
        block: TestBlock = runtime._block_instance

        runtime.set_input('in_1', 'Hello')

        assert block.in_1.signal == 'Hello'

    def test_run(self):
        runtime = BlockRuntime(TestBlock)
        block: TestBlock = runtime._block_instance

        runtime.set_parameter('param_1', 'World!')
        runtime.set_input('in_1', 'Hello ')
        runtime.run()
        out = runtime.get_output('out_1')

        assert out == 'Hello World!'


class TestBlock(BaseBlock):
    def __init__(self):
        self.param_1 = Param(param_id=ParamId('param_1'), param_type=str)
        self.in_1 = InputPort(port_id='in_1', type=str)
        self.out_1 = OutputPort(port_id='out_1', type=str)
        super().__init__(BlockInfo(
            distribution_id=BlockDistributionId('test_block'), name='', description=''
        ))

    def run(self):
        self.out_1.signal = self.in_1.signal + self.param_1.value
