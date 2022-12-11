from src.meow_sim.logger import logger
from src.meow_sim.data_structures.config import BlockDescription, Config, ConnectionDescription, ParamDescription, \
    PortDescription


def main():
    logger.info("Meow!  :cat:\n")

    config = load_config()
    logger.info("[green]Loaded config![/green]", ':rainbow:')

    logger.warn(config)

    # meow simul.json
    #
    #  gerar report do que vai ser executado
    #
    #  ir reportando status da simulaçao
    #
    #  reportar resultado?
    #    - escrever em um arquivo e reportar o path?
    #    - escrever gráficos em arquivos?


def load_config() -> Config:
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


if __name__ == "__main__":
    main()
