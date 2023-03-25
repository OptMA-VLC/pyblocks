from dataclasses import dataclass

from src.pyblock_sim.entity.project.graph_specification import GraphSpecification


@dataclass
class ProjectEntity:
    graph_spec: GraphSpecification

