from src.bdk.base_block import BaseBlock
from src.bdk.block_info import BlockInfo
from src.bdk.ports.PortBundle import PortBundle
from src.bdk.ports.port import Port
from src.blocks.string_print.implementation import StringPrintImpl
from src.meow_sim.entity.param_bundle import ParamBundle


class StringPrint(BaseBlock):
    def __init__(self):
        self.block_info = BlockInfo(
            distribution_id='br.ufmg.optma.to_upper',
            name='Makes a string upper case',
            description=''
        )
        self.params = ParamBundle()
        self.inputs = PortBundle(
            Port('str_in', str)
        )
        self.outputs = PortBundle()

        super().__init__()

    def run(self):
        string_to_print = self.inputs.get_signal('str_in')
        StringPrintImpl.print(string_to_print)
