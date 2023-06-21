import os.path
import sys
from pathlib import Path

from src.pyblock_sim.repository_provider import RepositoryProvider
from src.pyblock_sim.use_case.run_from_file.run_from_file_use_case import RunFromFileUseCase
from src.pyblock_sim.util.logger import logger
from src.pyblock_sim.util.set_directory import set_directory


def main():
    logger.info('Meow!  :cat:')
    check_requirements()

    project_path = Path('../experiments/vlc_lab/project.json')

    block_library_rel_path = Path('../block_library')
    block_library_path = Path(os.path.relpath(block_library_rel_path, project_path.parent))
    with set_directory(project_path.parent):
        repo_provider = RepositoryProvider(block_library_path)
        run_from_file_use_case = RunFromFileUseCase(repo_provider)
        run_from_file_use_case.run_from_file(Path(project_path.name))


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


if __name__ == "__main__":
    main()
