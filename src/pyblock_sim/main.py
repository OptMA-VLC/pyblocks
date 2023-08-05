import sys
from pathlib import Path

from src.pyblock_sim.repository.cli.cli import CLI
from src.pyblock_sim.repository.cli.object_printers.indexing_result_printer import IndexingResultPrinter
from src.pyblock_sim.repository.cli.object_printers.simulation_report_printer import SimulationReportPrinter
from src.pyblock_sim.repository.cli.print_level import PrintLevel
from src.pyblock_sim.repository.path_manager.path_manager import PathManager
from src.pyblock_sim.repository_provider import RepositoryProvider
from src.pyblock_sim.use_case.run_from_file.run_from_file_use_case import RunFromFileUseCase


def main():
    cli = setup_cli()

    cli.print('Welcome to pyblocks-sim!  :cat:')
    check_requirements(cli)

    path_manager = PathManager(
        run_path=Path.cwd(),
        project_rel_path=Path('../experiments/vlc_param_sweep/project.json'),
        # project_rel_path=Path('../tutorials/2_calculator/project.json'),
        block_library_rel_path=Path('../block_library')
    )

    repo_provider = RepositoryProvider(cli=cli, path_manager=path_manager)

    run_from_file_use_case = RunFromFileUseCase(repo_provider)
    run_from_file_use_case.run_from_file()


def setup_cli() -> CLI:
    cli = CLI()
    cli.register_obj_printer(IndexingResultPrinter())
    cli.register_obj_printer(SimulationReportPrinter())
    return cli


def check_requirements(cli: CLI):
    major_ver, minor_ver, _, _, _ = sys.version_info
    if major_ver < 3:
        cli.print('Python 2 is not supported. This program was written in Python 3.8', level=PrintLevel.ERROR)
        raise RuntimeError('Python 2 not supported.')

    if minor_ver < 8:
        cli.print(
            f'This program was written in Python 3.8 but is being run in Python {major_ver}.{minor_ver}. '
            'Errors may occur. Consider updating your Python interpreter.',
            level=PrintLevel.WARNING
        )

    try:
        import tkinter
    except ImportError as ex:
        cli.print('Can\'t import tkinter. Plotting will fail.', level=PrintLevel.WARNING)
        cli.print('tkinter can\'t be installed by pip and is needed as a backend to matplotlib.', level=PrintLevel.WARNING)
        cli.print('To install on Linux run: sudo apt-get install python3-tk', level=PrintLevel.WARNING)


if __name__ == "__main__":
    main()
