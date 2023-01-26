from src.meow_sim.entity.plan_description import BlockDescription, ConnectionDescription, ParamDescription
from src.meow_sim.entity.plan_description.simulation_plan import SimulationPlan


class PlanRepository:
    def load(self) -> SimulationPlan:
        return _create_simple_plan_for_dev()


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
