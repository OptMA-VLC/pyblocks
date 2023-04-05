from typing import Optional

from src.pyblock.block.params.param_id import ParamId
from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.entity.graph.connection_entity import ConnectionEntity


class SimulationException(Exception):
    inner_exception: Optional[Exception]


class BlockParamException(SimulationException):
    def __init__(self, block_instance_id: BlockInstanceId, param_id: ParamId, inner_ex: Optional[Exception]):
        self.inner_exception = inner_ex
        super().__init__(
            f"An error occurred while applying parameter '{param_id}' to the block '{block_instance_id}'"
        )


class BlockInputException(SimulationException):
    def __init__(self, conn: ConnectionEntity, inner_ex: Optional[Exception]):
        self.inner_exception = inner_ex
        super().__init__(
            f"An error occurred while transferring signal from port '{conn.origin_block}'::'{conn.origin_port}' "
            f"to port '{conn.destination_block}'::'{conn.destination_port}'"
        )


class BlockOutputException(SimulationException):
    def __init__(self, block_instance_id: BlockInstanceId, port_id: PortId,  inner_ex: Optional[Exception]):
        self.inner_exception = inner_ex
        super().__init__(
            f"An error occurred while getting the output from port "
            f"'{block_instance_id}'::'{port_id}'"
        )


class BlockRunningException(SimulationException):
    block_instance_id: BlockInstanceId

    def __init__(self, block_instance_id: BlockInstanceId, block_ex: Exception):
        super().__init__(f"The block '{block_instance_id}' produced an Exception while Running")

        self.inner_exception = block_ex
        self.block_instance_id = block_instance_id
