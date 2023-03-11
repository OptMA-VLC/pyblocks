import uuid
from dataclasses import dataclass, field

from src.meow_sim.entity.block.port import Port
from src.meow_sim.entity.connection_id import ConnectionId


def _generate_connection_id() -> ConnectionId:
    return ConnectionId(uuid.uuid4())


@dataclass
class Connection:
    from_port: Port
    to_port: Port
    id: ConnectionId = field(default_factory=_generate_connection_id)

