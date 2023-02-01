import sys
from pathlib import Path

from src.meow_sim.logger import logger
from src.meow_sim.repository.block_repository.block_repository import BlockRepository


def main():
    str_demo()


def str_demo():
    logger.info('Meow!  :cat:')

    check_requirements()

    # create block_repo
    logger.info('Loading block library...  ', end='')
    block_repo = BlockRepository()
    block_lib_path = Path('./blocks')
    block_repo.index_dir(block_lib_path)
    logger.info('[green]ok[/green]', no_tag=True)

    logger.info('Loading simulation Blocks...  ', end='')
    block_str_src = block_repo.load_by_dist_name('br.ufmg.optma.string_source')
    block_to_upper = block_repo.load_by_dist_name('br.ufmg.optma.to_upper')
    block_str_print = block_repo.load_by_dist_name('br.ufmg.optma.string_print')
    logger.info('[green]ok[/green]', no_tag=True)

    logger.info('Running block str_source...', end='')
    block_str_src.apply_parameters([
        ('string', 'Hello world!')
    ])
    block_str_src.run()
    sig_1 = block_str_src.get_signal('str_out')
    logger.info('[green]ok[/green]', no_tag=True)

    logger.info('Running block to_upper...', end='')
    block_to_upper.set_signal('str_in', sig_1)
    block_to_upper.run()
    sig_2 = block_to_upper.get_signal('str_out')
    logger.info('[green]ok[/green]', no_tag=True)

    logger.info('Running block str_print...', end='')
    block_str_print.set_signal('str_in', sig_2)
    block_str_print.run()
    logger.info('[green]ok[/green]', no_tag=True)


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
