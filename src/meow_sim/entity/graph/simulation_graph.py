import uuid
from typing import List

import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.dag

from src.meow_sim.entity.block.block_entity import BlockEntity
from src.meow_sim.entity.block.block_instance_id import BlockInstanceId
from src.meow_sim.entity.block.port_entity import PortEntity
from src.meow_sim.entity.connection import Connection
from src.meow_sim.entity.connection_id import ConnectionId


class SimulationGraph:
    _graph: nx.DiGraph

    def __init__(self):
        self._graph = nx.DiGraph()

    @property
    def blocks(self) -> List[BlockEntity]:
        blocks = []
        for (_, block) in self._graph.nodes.data(data='block'):
            blocks.append(block)
        return blocks

    @property
    def connections(self) -> List[Connection]:
        connections = []
        for (_, _, conn) in self._graph.edges.data(data='connection'):
            connections.append(conn)
        return connections

    def add_block(self, block: BlockEntity):
        self._graph.add_node(block.instance_id, block=block)
        pass

    def add_connection(self, connection: Connection):
        origin_port = connection.from_port
        origin_block: BlockEntity = origin_port.block
        destination_port = connection.to_port
        destination_block: BlockEntity = destination_port.block

        if None in [connection, origin_port, origin_block, destination_port, destination_block]:
            raise ValueError('Required information to add connection missing')

        if origin_block.instance_id == destination_block.instance_id:
            raise ValueError('Connecting a Block to itself is not supported')

        if not origin_block.has_output(origin_port):
            raise ValueError(f"PortEntity '{origin_port.port_id}' is not an output of block '{origin_block.name}'")

        if not destination_block.has_input(destination_port):
            raise ValueError(f"PortEntity '{destination_port.port_id}' is not an input of block '{destination_block.name}'")

        for conn in self.connections:
            is_to_same_block = conn.to_port.block.instance_id == destination_port.block.instance_id
            is_to_same_port = conn.to_port.port_id == destination_port.port_id

            if is_to_same_block and is_to_same_port:
                raise ValueError(
                    f"Can't add connection to block '{destination_block.name}', port '{destination_port.port_id}' "
                    f"because there is already a connection to that port (with connection id '{conn.id}')"
                )

        self._graph.add_edge(origin_block.instance_id, destination_block.instance_id, connection=connection)

    def get_incoming_connections(self, block_id: BlockInstanceId) -> List[Connection]:
        incoming_conns = []
        for _, _, edge_data in self._graph.in_edges(block_id, data=True):
            incoming_conns.append(edge_data['connection'])
        return incoming_conns

    def topological_sort(self) -> List[BlockEntity]:
        if not networkx.algorithms.dag.is_directed_acyclic_graph(self._graph):
            raise RuntimeError("Can't sort the simulation graph because it contains a cyclical dependency")

        nodes = list(networkx.algorithms.dag.topological_sort(self._graph))
        blocks = []

        for node in nodes:
            block = self._graph.nodes[node]['block']
            blocks.append(block)

        return blocks

    def plot_graph(self):
        fig, ax = plt.subplots()
        nx.draw_networkx(
            self._graph,
            None,
            ax,
            with_labels=True
        )
        plt.show()
