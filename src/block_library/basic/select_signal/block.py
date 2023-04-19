from typing import Any

from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.param import Param
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort
from src.pyblock.signals.multi_signal import MultiSignal
from src.pyblock.signals.signal_name import SignalName


class SelectSignalBlock(BaseBlock):
    def __init__(self):
        self.signal_in = InputPort(port_id='signal_in', type=MultiSignal)
        self.signal_out = OutputPort(port_id='signal_out', type=Any)

        self.signal_name = Param(param_id='signal_name', type=str)

        super().__init__(BlockInfo(
            distribution_id='br.ufmg.optma.basic.select_signal',
            name='Signal Selector Block',
            description='Selects a single signal (selected by setting the parameter '
                        'signal_name) from an input of type MultiSignal.'
        ))

    def run(self):
        signal_in: MultiSignal = self.signal_in.signal
        signal_name = self.signal_name.value
        self.signal_out.signal = signal_in.get(SignalName(signal_name))
