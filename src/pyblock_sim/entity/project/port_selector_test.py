import pytest

from src.pyblock_sim.entity.project.port_selector import PortSelector


class TestPortSelector:
    def test_ok(self):
        block = 'my_block'
        port = 'my_port'

        port_selector = PortSelector.parse(f'{block}::{port}')

        assert port_selector.block == block
        assert port_selector.port == port

    def test_rejects_wrong_formats(self):
        with pytest.raises(ValueError):
            PortSelector.parse('::my_port')

        with pytest.raises(ValueError):
            PortSelector.parse('my_block::')

        with pytest.raises(ValueError):
            PortSelector.parse('a_single_string_without_double_colons')

    def test_rejects_signal_selector(self):
        with pytest.raises(ValueError):
            PortSelector.parse('my_block::my_port[signal_name]')
