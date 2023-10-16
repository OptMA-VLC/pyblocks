from src.pyblock import TimeSignal
from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort


class LED_Block(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id='com.pyblocks.optics.LED_vi',
            description='LED model that takes the voltage and current as inputs.'
                        'The voltage and current multiplied give the input electrical'
                        'power, which is converted into optical power (a radiant flux)'
                        'by an efficiency factor.'
        )

        self.input_current = InputPort(
            port_id='input_current', type=TimeSignal,
            description='A time signal representing electrical current (in Ampere)'
        )
        self.input_voltage = InputPort(
            port_id='input_voltage', type=TimeSignal,
            description='A time signal representing voltage (in Volts)'
        )
        self.output_radiant_flux = OutputPort(
            port_id='output_radiant_flux', type=TimeSignal,
            description='A time signal representing radiant flux (in Watts)'
        )

        self.led_efficiency = Parameter(
            param_id='led_efficiency', type=float,
            description='Conversion factor between current and radiant flux. Given in Watt/Ampere.'
        )

    def run(self):
        input_current: TimeSignal = self.input_current.signal
        input_voltage: TimeSignal = self.input_voltage.signal
        led_efficiency = self.led_efficiency.value

        # validate inputs
        if not isinstance(input_voltage, TimeSignal):
            raise TypeError(f'input_voltage must be a TimeSignal (is {type(input_voltage).__name__})')
        if not isinstance(input_current, TimeSignal):
            raise TypeError(f'input_current must be a TimeSignal (is {type(input_current).__name__})')
        if not isinstance(led_efficiency, float) and not isinstance(led_efficiency, int):
            raise TypeError(f'led_efficiency must be a Number (is {type(led_efficiency).__name__})')

        voltage_resampled = TimeSignal(
            time=input_current.time,
            signal=input_voltage.resample_to(input_current)
        )

        input_power = input_current * voltage_resampled
        output_power = input_power * led_efficiency

        self.output_radiant_flux.signal = output_power
