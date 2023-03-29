from src.pyblock.block.params.param_id import ParamId
from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.entity.graph.connection_entity import ConnectionEntity


class BlockParamException(Exception):
    def __init__(self, block_instance_id: BlockInstanceId, param_id: ParamId):
        super().__init__(
            f"An error occurred while applying parameter '{param_id}' to the block '{block_instance_id}'"
        )


class BlockInputException(Exception):
    def __init__(self, conn: ConnectionEntity):
        super().__init__(
            f"An error occurred while transferring signal from port '{conn.origin_block}'::'{conn.origin_port}' "
            f"to port '{conn.destination_block}'::'{conn.destination_port}'"
        )


class BlockOutputException(Exception):
    def __init__(self, block_instance_id: BlockInstanceId, port_id: PortId):
        super().__init__(
            f"An error occurred while getting the output from port "
            f"'{block_instance_id}'::'{port_id}'"
        )


class BlockRunningException(Exception):
    block_instance_id: BlockInstanceId
    internal_block_exception: Exception

    def __init__(self, block_instance_id: BlockInstanceId, block_ex: Exception):
        super().__init__(f"The block '{block_instance_id}' produced an Exception while Running")

        self.block_instance_id = block_instance_id
        self.internal_block_exception = block_ex
