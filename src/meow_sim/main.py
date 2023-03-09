import sys
from pathlib import Path

from matplotlib import pyplot as plt

from src.bdk.params.param_id import ParamId
from src.bdk.ports.port_id import PortId
from src.bdk.signals.signal_wave import SignalWave
from src.blocks.ltspice_runner.ltspice_runner_config import LTSpiceRunnerConfig
from src.meow_sim.entity.connection import Connection
from src.meow_sim.entity.simulation.simulation_steps import SimulationStep
from src.meow_sim.logger import logger
from src.meow_sim.repository.block_repository.block_repository import BlockRepository
from src.meow_sim.repository.block_repository.indexing_result import IndexingResult, ResultItem
from src.meow_sim.repository.signal_repository.signal_repository import SignalRepository
from src.meow_sim.use_case.simulation_use_cases import SimulationUseCases


def main():
    logger.info('Meow!  :cat:')
    check_requirements()

    lt_spice_demo()


def print_indexing_result(result: IndexingResult):
    logger.verbose(f'Checked {result.indexed_path.absolute()} for blocks')

    for item in result.items:
        if item.type is ResultItem.ResultType.SUCCESS:
            logger.verbose(f'  /{item.path.name.ljust(20)} - [green]Success[/green]')
        elif item.type is ResultItem.ResultType.FAILED:
            logger.verbose(f'  /{item.path.name.ljust(20)} - [red]Failed[/red]')
            logger.verbose(f'    (failed with exception {item.exception.__class__.__name__})')
        elif item.type is ResultItem.ResultType.SKIPPED:
            logger.verbose(f'  /{item.path.name.ljust(20)} - [white]Skipped[/white]')


def lt_spice_demo():
    logger.info('Loading block library...  ')
    block_repo = BlockRepository()
    block_lib_path = Path('./blocks')
    indexing_result = block_repo.index_dir(block_lib_path)
    logger.info('Loading block library...  [green]ok[/green]')
    print_indexing_result(indexing_result)

    logger.info('Loading simulation Blocks...  ')
    block_ltspice = block_repo.get_block('br.ufmg.optma.ltspice_runner')
    logger.info('Loading simulation Blocks...  [green]ok[/green]')

    input_signal = make_triangle_wave()
    config = LTSpiceRunnerConfig(
        schematic_file='blocks/ltspice_runner/test_data/Transmissor.asc',
        file_name_in_circuit='TX_input.txt',
        add_instructions=[
            '; Simulation settings',
            '.tran 0 1000m 0 1u'
        ],
        probe_signals=['I(D1)']
    )

    conn_input = Connection(id='conn_in')
    conn_output = Connection(id='conn_out')

    steps = [
        SimulationStep(
            block=block_ltspice,
            params={
                ParamId('config'): config
            },
            inputs={
                PortId('signal_in'): conn_input
            },
            outputs={
                PortId('signal_out'): conn_output
            }
        )
    ]

    signal_repo = SignalRepository()
    simulation_use_cases = SimulationUseCases(signal_repo)

    signal_repo.set(conn_input.id, input_signal)
    simulation_use_cases.simulate(steps)

    output_signal = signal_repo.get(conn_output.id)

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(input_signal.time, input_signal.wave, color='r', label='input')
    ax2.plot(output_signal.time, output_signal.wave, label='output')
    plt.legend()
    plt.show()


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
