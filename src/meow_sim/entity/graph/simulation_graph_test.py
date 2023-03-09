# - reject adding block with same id
# - allow adding block with same id after removing
#
# - reject adding edge between non-existing blocks
from typing import List

import pytest

from src.meow_sim.entity.graph.simulation_graph import SimulationGraph
from src.meow_sim.entity.data_structures import BlockDescription, ConnectionDescription


class TestSimulationGraph_Blocks:
    def test_add_node(self):
        block = _block('block_1')
        graph = SimulationGraph()

        graph.add_block(block)

        assert len(graph.blocks) is 1

    def test_reject_duplicate_block(self):
        block = _block('block_1')
        graph = SimulationGraph()

        graph.add_block(block)
        with pytest.raises(Exception):
            graph.add_block(block)

    def test_remove_block(self):
        block = _block('block_1')
        graph = SimulationGraph()

        # removing a non-existing node should be a no-op
        graph.remove_node('foo')
        assert len(graph.blocks) is 0

        # removes a block
        graph.add_block(block)
        assert len(graph.blocks) is 1
        graph.remove_block(block.id)
        assert len(graph.blocks) is 0

        # should support re-adding block after removal
        graph.add_block(block)
        assert len(graph.blocks) is 1


class TestSimulationGraph_Connections:
    def test_add_connection(self):
        graph = self._graph_with_blocks(['block_1', 'block_2'])
        conn = ConnectionDescription(
            id='conn_1',
            from_block='block_1',
            to_block='block_2'
        )
        graph.add_connection()

    def _graph_with_blocks(self, block_ids: List[str]) -> SimulationGraph:
        g = SimulationGraph()
        for block_id in block_ids:
            g.add_block(_block(block_id))

        return g


def _block(block_id: str) -> BlockDescription:
    return BlockDescription(instance_of=f'com.test.{block_id}', id=f'{block_id}')
