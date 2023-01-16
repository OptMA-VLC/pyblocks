from .data_structures import \
    SimulPlan, BlockDescription, ConnectionDescription, ParamDescription, PortDescription


class PlanLoader:
    @staticmethod
    def load() -> SimulPlan:
        return SimulPlan(
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
