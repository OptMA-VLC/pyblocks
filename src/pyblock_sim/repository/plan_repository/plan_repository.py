from src.pyblock_sim.entity.block.block_entity import BlockEntity
from src.pyblock_sim.entity.graph.simulation_graph import SimulationGraph


class PlanRepository:
    def load(self) -> SimulationGraph:
        BlockEntity

        # create blocks
        #   have:
        #     - dist_id
        #     - instance_id
        #     - name
        #   missing:
        #     - runtime
        #     - inputs, outputs, params
        # create connections
        #
        #

        # block states?
        #   - created
        #   - loaded


        plan_file = PlanFile()


class PlanFile:
    pass

def _create_simple_plan_for_dev() -> SimulationPlan:
    return SimulationPlan(
        blocks=[
            BlockDescription(
                instance_of='br.ufmg.optma.vlc_lifi.channel',
                id='str_source',
                params=[
                    ParamDescription(key='string', value='Hello World!')
                ]
            ),
            BlockDescription(
                instance_of='br.ufmg.optma.test.string_print',
                id='str_print',
            )
        ],
        connections=[
            ConnectionDescription(
                id='conn_1',
                from_block='str_source',
                from_port='out',
                to_block='str_print',
                to_port='in'
            )
        ]
    )
