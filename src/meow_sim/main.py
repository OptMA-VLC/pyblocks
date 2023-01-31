import sys
from pathlib import Path

from src.meow_sim import use_cases
from src.meow_sim.entity.block import Block
from src.meow_sim.entity.simulation_graph import SimulationGraph
from src.meow_sim.logger import logger
from src.meow_sim.repository.block_repository.block_repository import BlockRepository
from src.meow_sim.repository.plan_repository.plan_repository import PlanRepository


def main():
    logger.info('Meow!  :cat:')

    check_requirements()

    # create block_repo
    logger.info('Loading block library...  ')
    block_repo = BlockRepository()
    block_lib_path = Path('./blocks')
    block_repo.index_dir(block_lib_path)
    logger.info('Load block library: [green]ok[/green]')

    # load plan
    logger.info('Loading simulation plan...', end=' ')
    plan = PlanRepository().load()
    logger.info('[green]ok[/green]', no_tag=True)

    graph = use_cases.build_simulation_graph_from_plan(plan)
    # load blocks

    # create graph
    logger.info('Creating simulation graph')
    graph = SimulationGraph()

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
