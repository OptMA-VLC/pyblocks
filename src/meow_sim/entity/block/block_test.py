from src.bdk.block_distribution_id import BlockDistributionId
from src.bdk.ports.port_id import PortId
from src.meow_sim.entity.block.block_entity import BlockEntity
from src.meow_sim.entity.block.port_entity import PortEntity


class TestBlock:
    def test_has_input(self):
        block = BlockEntity(distribution_id=BlockDistributionId('dist_id'), name='')
        port_1 = PortEntity(block=block, port_id=PortId('port_1'))
        port_2 = PortEntity(block=block, port_id=PortId('port_2'))

        block.outputs = [port_1]
        assert block.has_input(port_1) is False
        assert block.has_input(port_1.port_id) is False

        block.outputs = []
        block.inputs = [port_1]
        assert block.has_input(port_1) is True
        assert block.has_input(port_1.port_id) is True
        assert block.has_input(port_2) is False
        assert block.has_input(port_2.port_id) is False

    def test_has_output(self):
        block = BlockEntity(distribution_id=BlockDistributionId('dist_id'), name='Test Block')
        port_1 = PortEntity(block=block, port_id=PortId('port_1'))
        port_2 = PortEntity(block=block, port_id=PortId('port_2'))

        block.inputs = [port_1]
        assert block.has_output(port_1) is False
        assert block.has_output(port_1.port_id) is False

        block.inputs = []
        block.outputs = [port_1]
        assert block.has_output(port_1) is True
        assert block.has_output(port_1.port_id) is True
        assert block.has_output(port_2) is False
        assert block.has_output(port_2.port_id) is False
