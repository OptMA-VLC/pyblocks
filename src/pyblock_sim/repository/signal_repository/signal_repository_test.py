from typing import Any

from src.pyblock.block.ports.port_id import PortId
from src.pyblock_sim.entity.block.block_instance_id import BlockInstanceId
from src.pyblock_sim.entity.block.port_instance_id import PortInstanceId
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository


class TestSignalRepository:
    def test_create_and_read(self):
        repo = SignalRepository()
        signal = TestSignalRepository.SimpleSignal('signal_value')
        port_id = PortInstanceId(BlockInstanceId('block_1'), PortId('port_1'))

        repo.set(port_id, signal)
        read_signal = repo.get(port_id)

        assert read_signal.value == signal.value

    def test_update(self):
        repo = SignalRepository()
        signal = TestSignalRepository.SimpleSignal('signal_value')
        signal2 = TestSignalRepository.SimpleSignal('signal_value_2')
        port_id = PortInstanceId(BlockInstanceId('block_1'), PortId('port_1'))

        repo.set(port_id, signal)
        repo.set(port_id, signal2)
        read_signal = repo.get(port_id)

        assert read_signal.value == signal2.value

    def test_cant_affect_stored_signal_from_returned_value(self):
        repo = SignalRepository()
        signal = TestSignalRepository.ComposedSignal('original_value')
        port_id = PortInstanceId(BlockInstanceId('block_1'), PortId('port_1'))

        repo.set(port_id, signal)
        read_signal = repo.get(port_id)
        read_signal.inner_signal.value = 'altered_value'
        read_signal_2 = repo.get(port_id)

        assert read_signal_2.inner_signal.value == 'original_value'

    class SimpleSignal:
        value: Any

        def __init__(self, value):
            self.value = value

    class ComposedSignal:
        inner_signal: 'TestSignalRepository.SimpleSignal'

        def __init__(self, value):
            self.inner_signal = TestSignalRepository.SimpleSignal(value)
