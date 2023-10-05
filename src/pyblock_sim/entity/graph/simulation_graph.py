from typing import List

import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.dag

from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_entity import BlockEntity
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.entity.graph.connection_entity import ConnectionEntity


class SimulationGraph:
    _graph: nx.DiGraph

    def __init__(self):
        self._graph = nx.MultiDiGraph()

    @property
    def blocks(self) -> List[BlockEntity]:
        blocks = []
        for (_, block) in self._graph.nodes.data(data='block'):
            blocks.append(block)
        return blocks

    @property
    def connections(self) -> List[ConnectionEntity]:
        connections = []
        for (_, _, conn) in self._graph.edges.data(data='connection'):
            connections.append(conn)
        return connections

    def add_block(self, block: BlockEntity):
        for existing_block in self.blocks:
            if existing_block.instance_id == block.instance_id:
                raise RuntimeError(f"Can't add block with instance id '{block.instance_id}' "
                                   f"because it already exists in graph")

        self._graph.add_node(block.instance_id, block=block)
        pass

    def get_block(self, block_id: BlockInstanceId) -> BlockEntity:
        for block in self.blocks:
            if block.instance_id == block_id:
                return block

        raise KeyError(f"Block with instance id '{block_id}' does not exist in simulation graph")

    def add_connection(self, connection: ConnectionEntity):
        origin_block = self.get_block(connection.origin.block)
        destination_block = self.get_block(connection.destination.block)

        if origin_block.instance_id == destination_block.instance_id:
            raise ValueError('Connecting a Block to itself is not supported')

        if not origin_block.has_output(connection.origin.port):
            raise ValueError(f"Port with Id '{connection.origin.port}' is not an output of block '{origin_block.instance_id}'")

        if not destination_block.has_input(connection.destination.port):
            raise ValueError(f"Port with Id '{connection.destination.port}' is not an input of block '{destination_block.instance_id}'")

        if self._has_connection_to_port(connection.destination.block, connection.destination.port):
            raise ValueError(
                f"Can't add connection to block '{destination_block.instance_id}', "
                f"port '{connection.destination.port}' because there is already a connection to that port"
            )

        self._graph.add_edge(origin_block.instance_id, destination_block.instance_id, connection=connection)

    def get_incoming_connections(self, block_id: BlockInstanceId) -> List[ConnectionEntity]:
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

    def _has_connection_to_port(self, block_id: BlockInstanceId, port_id: PortId) -> bool:
        incoming_connections = self.get_incoming_connections(block_id)
        for conn in incoming_connections:
            if conn.destination.port == port_id:
                return True

        return False

    def plot_graph(self):
        fig, ax = plt.subplots()
        nx.draw_networkx(
            self._graph,
            None,
            ax,
            with_labels=True
        )
        plt.show()
