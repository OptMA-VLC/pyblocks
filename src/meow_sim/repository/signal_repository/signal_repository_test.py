from typing import Any

from src.meow_sim.entity.connection_id import ConnectionId
from src.meow_sim.repository.signal_repository.signal_repository import SignalRepository


class TestSignalRepository:
    def test_create_and_read(self):
        repo = SignalRepository()
        signal = TestSignalRepository.SimpleSignal('signal_value')
        conn_id = ConnectionId('sig_1')

        repo.set(conn_id, signal)
        read_signal = repo.get(conn_id)

        assert read_signal.value == signal.value

    def test_update(self):
        repo = SignalRepository()
        signal = TestSignalRepository.SimpleSignal('signal_value')
        signal2 = TestSignalRepository.SimpleSignal('signal_value_2')
        conn_id = ConnectionId('sig_1')

        repo.set(conn_id, signal)
        repo.set(conn_id, signal2)
        read_signal = repo.get(conn_id)

        assert read_signal.value == signal2.value

    def test_cant_affect_stored_signal_from_returned_value(self):
        repo = SignalRepository()
        signal = TestSignalRepository.ComposedSignal('original_value')
        conn_id = ConnectionId('sig_1')

        repo.set(conn_id, signal)
        read_signal = repo.get(conn_id)
        read_signal.inner_signal.value = 'altered_value'
        read_signal_2 = repo.get(conn_id)

        assert read_signal_2.inner_signal.value == 'original_value'

    class SimpleSignal:
        value: Any

        def __init__(self, value):
            self.value = value

    class ComposedSignal:
        inner_signal: 'TestSignalRepository.SimpleSignal'

        def __init__(self, value):
            self.inner_signal = TestSignalRepository.SimpleSignal(value)
