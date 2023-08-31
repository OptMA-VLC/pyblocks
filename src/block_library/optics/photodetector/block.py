from src.pyblock import TimeSignal
from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort


class Photodetector_Block(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id='com.pyblocks.optics.photodetector',
            description='Represents a photodetector as a simple conversion '
                        'factor between optical power and current.'
        )

        self.input_current = InputPort(
            port_id='input_radiant_flux', type=TimeSignal,
            description='A time signal representing radiant flux (in Watts)'
        )
        self.output_radiant_flux = OutputPort(
            port_id='output_current', type=TimeSignal,
            description='A time signal representing electrical current (in Ampere)'
        )

        self.sensitivity = Parameter(
            param_id='sensitivity', type=float,
            description='Photodetector sensitivity. Given in Ampere/Watt'
        )

    def run(self):
        input_signal = self.input_current.signal
        sensitivity = self.sensitivity.value
        self.output_radiant_flux.signal = TimeSignal(
            time=input_signal.time,
            signal=(sensitivity * input_signal.signal)
        )
