import sys

from src.meow_sim.logger import logger

from src.meow_sim.block_library.block_library import BlockLibrary
from src.meow_sim.simul_graph.simulation_graph import SimulationGraph
from src.meow_sim.simul_plan.plan_loader import PlanLoader
from src.meow_sim.simul_plan.plan_validator import PlanValidator


def main():
    logger.info('Meow!  :cat:')

    check_requirements()

    # logger.info('Loading block library...')
    # block_lib = BlockLibrary()
    # block_lib.load_from_dir(BlockLibrary.BLOCK_PATH)
    # logger.info(f'Block library loaded. Found [green]{len(block_lib)}[/green] blocks.')
    #
    # logger.info('Loading simulation plan...', end=' ')
    # plan = PlanLoader.load()
    # logger.info('[green]OK[/green]', no_tag=True)
    #
    # logger.info('Validating plan...', end=' ')
    # validation_errors = PlanValidator.validate(plan)
    # logger.info('[green]OK[/green]', no_tag=True)
    #
    # logger.info('Building simulation graph...')
    # simul_graph = SimulationGraph()
    # for block in plan.blocks:
    #     simul_graph.add_block(block)
    #
    # for connection in plan.connections:
    #     simul_graph.add_connection(connection)
    #
    # simul_graph.plot_graph()


def check_requirements():
    major_ver, minor_ver, _, _, _ = sys.version_info
    if major_ver < 2:
        logger.error('Python 2 is not supported. This program was written in Python 3.8')
        raise RuntimeError('Python 2 not supported.')

    if minor_ver < 8:
        logger.warn(
            f'This program was written in Python 3.8 but is being run in Python {major_ver}.{minor_ver}. '
            'Errors may occur. Consider updating your Python interpreter.'
        )

    try:
        import tkinter
    except ImportError as ex:
        logger.warn('Can\'t import tkinter. Plotting will fail.')
        logger.warn('tkinter can\'t be installed by pip and is needed as a backend to matplotlib.')
        logger.warn('To install on Linux run: sudo apt-get install python3-tk')


if __name__ == "__main__":
    main()
