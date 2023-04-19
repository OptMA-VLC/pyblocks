from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List

from src.pyblock.block.block_distribution_id import BlockDistributionId
from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.entity.block.interface_block_runtime import IBlockRuntime
from src.pyblock_sim.entity.block.param_manager import ParameterManager
from src.pyblock_sim.entity.block.port_entity import PortEntity


@dataclass
class BlockEntity:
    class State(Enum):
        CREATED = auto()
        LOADED = auto()

    distribution_id: BlockDistributionId
    instance_id: BlockInstanceId
    name: str
    state: State
    param_manager: Optional[ParameterManager]
    runtime: Optional[IBlockRuntime]
    inputs: List[PortEntity]
    outputs: List[PortEntity]

    def __init__(
            self,
            distribution_id: BlockDistributionId,
            name: str,
            instance_id: BlockInstanceId = None
    ):
        self.distribution_id = distribution_id
        self.name = name
        self.state = BlockEntity.State.CREATED
        self.param_manager = ParameterManager()
        self.runtime = None
        self.inputs = []
        self.outputs = []

        if instance_id is None:
            self.instance_id = BlockInstanceId(f'{self.distribution_id}@{id(self)}')
        else:
            self.instance_id = instance_id

    def load(self, runtime: IBlockRuntime):
        self.runtime = runtime
        self.inputs = runtime.list_inputs(self)
        self.outputs = runtime.list_outputs(self)
        self.param_manager.set_block_params(runtime.list_parameters())

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
