from scipy.signal import butter, lfilter

from src.pyblock import TimeSignal
from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort


class LowPassFilterBlock(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id="com.pyblocks.signal.low_pass",
            name="Low Pass Filter",
            description="Low pass Butterworth filter. Order and cutoff frequency can be set by the parameters"
        )

        self.input = InputPort(port_id='input')
        self.output = OutputPort(port_id='output')
        self.order = Parameter(param_id='order', default=1)
        self.f_cutoff = Parameter(param_id='f_cutoff', default=1000)

    def run(self):
        # prepare parameters
        input_signal: TimeSignal = self.input.signal
        order = self.order.value
        f_cutoff = float(self.f_cutoff.value)

        f_sample = input_signal.sample_frequency

        # apply filter
        (b, a) = butter(order, f_cutoff, fs=f_sample, btype='low', analog=False)
        out_signal = lfilter(b, a, input_signal.signal)

        # set output
        self.output.signal = TimeSignal(
            time=input_signal.time,
            signal=out_signal
        )
