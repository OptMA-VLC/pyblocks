from dataclasses import dataclass, field
from typing import Optional, List, Union

from src.bdk.block_distribution_id import BlockDistributionId
from src.bdk.ports.port_id import PortId
from src.meow_sim.entity.block.user_parameter_entity import UserParameterEntity
from src.meow_sim.entity.block.available_parameter_entity import AvailableParameterEntity
from src.meow_sim.entity.block.block_instance_id import BlockInstanceId
from src.meow_sim.entity.block.interface_block_runtime import IBlockRuntime
from src.meow_sim.entity.block.port_entity import PortEntity


@dataclass
class BlockEntity:
    instance_id: BlockInstanceId
    distribution_id: BlockDistributionId
    name: str
    runtime: Optional[IBlockRuntime] = None
    inputs: List[PortEntity] = field(default_factory=list)
    outputs: List[PortEntity] = field(default_factory=list)
    available_params: List[AvailableParameterEntity] = field(default_factory=list)
    user_params: List[UserParameterEntity] = field(default_factory=list)

    def get_input(self, port: Union[PortEntity, PortId]):
        return self._get_port_in_list(self.inputs, port)

    def has_input(self, port: Union[PortEntity, PortId]) -> bool:
        try:
            self._get_port_in_list(self.inputs, port)
        except KeyError:
            return False

        return True

    def get_output(self, port: Union[PortEntity, PortId]):
        return self._get_port_in_list(self.outputs, port)

    def has_output(self, port: Union[PortEntity, PortId]) -> bool:
        try:
            self._get_port_in_list(self.outputs, port)
        except KeyError:
            return False

        return True

    def _get_port_in_list(self, port_list: List[PortEntity], port: Union[PortEntity, PortId]) -> PortEntity:
        if isinstance(port, PortEntity):
            port_id = port.port_id
        elif isinstance(port, PortId):
            port_id = port
        else:
            raise ValueError(f'port is not an instance of {PortEntity.__name__} or {PortId.__name__}')

        for port in port_list:
            if port.port_id == port_id:
                return port

        raise KeyError(f"PortEntity '{port_id}' does not exist")
