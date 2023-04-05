from dataclasses import dataclass
from typing import List

from src.pyblock_sim.entity.project.command.command_entity import CommandEntity
from src.pyblock_sim.entity.project.graph_specification import GraphSpecification


@dataclass
class ProjectEntity:
    graph_spec: GraphSpecification
    commands: List[CommandEntity]
