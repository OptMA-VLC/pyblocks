import numpy as np
import scipy

from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.param import Param
from src.pyblock.block.ports.output import Output
from src.pyblock.signals.signal_wave import SignalWave


class SignalGeneratorBlock(BaseBlock):
    def __init__(self):
        self.freq = Param(param_id='frequency', param_type=float, default=1000.0)
        self.sample_freq = Param(param_id='sample_frequency', param_type=float, default=10000.0)
        self.duration = Param(param_id='duration', param_type=float, default=0.01)
        self.duty = Param(param_id='duty', param_type=float, default=0.5)

        self.signal_out = Output(port_id='signal_out', type=SignalWave)

        super().__init__(BlockInfo(
            distribution_id='br.ufmg.optma.signal_generator',
            name='Signal Generator',
            description='Generates a Square, Triangle or Sine Wave signal'
        ))

    def run(self):
        f_sample = self.sample_freq.value
        f = self.freq.value
        duration = self.duration.value
        duty = self.duty.value

        t = np.linspace(0, duration, int(f_sample)+1)
        square_wave = scipy.signal.square(2*np.pi * f * t, duty=duty)

        self.signal_out.signal = SignalWave(t, square_wave)
