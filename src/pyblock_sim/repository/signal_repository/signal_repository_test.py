from typing import Any

import pytest

from src.pyblock.block.ports.port_id import PortId
from src.pyblock.signals.multi_signal import MultiSignal
from src.pyblock.signals.signal_name import SignalName
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.entity.project.signal_selector import SignalSelector
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository


class TestSignalRepository:
    def test_create_and_read(self):
        repo = SignalRepository()
        block_instance_id = BlockInstanceId('block_1')
        port_id = PortId('port_1')
        signal = TestSignalRepository.SimpleSignal('signal_value')

        repo.set(block_instance_id, port_id, signal)
        read_signal = repo.get(block_instance_id, port_id)

        assert read_signal.value == signal.value

    def test_update(self):
        repo = SignalRepository()
        block_instance_id = BlockInstanceId('block_1')
        port_id = PortId('port_1')
        signal = TestSignalRepository.SimpleSignal('signal_value')
        signal_2 = TestSignalRepository.SimpleSignal('signal_value_2')

        repo.set(block_instance_id, port_id, signal)
        repo.set(block_instance_id, port_id, signal_2)
        read_signal = repo.get(block_instance_id, port_id)

        assert read_signal.value == signal_2.value

    def test_cant_affect_stored_signal_from_returned_value(self):
        repo = SignalRepository()
        block_instance_id = BlockInstanceId('block_1')
        port_id = PortId('port_1')
        signal = TestSignalRepository.ComposedSignal('original_value')

        repo.set(block_instance_id, port_id, signal)
        read_signal = repo.get(block_instance_id, port_id)
        read_signal.inner_signal.value = 'altered_value'
        read_signal_2 = repo.get(block_instance_id, port_id)

        assert read_signal_2.inner_signal.value == 'original_value'

    def test_signal_selector_access(self):
        repo = SignalRepository()
        multi_signal = MultiSignal({
            'signal_1': 'signal_value',
            'signal_2': 'signal_value_2'
        })
        selector_sig_1 = SignalSelector(
            block=BlockInstanceId('block_inst'),
            port=PortId('port_id'),
            signal_name=SignalName('signal_1')
        )
        selector_sig_2 = SignalSelector(
            block=BlockInstanceId('block_inst'),
            port=PortId('port_id'),
            signal_name=SignalName('signal_2')
        )
        selector_sig_nonexistent = SignalSelector(
            block=BlockInstanceId('block_inst'),
            port=PortId('port_id'),
            signal_name=SignalName('does_not_exist')
        )

        repo.set(BlockInstanceId('block_inst'), PortId('port_id'), multi_signal)

        retrieved_sig_1 = repo.get_by_selector(selector_sig_1)
        retrieved_sig_2 = repo.get_by_selector(selector_sig_2)

        assert retrieved_sig_1 == 'signal_value'
        assert retrieved_sig_2 == 'signal_value_2'

        with pytest.raises(KeyError):
            repo.get_by_selector(selector_sig_nonexistent)

    class SimpleSignal:
        value: Any

        def __init__(self, value):
            self.value = value

    class ComposedSignal:
        inner_signal: 'TestSignalRepository.SimpleSignal'

        def __init__(self, value):
            self.inner_signal = TestSignalRepository.SimpleSignal(value)
