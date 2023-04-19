import uuid
from dataclasses import field
from typing import Union

from src.pyblock_sim.entity.block.port_entity import PortEntity
from src.pyblock_sim.entity.graph.connection_instance_id import ConnectionInstanceId
from src.pyblock_sim.entity.project.port_selector import PortSelector
from src.pyblock_sim.entity.project.signal_selector import SignalSelector


def _generate_connection_id() -> ConnectionInstanceId:
    return ConnectionInstanceId(uuid.uuid4())



class ConnectionEntity:
    origin: SignalSelector
    destination: PortSelector
    # origin_block: BlockInstanceId
    # origin_port: PortId
    # destination_block: BlockInstanceId
    # destination_port: PortId
    id: ConnectionInstanceId = field(default_factory=_generate_connection_id)

    def __init__(
            self,
            origin: Union[SignalSelector, PortSelector],
            destination: PortSelector
    ):
        self.destination = destination
        if isinstance(origin, PortSelector):
            self.origin = SignalSelector(block=origin.block, port=origin.port)
        else:
            self.origin = origin

    @staticmethod
    def from_port_entity(origin: PortEntity, destination: PortEntity):
        return ConnectionEntity(
            origin=PortSelector(origin.block.instance_id, origin.port_id),
            destination=PortSelector(destination.block.instance_id, destination.port_id)
        )
