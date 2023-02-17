import numpy as np
from numpy import testing
from scipy import signal
import matplotlib.pyplot as plt

from src.blocks.signal_generator.block import SignalGeneratorBlock
from src.meow_sim.repository.block_adapter.block_adapter import BlockAdapter


class TestSignalGenerator:
    def test_square_wave(self):
        f_sample = 500
        f_wave = 5
        t = np.linspace(0, 1, f_sample+1)
        square_wave = signal.square(2*np.pi * f_wave * t)

        adapter = BlockAdapter(SignalGeneratorBlock)
        adapter.apply_parameters([
            ('frequency', f_wave),
            ('sample_frequency', f_sample),
            ('duration', 1),
        ])
        adapter.run()
        out = adapter.get_signal('signal_out')

        testing.assert_allclose(t, out.time)
        testing.assert_allclose(square_wave, out.wave)
