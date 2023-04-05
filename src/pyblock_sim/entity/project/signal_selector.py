from dataclasses import dataclass
from typing import Optional

from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId


@dataclass
class SignalSelector:
    block: BlockInstanceId
    port: PortId
    signal_name: Optional[str]

    def __str__(self):
        s = f'{self.block}::{self.port}'
        if self.signal_name is not None:
            s += f'[{self.signal_name}]'
        return s

    @staticmethod
    def parse(signal_selector_str: str) -> 'SignalSelector':
        format_error = ValueError(
                f"Signal selector string must be in the format "
                f"block_instance_id::port_id[signal_name]' (received '{signal_selector_str}')"
            )

        try:
            double_colon_split = signal_selector_str.split('::')
            if len(double_colon_split) != 2:
                raise format_error
            block_part = double_colon_split[0]

            open_brackets_split = double_colon_split[1].split('[')
            port_part = open_brackets_split[0]
            if len(open_brackets_split) == 1:
                signal_part = None
            elif len(open_brackets_split) == 2:
                close_brackets_split = open_brackets_split[1].split(']')
                if len(close_brackets_split[1]) != 0:
                    raise format_error
                signal_part = close_brackets_split[0]
            else:
                raise format_error

        except IndexError as ex:
            raise format_error from ex

        return SignalSelector(
            block=BlockInstanceId(block_part),
            port=PortId(port_part),
            signal_name=signal_part
        )


