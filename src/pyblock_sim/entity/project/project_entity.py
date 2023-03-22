from typing import List


class BlockSpecification:
    dist_id: str
    instance_id: str
    name: str


class ConnectionSpecification:
    origin_block: str
    origin_port: str
    destination_block: str
    destination_port: str


class GraphSpecification:
    blocks: List[BlockSpecification]
    connections: List[ConnectionSpecification]


class ProjectEntity:
    graph_spec: GraphSpecification

