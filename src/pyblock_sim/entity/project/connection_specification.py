from dataclasses import dataclass

from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId


@dataclass
class ConnectionSpecification:
    origin_block: BlockInstanceId
    origin_port: PortId
    destination_block: BlockInstanceId
    destination_port: PortId
