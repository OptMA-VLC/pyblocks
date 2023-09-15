import numpy as np

from src.pyblock import TimeSignal
from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort


class LOSChannelNoiseBlock(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id='com.pyblocks.optics.LOS_channel_noise',
            description='This block can inject a constant background light or white noise in a radiant flux signal.'
        )

        self.input_signal = InputPort(
            port_id='input_radiant_flux'
        )
        self.output_signal = OutputPort(
            port_id='output_radiant_flux'
        )

        self.ambient_light_w = Parameter(
            param_id='ambient_light_w',
            default=0,
            description='Value in Watts of a constant level of ambient light'
        )
        self.white_noise_w = Parameter(
            param_id='white_noise_w',
            default=0,
            description='Addictive white gaussian noise in Watts'
        )

    def run(self):
        ambient_light = self.ambient_light_w.value
        white_noise = self.white_noise_w.value

        if white_noise != 0:
            raise NotImplementedError('White noise not implemented yet. Leave parameter at 0 pls.')

        input_signal: TimeSignal = self.input_signal.signal

        output_signal = input_signal.signal + ambient_light

        self.output_signal.signal = TimeSignal(
            time=input_signal.time,
            signal=output_signal
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
