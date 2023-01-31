from src.meow_sim.entity.block import Block
from src.meow_sim.entity.plan_description.block_description import BlockDescription
from src.meow_sim.entity.plan_description.simulation_plan import SimulationPlan
from src.meow_sim.entity.simulation_graph import SimulationGraph
from src.meow_sim.repository.block_repository.block_repository import BlockRepository


class UseCases:
    block_repo: BlockRepository

    def __init__(self, block_repo: BlockRepository):
        self.block_repo = block_repo

    def build_simulation_graph_from_plan(self, plan: SimulationPlan) -> SimulationGraph:
        for block_desc in plan.blocks:
            # load block
            adapter = self.block_repo.load_by_dist_name(block_desc.instance_of)

            b = Block(
                id=block_desc.id,
                runtime=adapter
            )

            # apply parameters to get ports

            # add block to graph

        # add connections to graph
