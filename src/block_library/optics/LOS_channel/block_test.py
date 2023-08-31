import numpy as np

from src.block_library.optics.LOS_channel.block import LOSChannelBlock
from src.pyblock import TimeSignal
from src.pyblock.testing.block_runner.block_runner import BlockTester


class TestLOSChannel:
    def test_line_of_sight(self):
        # LED and PD aligned, separated by 2 meters
        self._test_scenario(
            l_0_analytical=0.318 * (10 ** -6),
            led_position=[0, 0, 0],
            led_orientation=[0, 0, 1],
            pd_position=[0, 0, 2],
            pd_orientation=[0, 0, -1],
            pd_area_mm=4,
        )

    def test_missaligned(self):
        # LED and PD separated by 2m but both pointing up
        # light hits PD directly at it's back
        self._test_scenario(
            l_0_analytical=0,
            led_position=[0, 0, 0],
            led_orientation=[0, 0, 1],
            led_half_power_angle=80,
            pd_position=[0, 0, 2],
            pd_orientation=[0, 0, 1],
            pd_area_mm=4,
        )

    def test_triangle(self):
        # Scenario where the path between LED and PD is the
        # hypotenuse of a triangle with 30 deg and 60 deg angles
        self._test_scenario(
            l_0_analytical=0.179267 * (10**-6),
            led_position=[0, 0, 1],
            led_orientation=[0, 0, -1],
            pd_position=[0.408, 0.408, 0],
            pd_orientation=[0, 0, 1],
            pd_area_mm=1,
        )

    def test_triangle_m(self):
        # Same as previous scenario but LED half-power angle is 80 deg
        # corresponds to lambert index (m) = 0.3959
        self._test_scenario(
            l_0_analytical=0.13647 * (10**-6),
            led_position=[0, 0, 1],
            led_orientation=[0, 0, -1],
            led_half_power_angle=80,
            pd_position=[0.408, 0.408, 0],
            pd_orientation=[0, 0, 1],
            pd_area_mm=1,
        )


    def _test_scenario(
            self, l_0_analytical,
            led_position, led_orientation,
            pd_position, pd_orientation, pd_area_mm,
            led_half_power_angle=60,
            pd_fov=60
    ):
        input_signal = TimeSignal(
            time=[0, 1, 2, 3, 4, 5],
            signal=[0, 1, 2, 0, 0, 1]
        )
        analytical_solution = l_0_analytical * input_signal.signal

        # prepare
        tester = BlockTester(LOSChannelBlock) \
            .set_parameter('led_position', led_position) \
            .set_parameter('led_orientation', led_orientation) \
            .set_parameter('led_half_power_angle_deg', led_half_power_angle) \
            .set_parameter('pd_position', pd_position) \
            .set_parameter('pd_orientation', pd_orientation) \
            .set_parameter('pd_area_mm', pd_area_mm) \
            .set_parameter('pd_field_of_view', pd_fov) \
            .set_input('input_radiant_flux', input_signal)

        # run
        tester.run()
        output_signal: TimeSignal = tester.get_output('output_radiant_flux')

        self._assert_result(output_signal.signal, analytical_solution)

    def _assert_result(
            self, actual: np.array, expected: np.array, rtol: float = 0.001
    ):
        np.testing.assert_allclose(actual, expected, rtol=rtol)
