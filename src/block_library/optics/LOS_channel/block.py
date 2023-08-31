import numpy as np

from src.pyblock import TimeSignal
from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort


class LOSChannelBlock(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id='com.pyblocks.optics.LOS_channel',
            description='This block implements a Line-of-Sight VLC channel model.\n'
                        'The model is based on the work "Indoor Channel Characteristics for '
                        'Visible Light Communications" by Lee, Park et al. (2011)'
        )

        self.input_signal = InputPort(
            port_id='input_radiant_flux'
        )
        self.output_signal = OutputPort(
            port_id='output_radiant_flux'
        )

        self.led_position = Parameter(
            param_id='led_position',
            description='A point (in the format [x, y, z]) representing the cartesian '
                        'coordinates of the LED. Assumed to be in meters.'
        )
        self.led_orientation = Parameter(
            param_id='led_orientation',
            description='A vector (in the format [x, y, z] representing the orientation of the LED'
        )
        self.led_half_power_angle = Parameter(
            param_id='led_half_power_angle_deg', default=60,
            description='The angle (measured from the normal to the LED surface) where the optical '
                        'intensity falls to half the maximum value. Default = 60 deg'
        )
        self.pd_position = Parameter(
            param_id='pd_position',
            description='A point (in the format [x, y, z]) representing the cartesian '
                        'coordinates of the photodetector. Assumed to be in meters.'
        )
        self.pd_orientation = Parameter(
            param_id='pd_orientation',
            description='A vector (in the format [x, y, z] representing the orientation of the photodetector'
        )
        self.pd_area_mm = Parameter(
            param_id='pd_area_mm',
            description='Area of the photodetector. In square millimeters.'
        )
        self.pd_fov = Parameter(
            param_id='pd_field_of_view', default=60,
            description='Field-of-View of the photodetector, in degrees; Default = 60º'
        )

    def run(self):
        led_position = np.array(self.led_position.value)
        led_orientation = np.array(self.led_orientation.value)
        led_half_power_angle = self._deg_to_rad(self.led_half_power_angle.value)
        pd_position = np.array(self.pd_position.value)
        pd_orientation = np.array(self.pd_orientation.value)
        pd_area_mm = self._square_mm_to_square_m(self.pd_area_mm.value)
        pd_fov = self._deg_to_rad(self.pd_fov.value)

        input_signal: TimeSignal = self.input_signal.signal

        theta = self._angle_between_vectors(led_orientation, (pd_position - led_position))
        phi = self._angle_between_vectors(pd_orientation, (led_position - pd_position))
        distance = self._distance_between_points(led_position, pd_position)

        # if LED->Photodiode path is outside PD's Field-of-View, no signal received
        if phi > pd_fov:
            self.output_signal.signal = TimeSignal(
                time=input_signal.time, signal=np.zeros(len(input_signal))
            )
            return

        lambert_index = -np.log(2) / np.log(np.cos(led_half_power_angle))
        lambert_radiator_part = (np.cos(phi) ** lambert_index) * (lambert_index + 1)
        photodetector_part = pd_area_mm * np.cos(theta)
        l_0 = (lambert_radiator_part * photodetector_part) / (2 * np.pi * (distance ** 2))

        self.output_signal.signal = TimeSignal(
            time=input_signal.time,
            signal=(input_signal.signal * l_0)
        )

    def _angle_between_vectors(self, v1: np.array, v2: np.array):
        v1_normalized = v1 / np.linalg.norm(v1)
        v2_normalized = v2 / np.linalg.norm(v2)

        return np.arccos(np.clip(
            np.dot(v1_normalized, v2_normalized), -1, 1
        ))

    def _deg_to_rad(self, deg: float) -> float:
        return (deg/360.0) * 2.0 * np.pi

    def _distance_between_points(self, p1: np.array, p2: np.array) -> float:
        return np.sqrt(
            (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2
        )

    def _square_mm_to_square_m(self, area: float) -> float:
        return area * 10**-6
