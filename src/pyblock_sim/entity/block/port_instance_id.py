from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId


class PortInstanceId:
    block_instance_id: BlockInstanceId
    port_id: PortId

    def __init__(self, block_instance_id: BlockInstanceId, port_id: PortId):
        self.block_instance_id = block_instance_id
        self.port_id = port_id

    def __str__(self):
        return f'{self.block_instance_id}::{self.port_id}'

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash((self.block_instance_id, self.port_id))
