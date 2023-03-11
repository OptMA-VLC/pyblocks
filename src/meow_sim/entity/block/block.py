from dataclasses import dataclass, field
from typing import Optional, List, Union

from src.bdk.block_distribution_id import BlockDistributionId
from src.bdk.ports.port_id import PortId
from src.meow_sim.entity.block.block_instance_id import BlockInstanceId
from src.meow_sim.entity.block.interface_block_runtime import IBlockRuntime
from src.meow_sim.entity.block.port import Port


@dataclass
class Block:
    instance_id: BlockInstanceId
    distribution_id: BlockDistributionId
    name: str
    runtime: Optional[IBlockRuntime] = None
    inputs: List[Port] = field(default_factory=list)
    outputs: List[Port] = field(default_factory=list)

    def has_input(self, port: Union[Port, PortId]) -> bool:
        return self._is_port_in_list(self.inputs, port)

    def has_output(self, port: Union[Port, PortId]) -> bool:
        return self._is_port_in_list(self.outputs, port)

    def _is_port_in_list(self, port_list: List[Port], port: Union[Port, PortId]) -> bool:
        print(f'{PortId.__name__}')
        if isinstance(port, Port):
            port_id = port.port_id
        elif isinstance(port, PortId):
            port_id = port
        else:
            raise ValueError(f'port is not an instance of {Port.__name__} or {PortId.__name__}')

        for port in port_list:
            if port.port_id == port_id:
                return True
        return False
