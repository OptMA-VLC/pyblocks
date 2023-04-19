from dataclasses import dataclass

from src.pyblock_sim.entity.project.port_selector import PortSelector
from src.pyblock_sim.entity.project.signal_selector import SignalSelector


@dataclass
class ConnectionSpecification:
    origin: SignalSelector
    destination: PortSelector
