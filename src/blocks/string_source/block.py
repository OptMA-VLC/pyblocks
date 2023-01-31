from src.bdk.base_block import BaseBlock
from src.bdk.block_info import BlockInfo
from src.bdk.params.parameter import Parameter
from src.bdk.ports.PortBundle import PortBundle
from src.bdk.ports.port import Port
from src.meow_sim.entity.param_bundle import ParamBundle


class StringSource(BaseBlock):
    def __init__(self):
        self.block_info = BlockInfo(
            distribution_id='br.ufmg.optma.string_source',
            name='String Data Source',
            description='',
        )
        self.params = ParamBundle(
            Parameter('string', str)
        )
        self.inputs = PortBundle()
        self.outputs = PortBundle(
            Port('str_out', str)
        )

        super().__init__()

    def run(self):
        string_to_output = self.params.get_param('string')
        self.outputs.set_signal('str_out', string_to_output)
