import numpy as np

from src.block_library.optics.LOS_channel.block import LOSChannelBlock
from src.block_library.optics.LOS_channel_noise.block import LOSChannelNoiseBlock
from src.pyblock import TimeSignal
from src.pyblock.testing.block_runner.block_runner import BlockTester


class TestLOSChannel:
    def test(self):
        input_signal = TimeSignal(
            time=[0, 1, 2, 3, 4, 5],
            signal=[0, 0, 1, 1, 0, 0]
        )

        output_signal = self._run_scenario(input_signal, ambient_light=0.5)

        np.testing.assert_equal(output_signal.signal, [0.5, 0.5, 1.5, 1.5, 0.5, 0.5])

    def _run_scenario(self, input_signal: TimeSignal, ambient_light=0, white_noise=0) -> TimeSignal:
        # prepare
        tester = BlockTester(LOSChannelNoiseBlock) \
            .set_parameter('ambient_light_w', ambient_light) \
            .set_parameter('white_noise_w', white_noise) \
            .set_input('input_radiant_flux', input_signal)

        # run
        tester.run()
        output_signal: TimeSignal = tester.get_output('output_radiant_flux')

        return output_signal