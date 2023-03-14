import numpy as np
from numpy import testing
from scipy import signal

from src.bdk.params.param_id import ParamId
from src.bdk.ports.port_id import PortId
from src.blocks.signal_generator.block import SignalGeneratorBlock
from src.meow_sim.block_runtime.block_runtime.block_runtime import BlockRuntime


class TestSignalGenerator:
    def test_square_wave(self):
        f_sample = 500
        f_wave = 5
        t = np.linspace(0, 1, f_sample+1)
        square_wave = signal.square(2*np.pi * f_wave * t)

        runtime = BlockRuntime(SignalGeneratorBlock)
        runtime.set_parameter(ParamId('frequency'), f_wave)
        runtime.set_parameter(ParamId('sample_frequency'), f_sample)
        runtime.set_parameter(ParamId('duration'), 1)

        runtime.run()
        out = runtime.get_output(PortId('signal_out'))

        testing.assert_allclose(t, out.time)
        testing.assert_allclose(square_wave, out.wave)
