from src.pyblock import TimeSignal
from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.param import Param
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort


class GainBlock(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id='br.ufmg.optma.basic.gain',
            name='Gain',
            description='Applies a gain to a signal'
        )

        self.gain_db = Param(param_id='gain_db', type=float, default=0.0)
        self.signal_in = InputPort(port_id='signal_in', type=TimeSignal)
        self.signal_out = OutputPort(port_id='signal_out', type=TimeSignal)

    def run(self):
        gain = pow(10.0, self.gain_db.value/20.0)
        signal_in = self.signal_in.signal
        signal_out = TimeSignal(
            time=signal_in.time,
            signal=signal_in.wave * gain
        )

        self.signal_out.signal = signal_out
