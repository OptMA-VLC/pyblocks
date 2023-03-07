from dataclasses import dataclass

from src.meow_sim.entity.connection_id import ConnectionId


@dataclass
class Connection:
    id: ConnectionId
