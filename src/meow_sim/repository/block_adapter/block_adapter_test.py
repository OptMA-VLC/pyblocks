from src.bdk.base_block import BaseBlock
from src.bdk.block_info import BlockInfo
from src.bdk.params.parameter import Parameter
from src.bdk.ports.input import Input
from src.bdk.ports.output import Output
from src.meow_sim.repository.block_adapter.block_adapter import BlockAdapter


class TestBlock(BaseBlock):
    def __init__(self):
        self.param_1 = Parameter(id='param_1', type=str)
        self.in_1 = Input(port_id='in_1', type=str)
        self.out_1 = Output(port_id='out_1', type=str)
        super().__init__(BlockInfo(
            distribution_id='test_block', name='', description=''
        ))

    def run(self):
        self.out_1.signal = self.in_1.signal + self.param_1.value

class TestBlockAdapter:
    def test_applies_parameters(self):
        adapter = BlockAdapter(TestBlock)
        block: TestBlock = adapter._block_instance

        adapter.apply_parameters([
            ('param_1', 'Hello')
        ])

        assert block.param_1.value == 'Hello'

    def test_applies_input(self):
        adapter = BlockAdapter(TestBlock)
        block: TestBlock = adapter._block_instance

        adapter.set_input('in_1', 'Hello')

        assert block.in_1.signal == 'Hello'

    def test_run(self):
        adapter = BlockAdapter(TestBlock)
        block: TestBlock = adapter._block_instance

        adapter.apply_parameters([
            ('param_1', 'World!')
        ])
        adapter.set_input('in_1', 'Hello ')
        adapter.run()
        out = adapter.get_output('out_1')

        assert out == 'Hello World!'
