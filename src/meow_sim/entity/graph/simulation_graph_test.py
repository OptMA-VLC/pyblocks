from typing import Tuple

import pytest

from src.bdk.block_distribution_id import BlockDistributionId
from src.meow_sim.entity.block.block import Block
from src.meow_sim.entity.block.block_instance_id import BlockInstanceId
from src.meow_sim.entity.connection import Connection
from src.meow_sim.entity.graph.graph_builder_util import GraphBuilderUtil
from src.meow_sim.entity.graph.simulation_graph import SimulationGraph


class TestSimulationGraph_Blocks:
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

    def _block(self, dist_id='dist_id', instance_id='instance_id') -> Block:
        return Block(
            distribution_id=BlockDistributionId(dist_id),
            instance_id=BlockInstanceId(instance_id),
            name='Test Block',
            runtime=None
        )


class TestSimulationGraph_Connections:
    def test_add_connection(self):
        graph_builder = GraphBuilderUtil() \
            .with_block('block_1', inputs=['in'], outputs=['out']) \
            .with_block('block_2', inputs=['in'], outputs=['out'])
        graph = graph_builder.build()
        block_1 = graph_builder.get_block('block_1')
        block_2 = graph_builder.get_block('block_2')

        conn = Connection(
            from_port=block_1.outputs[0],
            to_port=block_2.inputs[0]
        )

        graph.add_connection(conn)

        assert len(graph.connections) is 1

    def test_cant_connect_input_to_output(self):
        graph_builder = GraphBuilderUtil() \
            .with_block('block_1', inputs=['in'], outputs=['out']) \
            .with_block('block_2', inputs=['in'], outputs=['out'])
        graph = graph_builder.build()
        block_1 = graph_builder.get_block('block_1')
        block_2 = graph_builder.get_block('block_2')

        conn = Connection(
            from_port=block_2.inputs[0],
            to_port=block_1.outputs[0]
        )

        with pytest.raises(Exception):
            graph.add_connection(conn)

    def test_cant_connect_output_to_output(self):
        graph_builder = GraphBuilderUtil() \
            .with_block('block_1', inputs=['in'], outputs=['out']) \
            .with_block('block_2', inputs=['in'], outputs=['out'])
        graph = graph_builder.build()
        block_1 = graph_builder.get_block('block_1')
        block_2 = graph_builder.get_block('block_2')

        conn = Connection(
            from_port=block_1.outputs[0],
            to_port=block_2.outputs[0]
        )

        with pytest.raises(Exception):
            graph.add_connection(conn)

    def test_cant_connect_input_to_input(self):
        graph_builder = GraphBuilderUtil() \
            .with_block('block_1', inputs=['in'], outputs=['out']) \
            .with_block('block_2', inputs=['in'], outputs=['out'])
        graph = graph_builder.build()
        block_1 = graph_builder.get_block('block_1')
        block_2 = graph_builder.get_block('block_2')

        conn = Connection(
            from_port=block_1.inputs[0],
            to_port=block_2.inputs[0]
        )

        with pytest.raises(Exception):
            graph.add_connection(conn)

    def test_cant_connect_block_to_itself(self):
        graph_builder = GraphBuilderUtil() \
            .with_block('block_1', inputs=['in'], outputs=['out'])
        graph = graph_builder.build()
        block_1 = graph_builder.get_block('block_1')

        conn = Connection(
            from_port=block_1.outputs[0],
            to_port=block_1.inputs[0]
        )

        with pytest.raises(Exception):
            graph.add_connection(conn)

    def test_cant_add_two_connections_to_same_input(self):
        graph_builder = GraphBuilderUtil() \
            .with_block('block_1', outputs=['out']) \
            .with_block('block_2', outputs=['out']) \
            .with_block('block_3', inputs=['in'])
        graph = graph_builder.build()
        block_1 = graph_builder.get_block('block_1')
        block_2 = graph_builder.get_block('block_2')
        block_3 = graph_builder.get_block('block_3')

        conn_1 = Connection(
            from_port=block_1.outputs[0],
            to_port=block_3.inputs[0]
        )
        conn_2 = Connection(
            from_port=block_2.outputs[0],
            to_port=block_3.inputs[0]
        )

        graph.add_connection(conn_1)
        with pytest.raises(Exception):
            graph.add_connection(conn_2)
