from src.pyblock import TimeSignal
from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort


class SubBlock(BaseBlock):
    def __init__(self):
        self.info = BlockInfo(
            distribution_id='com.pyblocks.basic.sub', name='Subtraction',
            description='Receives two TimeSignal inputs (signal_a, signal_b) and produces a - b on signal_out. '
                        'Signal B will be resampled to match signal A'
        )

        self.signal_a = InputPort(
            port_id='signal_a', type=TimeSignal,
            description='Signal A'
        )
        self.signal_b = InputPort(
            port_id='signal_b', type=TimeSignal,
            description='Signal B'
        )
        self.signal_out = OutputPort(
            port_id='signal_out', type=TimeSignal,
            description='A - B'
        )

    def run(self):
        signal_a = self.signal_a.signal
        signal_b = self.signal_b.signal

        if not isinstance(signal_a, TimeSignal):
            raise TypeError(f'signal_a must be a TimeSignal (is {type(signal_a).__name__})')

        if not isinstance(signal_b, TimeSignal):
            raise TypeError(f'signal_b must be a TimeSignal (is {type(signal_b).__name__})')

        signal_b_resampled = signal_b.resample_to(signal_a)

        self.signal_out.signal = signal_a - signal_b_resampled
