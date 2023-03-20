import uuid
from dataclasses import dataclass, field

from src.pyblock_sim.entity.block.port_entity import PortEntity
from src.pyblock_sim.entity.connection_instance_id import ConnectionInstanceId


def _generate_connection_id() -> ConnectionInstanceId:
    return ConnectionInstanceId(uuid.uuid4())


@dataclass
class Connection:
    from_port: PortEntity
    to_port: PortEntity
    id: ConnectionInstanceId = field(default_factory=_generate_connection_id)

