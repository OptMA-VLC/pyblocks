from dataclasses import dataclass

from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId


@dataclass
class PortSelector:
    block: BlockInstanceId
    port: PortId

    @staticmethod
    def parse(port_str: str) -> 'PortSelector':
        parts = port_str.split('::')
        if len(parts) != 2:
            raise ValueError(
                f"Error parsing the port name '{port_str}', ports must "
                f"be specified in the format 'block_instance_id::port_id'"
            )

        return PortSelector(block=BlockInstanceId(parts[0]), port=PortId(parts[1]))

    def __str__(self):
        return f'{self.block}::{self.port}'
