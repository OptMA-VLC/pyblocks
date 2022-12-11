from src.meow_sim.data_structures.config import BlockDescription, Config, ConnectionDescription, ParamDescription, \
    PortDescription


class ConfigLoader:
    @staticmethod
    def load() -> Config:
        return Config(
            blocks=[BlockDescription(
                id='str_source',
                path='$BLOCKS/string_source',
                params=[
                    ParamDescription(key='string', value='Hello World!')
                ],
                outputs=[
                    PortDescription(id='out')
                ]
            ), BlockDescription(
                id='str_print',
                path='$BLOCKS/string_print',
                inputs=[
                    PortDescription(id='in')
                ]
            )],
            connections=[
                ConnectionDescription(
                    from_block='str_source',
                    from_port='out',
                    to_block='str_print',
                    to_port='in'
                )
            ]
        )
