import os.path
import sys
from pathlib import Path

from matplotlib import pyplot as plt

from src.pyblock.block.ports.port_id import PortId
from src.pyblock.signals.signal_wave import SignalWave
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.repository.block_repository.block_repository import BlockRepository
from src.pyblock_sim.repository.block_repository.block_repository_exceptions import NoBlockPyFile
from src.pyblock_sim.repository.block_repository.indexing_result import IndexingResult, ResultItem
from src.pyblock_sim.repository.project_repository.project_repository import ProjectRepository
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository
from src.pyblock_sim.use_case.build_simulation_graph_use_case import BuildSimulationGraphUseCase
from src.pyblock_sim.use_case.compute_simulation_steps_use_case import ComputeSimulationStepsUseCase
from src.pyblock_sim.use_case.simulate_use_case import SimulateUseCase
from src.pyblock_sim.util.logger import logger
from src.pyblock_sim.util.set_directory import set_directory


def main():
    logger.info('Meow!  :cat:')
    check_requirements()

    project_path = Path('../examples/ltspice_integration/project.json')

    library_rel_path = Path('../block_library')
    library_path = Path(os.path.relpath(library_rel_path, project_path.parent))
    with set_directory(project_path.parent):
        run_simulator(library_path, Path(project_path.name))


def run_simulator(library_path: Path, project_path: Path):
    block_repo = BlockRepository(library_path)
    signal_repo = SignalRepository()

    build_graph_use_case = BuildSimulationGraphUseCase(block_repo)
    compute_simulation_steps_use_case = ComputeSimulationStepsUseCase()
    simulate_use_case = SimulateUseCase(signal_repo, block_repo)

    logger.info('Loading block library...      ', end='')
    indexing_result = block_repo.index_blocks()
    logger.info('[green]ok[/green]', no_tag=True)
    print_indexing_result(indexing_result)

    logger.info('Loading project...            ', end='')
    project = ProjectRepository().load(project_path)
    logger.info('[green]ok[/green]', no_tag=True)

    logger.info('Building simulation graph...  ', end='')
    simulation_graph = build_graph_use_case.build_simulation_graph(project.graph_spec)
    logger.info('[green]ok[/green]', no_tag=True)

    logger.info('Computing simulation steps... ', end='')
    simulation_steps = compute_simulation_steps_use_case.compute_simulation_steps(simulation_graph)
    logger.info('[green]ok[/green]', no_tag=True)

    logger.info('Starting Simulation...')
    simulate_use_case.simulate(simulation_steps)
    logger.info('Simulation Done.')

    input_signal = signal_repo.get(BlockInstanceId('sig_gen_1'), PortId('signal_out'))
    output_signal = signal_repo.get(BlockInstanceId('ltspice_rx'), PortId('signal_out'))

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(input_signal.time, input_signal.wave, color='r', label='input')
    ax2.plot(output_signal.time, output_signal.wave, label='output')
    plt.legend()
    plt.show()


def print_indexing_result(result: IndexingResult):
    logger.verbose(f'Checked {result.indexed_path.absolute()} for blocks')

    for item in result.items:
        if item.outcome is ResultItem.ResultType.SUCCESS:
            logger.verbose(f'  /{item.path.name.ljust(20)} - [green]Success[/green]')
        elif item.outcome is ResultItem.ResultType.FAILED:
            if isinstance(item.exception, NoBlockPyFile):
                logger.verbose(f'  /{item.path.name.ljust(20)} - [white]Not a Block[/white]')
            else:
                logger.verbose(f'  /{item.path.name.ljust(20)} - [red]Failed[/red]')
                logger.verbose(f'    (failed with exception {item.exception.__class__.__name__} - {item.exception})')
        elif item.outcome is ResultItem.ResultType.SKIPPED:
            logger.verbose(f'  /{item.path.name.ljust(20)} - [white]Skipped[/white]')


def check_requirements():
    major_ver, minor_ver, _, _, _ = sys.version_info
    if major_ver < 3:
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


def make_triangle_wave(end_time=1, step=0.001, period=0.2):
    time = []
    wave = []

    current_time = 0
    current_wave = 0
    wave_delta = 1/(period/step)
    while current_time <= end_time:
        time.append(current_time)
        wave.append(current_wave)

        current_time += step
        current_wave += wave_delta

        if current_wave > 1:
            current_wave = 0

    return SignalWave(time, wave)


if __name__ == "__main__":
    main()
