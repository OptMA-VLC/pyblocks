from dataclasses import dataclass
from typing import Optional

from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.use_case.simulate_use_case.simulation_exceptions import SimulationException


@dataclass
class SimulationStepReport:
    block_instance_id: BlockInstanceId
    total_number_of_steps: Optional[int] = None
    step_number: Optional[int] = None
    success: bool = True
    execution_time: float = 0.0
    stdout: str = ''
    stderr: str = ''
    exception: Optional[SimulationException] = None
