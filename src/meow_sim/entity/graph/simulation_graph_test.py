from typing import Tuple

import pytest

from src.bdk.ports.port_id import PortId
from src.meow_sim.entity.block.block import Block
from src.meow_sim.entity.block.port import Port
from src.meow_sim.entity.connection import Connection
from src.meow_sim.entity.graph.simulation_graph import SimulationGraph


class TestSimulationGraph:
    def test_add_block(self):
        graph = SimulationGraph()
        block = self._block(dist_id='block_1')

        graph.add_block(block)

        assert len(graph.blocks) is 1

    def test_add_two_blocks_of_same_type(self):
        block_1 = self._block(dist_id='dist_id_1', instance_id='block_1')
        block_2 = self._block(dist_id='dist_id_1', instance_id='block_2')
        graph = SimulationGraph()

        graph.add_block(block_1)
        graph.add_block(block_2)

        assert len(graph.blocks) is 2

    def test_adding_existing_instance_is_update(self):
        block_1 = self._block(dist_id='dist_id_1', instance_id='same_instance')
        block_2 = self._block(dist_id='dist_id_2', instance_id='same_instance')
        graph = SimulationGraph()

        graph.add_block(block_1)
        graph.add_block(block_2)

        assert len(graph.blocks) is 1
        block = graph.blocks[0]
        assert block.distribution_id is block_2.distribution_id

    def test_add_connection(self):
        (graph, block_1, block_2) = self._graph_with_two_blocks()
        conn = Connection(
            from_port=block_1.outputs[0],
            to_port=block_2.inputs[0]
        )

        graph.add_connection(conn)

        assert len(graph.connections) is 1

    def test_cant_connect_input_to_output(self):
        (graph, block_1, block_2) = self._graph_with_two_blocks()
        conn = Connection(
            from_port=block_2.inputs[0],
            to_port=block_1.outputs[0]
        )

        with pytest.raises(Exception):
            graph.add_connection(conn)

    def test_cant_connect_output_to_output(self):
        (graph, block_1, block_2) = self._graph_with_two_blocks()
        conn = Connection(
            from_port=block_1.outputs[0],
            to_port=block_2.outputs[0]
        )

        with pytest.raises(Exception):
            graph.add_connection(conn)

    def test_cant_connect_input_to_input(self):
        (graph, block_1, block_2) = self._graph_with_two_blocks()
        conn = Connection(
            from_port=block_1.inputs[0],
            to_port=block_2.inputs[0]
        )

        with pytest.raises(Exception):
            graph.add_connection(conn)

    def test_cant_connect_block_to_itself(self):
        (graph, block_1, block_2) = self._graph_with_two_blocks()
        conn = Connection(
            from_port=block_1.outputs[0],
            to_port=block_1.inputs[0]
        )

        with pytest.raises(Exception):
            graph.add_connection(conn)

    def test_ignore_duplicate_connection(self):
        (graph, block_1, block_2) = self._graph_with_two_blocks()
        conn = Connection(
            from_port=block_1.outputs[0],
            to_port=block_2.inputs[0]
        )

        graph.add_connection(conn)
        assert len(graph.connections) is 1
        graph.add_connection(conn)
        assert len(graph.connections) is 1

    def _block(self, dist_id='dist_id', instance_id='instance_id') -> Block:
        return Block(
            distribution_id=dist_id,
            instance_id=instance_id,
            name='Test Block',
            runtime=None
        )

    def _graph_with_two_blocks(self) -> Tuple[SimulationGraph, Block, Block]:
        block_1 = self._block(instance_id='inst_id_1', dist_id='block_1')
        block_1.inputs = [Port(block=block_1, port_id=PortId('port_in'))]
        block_1.outputs = [Port(block=block_1, port_id=PortId('port_out'))]
        block_2 = self._block(instance_id='inst_id_2', dist_id='block_2')
        block_2.inputs = [Port(block=block_2, port_id=PortId('port_in'))]
        block_2.outputs = [Port(block=block_2, port_id=PortId('port_out'))]

        g = SimulationGraph()
        g.add_block(block_1)
        g.add_block(block_2)

        return g, block_1, block_2
