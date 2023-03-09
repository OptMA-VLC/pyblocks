from dataclasses import dataclass
from typing import Any, Dict

from src.bdk.params.param_id import ParamId
from src.bdk.ports.port_id import PortId
from src.meow_sim.entity.block import Block
from src.meow_sim.entity.connection import Connection


@dataclass
class SimulationStep:
    block: Block
    params: Dict[ParamId, Any]
    inputs: Dict[PortId, Connection]
    outputs: Dict[PortId, Connection]
