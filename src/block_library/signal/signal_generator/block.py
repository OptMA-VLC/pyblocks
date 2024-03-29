import numpy as np
import scipy

from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.ports.output_port import OutputPort
from src.pyblock.signals.time_signal import TimeSignal


class SignalGeneratorBlock(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id='com.pyblocks.signal.signal_generator',
            name='Signal Generator',
            description='Generates a Square, Triangle or Sine Wave signal'
        )

        self.wave_form = Parameter(param_id='wave_form', type=str, default='square')
        self.freq = Parameter(param_id='frequency', type=float, default=1000.0)
        self.sample_freq = Parameter(param_id='sample_frequency', type=float, default=10000.0)
        self.duration = Parameter(param_id='duration', type=float, default=0.01)
        self.duty = Parameter(param_id='duty', type=float, default=0.5)
        self.amplitude = Parameter(param_id='amplitude', type=float, default=1.0)

        self.signal_out = OutputPort(port_id='signal_out', type=TimeSignal)

    def run(self):
        wave_form = self.wave_form.value.lower()
        f_sample = self.sample_freq.value
        f = self.freq.value
        duration = self.duration.value
        duty = self.duty.value
        amplitude = self.amplitude.value

        t = np.linspace(0, duration, int(f_sample)+1)

        if wave_form == 'square':
            signal = scipy.signal.square(2*np.pi * f * t, duty=duty)
            signal = 0.5 * (signal + 1)  # make wave have bounds [0, 1]
            signal = 1 - signal          # make wave start at low level
            signal = signal * amplitude  # adjust amplitude
        elif wave_form == 'triangle':
            signal = scipy.signal.sawtooth(2*np.pi * f * t, width=duty)
            signal = (signal + 1)/2
        elif wave_form == 'sine':
            signal = np.sin(2*np.pi * f * t)
            signal = signal * amplitude/2 + amplitude/2
        else:
            raise ValueError(f"The requested wave_form ('{wave_form}') is not supported.")


        self.signal_out.signal = TimeSignal(t, signal)
