import pytest

from src.pyblock_sim.entity.project.signal_selector import SignalSelector


class TestSignalSelector:
    def test_simple_signal(self):
        block = 'my_block'
        port = 'my_port'

        signal_selector = SignalSelector.parse(f'{block}::{port}')

        assert signal_selector.block == block
        assert signal_selector.port == port

    def test_multisignal(self):
        block = 'my_block'
        port = 'my_port'
        signal = 'my_signal_name'

        signal_selector = SignalSelector.parse(f'{block}::{port}[{signal}]')

        assert signal_selector.block == block
        assert signal_selector.port == port
        assert signal_selector.signal_name == signal

    def test_reject_wrong_formats(self):
        with pytest.raises(ValueError):
            SignalSelector.parse('my_block::my_port[my_signal')

        with pytest.raises(ValueError):
            SignalSelector.parse('my_block::my_port[my_signal]extra')

        with pytest.raises(ValueError):
            SignalSelector.parse('my_block::my_port [my_signal]')

        with pytest.raises(ValueError):
            SignalSelector.parse('my_block::my_port::my_signal')

        with pytest.raises(ValueError):
            SignalSelector.parse('my_block[my_signal]')

        with pytest.raises(ValueError):
            SignalSelector.parse('just_a_string')
