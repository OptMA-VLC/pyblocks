import numpy as np
from scipy import signal

from src import pyblock
from src.pyblock.block.params.param_id import ParamId
from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.block_runtime.block_runtime import BlockRuntime
from src.block_library.signal.signal_generator.block import SignalGeneratorBlock


class TestSignalGenerator:
    def test_square_wave(self):
        f_sample = 500.0
        f_wave = 10.0
        t = np.linspace(0, 0.2, int(f_sample+1.0))
        square_wave = signal.square(2*np.pi * f_wave * t)

        runtime = BlockRuntime(SignalGeneratorBlock)
        runtime.set_parameter(ParamId('wave_form'), 'square')
        runtime.set_parameter(ParamId('duty'), 0.5)
        runtime.set_parameter(ParamId('frequency'), f_wave)
        runtime.set_parameter(ParamId('sample_frequency'), f_sample)
        runtime.set_parameter(ParamId('duration'), 0.2)

        runtime.run()
        out = runtime.get_output(PortId('signal_out'))

        pyblock.testing.plot(out)
        np.testing.assert_allclose(t, out.time)
        np.testing.assert_allclose(square_wave, out.wave)
