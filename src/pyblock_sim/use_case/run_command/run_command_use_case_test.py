import csv

import numpy.testing
import numpy as np

from src.pyblock import TimeSignal
from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.entity.project.command.command_entity import CommandType
from src.pyblock_sim.entity.project.command.save_command_entity import SaveCommandEntity
from src.pyblock_sim.entity.project.signal_selector import SignalSelector
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository
from src.pyblock_sim.use_case.run_command.run_command_use_case import RunCommandUseCase


class TestRunCommandUseCase_SaveCommand:
    def test_ok(self, tmp_path):
        sig_1 = np.array([0, 1, 2])
        sig_2 = TimeSignal(
            time=[0.0, 0.1],
            signal=[4, 5]
        )

        signal_repo = SignalRepository()
        block = BlockInstanceId('block')
        port_1 = PortId('port_1')
        port_2 = PortId('port_2')
        signal_repo.set(block, port_1, sig_1)
        signal_repo.set(block, port_2, sig_2)
        use_case = RunCommandUseCase(signal_repo)

        cmd = SaveCommandEntity(
            type=CommandType.SAVE,
            save_path=str(tmp_path/'result.csv'),
            signals=[
                SignalSelector(block=block, port=port_1, signal_name=None),
                SignalSelector(block=block, port=port_2, signal_name=None),
            ]
        )
        use_case.run_command(cmd)

        with open(tmp_path/'result.csv') as f:
            reader = csv.reader(f)
            lines = []
            for line in reader:
                lines.append(line)

            assert len(lines) == 4
            numpy.testing.assert_equal(
                lines[0], ['block::port_1', 'block::port_2 (time)', 'block::port_2 (signal)']
            )
            numpy.testing.assert_equal(
                lines[1], ['0',              '0.0',                  '4']
            )
            numpy.testing.assert_equal(
                lines[2], ['1',              '0.1',                  '5']
            )
            numpy.testing.assert_equal(
                lines[3], ['2',              '',                     '']
            )
