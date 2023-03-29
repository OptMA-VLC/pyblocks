from dataclasses import dataclass
from typing import Optional

from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId


@dataclass
class SimulationStepReport:
    block_instance_id: BlockInstanceId
    success: bool = True
    execution_time: float = 0.0
    stdout: str = ''
    stderr: str = ''
    exception: Optional[Exception] = None
