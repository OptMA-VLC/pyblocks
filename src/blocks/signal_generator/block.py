import numpy as np
import scipy

from src.bdk.base_block import BaseBlock
from src.bdk.block_info import BlockInfo
from src.bdk.params.parameter import Parameter
from src.bdk.ports.PortBundle import PortBundle
from src.bdk.ports.port import Port
from src.bdk.signals.signal_wave import SignalWave
from src.meow_sim.entity.param_bundle import ParamBundle


class SignalGeneratorBlock(BaseBlock):
    def __init__(self):
        self.block_info = BlockInfo(
            distribution_id='br.ufmg.optma.signal_generator',
            name='Signal Generator',
            description='Generates a Square, Triangle or Sine Wave signal'
        )
        self.params = ParamBundle(
            Parameter(id='frequency', type=float),
            Parameter(id='sample_frequency', type=float),
            Parameter(id='duration', type=float),
            Parameter(id='duty', type=float, default=0.5),
        )
        self.inputs = PortBundle()
        self.outputs = PortBundle(
            Port(port_id='signal_out', signal_type=SignalWave)
        )
        super().__init__()

    def run(self):
        f_sample = self.params.get_param('sample_frequency')
        f = self.params.get_param('frequency')
        duration = self.params.get_param('duration')
        duty = self.params.get_param('duty')

        t = np.linspace(0, duration, f_sample+1)
        square_wave = scipy.signal.square(2*np.pi * f * t, duty=duty)

        self.outputs.set_signal('signal_out', SignalWave(t, square_wave))
