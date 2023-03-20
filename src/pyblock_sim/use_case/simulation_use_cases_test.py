from typing import List

import pytest

from src.pyblock_sim.entity.block.block_entity import BlockEntity
from src.pyblock_sim.entity.graph.graph_builder_util import GraphBuilderUtil
from src.pyblock_sim.entity.simulation.simulation_steps import SimulationStep
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository
from src.pyblock_sim.use_case.simulation_use_cases import SimulationUseCases


class TestGenerateSteps:
    @property
    def _use_case(self) -> SimulationUseCases:
        return SimulationUseCases(signal_repo=SignalRepository())

    def test_simple_graph(self):
        graph_builder = GraphBuilderUtil() \
            .with_block('block_1', outputs=['out']) \
            .with_block('block_2', inputs=['in']) \
            .with_connection('block_1', 'out', 'block_2', 'in')

        graph = graph_builder.build()
        block_1 = graph_builder.get_block('block_1')
        block_2 = graph_builder.get_block('block_2')

        steps = self._use_case.create_simulation_steps(graph)

        assert len(steps) == 2
        assert steps[0].block.instance_id == block_1.instance_id
        assert steps[1].block.instance_id == block_2.instance_id

    def test_single_block(self):
        graph = GraphBuilderUtil().with_block('block_1').build()

        steps = self._use_case.create_simulation_steps(graph)

        assert len(steps) == 1

    def test_c_depends_on_a_and_b(self):
        graph_builder = GraphBuilderUtil() \
            .with_block('block_a', inputs=['in'], outputs=['out']) \
            .with_block('block_b', inputs=['in'], outputs=['out']) \
            .with_block('block_c', inputs=['in_a', 'in_b']) \
            .with_connection('block_a', 'out', 'block_c', 'in_a') \
            .with_connection('block_b', 'out', 'block_c', 'in_b')
        graph = graph_builder.build()
        block_c = graph_builder.get_block('block_c')

        steps = self._use_case.create_simulation_steps(graph)

        assert len(steps) == 3
        # order between block_a and block_b is not important
        assert steps[2].block.instance_id == block_c.instance_id

    def test_independent_sub_graphs(self):
        graph_builder = GraphBuilderUtil() \
            .with_block('block_a', inputs=['in'], outputs=['out']) \
            .with_block('block_b', inputs=['in'], outputs=['out']) \
            .with_block('block_c', inputs=['in'], outputs=['out']) \
            .with_block('block_d', inputs=['in'], outputs=['out']) \
            .with_connection('block_a', 'out', 'block_b', 'in') \
            .with_connection('block_c', 'out', 'block_d', 'in')
        graph = graph_builder.build()

        steps = self._use_case.create_simulation_steps(graph)

        assert len(steps) == 4

        block_a_pos = self._find_block_position_in_steps(steps, graph_builder.get_block('block_a'))
        block_b_pos = self._find_block_position_in_steps(steps, graph_builder.get_block('block_b'))
        block_c_pos = self._find_block_position_in_steps(steps, graph_builder.get_block('block_c'))
        block_d_pos = self._find_block_position_in_steps(steps, graph_builder.get_block('block_d'))

        assert block_a_pos < block_b_pos
        assert block_c_pos < block_d_pos

    def test_intermediate_block(self):
        graph_builder = GraphBuilderUtil() \
            .with_block('block_a', inputs=['in'], outputs=['out']) \
            .with_block('block_b', inputs=['in'], outputs=['out']) \
            .with_block('block_c', inputs=['in_1', 'in_2'], outputs=['out']) \
            .with_connection('block_a', 'out', 'block_c', 'in_2') \
            .with_connection('block_a', 'out', 'block_b', 'in') \
            .with_connection('block_b', 'out', 'block_c', 'in_1')
        graph = graph_builder.build()

        steps = self._use_case.create_simulation_steps(graph)

        assert len(steps) == 3

        block_a_pos = self._find_block_position_in_steps(steps, graph_builder.get_block('block_a'))
        block_b_pos = self._find_block_position_in_steps(steps, graph_builder.get_block('block_b'))
        block_c_pos = self._find_block_position_in_steps(steps, graph_builder.get_block('block_c'))

        assert block_a_pos < block_b_pos
        assert block_b_pos < block_c_pos

    def test_reject_circular_dependency(self):
        graph_builder = GraphBuilderUtil() \
            .with_block('block_1', inputs=['in'], outputs=['out']) \
            .with_block('block_2', inputs=['in'], outputs=['out']) \
            .with_block('block_3', inputs=['in'], outputs=['out']) \
            .with_connection('block_1', 'out', 'block_2', 'in') \
            .with_connection('block_2', 'out', 'block_3', 'in') \
            .with_connection('block_3', 'out', 'block_1', 'in')
        graph = graph_builder.build()

        with pytest.raises(Exception):
            self._use_case.create_simulation_steps(graph)

    def _find_block_position_in_steps(self, steps: List[SimulationStep], block: BlockEntity):
        for (idx, step) in enumerate(steps):
            if step.block.instance_id == block.instance_id:
                return idx
        raise ValueError(f"Block with instance id '{block.instance_id}' not found in steps")

