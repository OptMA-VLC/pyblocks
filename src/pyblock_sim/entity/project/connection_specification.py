from dataclasses import dataclass

from src.pyblock_sim.entity.project.port_selector import PortSelector


@dataclass
class ConnectionSpecification:
    origin: PortSelector
    destination: PortSelector
