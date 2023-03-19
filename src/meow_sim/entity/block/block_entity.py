from dataclasses import dataclass, field
from enum import Enum, auto
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
    class State(Enum):
        CREATED = auto()
        LOADED = auto()

    distribution_id: BlockDistributionId
    name: str
    state: State = State.CREATED
    runtime: Optional[IBlockRuntime] = None
    inputs: List[PortEntity] = field(default_factory=list)
    outputs: List[PortEntity] = field(default_factory=list)
    available_params: List[AvailableParameterEntity] = field(default_factory=list)
    user_params: List[UserParameterEntity] = field(default_factory=list)

    @property
    def instance_id(self):
        return BlockInstanceId(f'{self.distribution_id}@{id(self)}')

    def load(self, runtime: IBlockRuntime):
        self.runtime = runtime
        self.inputs = runtime.list_inputs(self)
        self.outputs = runtime.list_outputs(self)
        self.available_params = runtime.list_params()
        self.state = BlockEntity.State.LOADED

    def get_input(self, port: PortId) -> PortEntity:
        return self._get_port_in_list(self.inputs, port)

    def has_input(self, port: PortId) -> bool:
        try:
            self._get_port_in_list(self.inputs, port)
        except KeyError:
            return False

        return True

    def get_output(self, port: PortId) -> PortEntity:
        return self._get_port_in_list(self.outputs, port)

    def has_output(self, port: PortId) -> bool:
        try:
            self._get_port_in_list(self.outputs, port)
        except KeyError:
            return False

        return True

    def _get_port_in_list(self, port_list: List[PortEntity], port_id: PortId) -> PortEntity:
        for port in port_list:
            if port.port_id == port_id:
                return port

        raise KeyError(f"The Block '{self.name}' has no port '{port_id}'")
