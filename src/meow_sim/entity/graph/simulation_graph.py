import uuid
from typing import List

import matplotlib.pyplot as plt
import networkx as nx

from src.meow_sim.entity.block.block import Block
from src.meow_sim.entity.block.port import Port
from src.meow_sim.entity.connection import Connection
from src.meow_sim.entity.connection_id import ConnectionId


class SimulationGraph:
    _graph: nx.DiGraph

    def __init__(self):
        self._graph = nx.DiGraph()

    @property
    def blocks(self) -> List[Block]:
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

    def add_block(self, block: Block):
        self._graph.add_node(block.instance_id, block=block)
        pass

    def add_connection(self, connection: Connection):
        origin_port = connection.from_port
        origin_block: Block = origin_port.block
        destination_port = connection.to_port
        destination_block: Block = destination_port.block

        if None in [connection, origin_port, origin_block, destination_port, destination_block]:
            raise ValueError('Required information to add connection missing')

        if origin_block.instance_id == destination_block.instance_id:
            raise ValueError('Connecting a Block to itself is not supported')

        if not origin_block.has_output(origin_port):
            raise ValueError(f"Port '{origin_port.port_id}' is not an output of block '{origin_block.name}'")

        if not destination_block.has_input(destination_port):
            raise ValueError(f"Port '{destination_port.port_id}' is not an input of block '{destination_block.name}'")

        self._graph.add_edge(origin_block.instance_id, destination_block.instance_id, connection=connection)

    def plot_graph(self):
        fig, ax = plt.subplots()
        nx.draw_networkx(
            self._graph,
            None,
            ax,
            with_labels=True
        )
        plt.show()

