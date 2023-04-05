from dataclasses import dataclass
from typing import Optional

from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.use_case.simulate.simulation_exceptions import SimulationException


@dataclass
class SimulationStepReport:
    block_instance_id: BlockInstanceId
    success: bool = True
    execution_time: float = 0.0
    stdout: str = ''
    stderr: str = ''
    exception: Optional[SimulationException] = None
