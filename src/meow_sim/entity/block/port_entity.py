from dataclasses import dataclass
from typing import Type, Any

from src.bdk.ports.port_id import PortId
from src.meow_sim.entity.block.port_instance_id import PortInstanceId


@dataclass
class PortEntity:
    block: 'BlockEntity'
    port_id: PortId
    type: Type = Any

    @property
    def instance_id(self) -> PortInstanceId:
        return PortInstanceId(self.block.instance_id, self.port_id)