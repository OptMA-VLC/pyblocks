from src.pyblock import TimeSignal
from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort


class LED_Block(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id='com.pyblocks.optics.LED',
            description='Represents an LED as a constant conversion factor between current and radiant flux.'
        )

        self.input_current = InputPort(
            port_id='input_current', type=TimeSignal,
            description='A time signal representing electrical current (in Ampere)'
        )
        self.output_radiant_flux = OutputPort(
            port_id='output_radiant_flux', type=TimeSignal,
            description='A time signal representing radiant flux (in Watts)'
        )

        # TODO: descobrir se esse parâmetro tem nome
        self.conversion_constant = Parameter(
            param_id='conversion_constant', type=float,
            description='Conversion factor between current and radiant flux. Given in Watt/Ampere.'
        )

    def run(self):
        input_signal = self.input_current.signal
        conversion_constant = self.conversion_constant.value
        self.output_radiant_flux.signal = TimeSignal(
            time=input_signal.time,
            signal=(conversion_constant * input_signal.signal)
        )

