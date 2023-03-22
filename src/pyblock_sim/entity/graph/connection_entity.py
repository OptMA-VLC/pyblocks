import uuid
from dataclasses import field, dataclass

from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.entity.block.port_entity import PortEntity
from src.pyblock_sim.entity.graph.connection_instance_id import ConnectionInstanceId


def _generate_connection_id() -> ConnectionInstanceId:
    return ConnectionInstanceId(uuid.uuid4())


@dataclass
class ConnectionEntity:
    origin_block: BlockInstanceId
    origin_port: PortId
    destination_block: BlockInstanceId
    destination_port: PortId
    id: ConnectionInstanceId = field(default_factory=_generate_connection_id)

    @classmethod
    def from_port_entity(cls, from_port: PortEntity, to_port: PortEntity) -> 'ConnectionEntity':
        return ConnectionEntity(
            origin_block=from_port.block.instance_id,
            origin_port=from_port.port_id,
            destination_block=to_port.block.instance_id,
            destination_port=to_port.port_id
        )

