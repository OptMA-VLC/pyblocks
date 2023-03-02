import sys
from pathlib import Path
from typing import List

from matplotlib import pyplot as plt

from src.bdk.signals.signal_wave import SignalWave
from src.blocks.ltspice_runner.ltspice_runner_config import LTSpiceRunnerConfig
from src.meow_sim.logger import logger
from src.meow_sim.repository.block_adapter.block_adapter import BlockAdapter
from src.meow_sim.repository.block_repository.block_repository import BlockRepository
from src.meow_sim.repository.block_repository.indexing_result import IndexingResult, ResultItem


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
    block_ltspice_class = block_repo.get_class_from_dist_name('br.ufmg.optma.ltspice_runner')
    block_ltspice = BlockAdapter(block_ltspice_class)
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

    logger.info('Running block ltspice_runner...', end='')
    block_ltspice.apply_parameters([
        ('config', config)
    ])
    block_ltspice.set_input('signal_in', input_signal)
    block_ltspice.run()
    logger.info('[green]ok[/green]', no_tag=True)

    output_signal = block_ltspice.get_output('signal_out')

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
