import pytest

from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.param import Param
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort
from src.pyblock.testing.block_validation.validate_block import validate, BlockValidationError


class TestValidateBlock:
    def test_ok(self):
        class OkBlock(BaseBlock):
            def __init__(self):
                self.info = BlockInfo('com.test.block')
                self.input = InputPort('in_port')
                self.output = OutputPort('out_port')
                self.param = Param('param', type=str)

            def run(self):
                pass

        block = OkBlock()
        validate(block)

    def test_no_info(self):
        class NoInfoBlock(BaseBlock):
            def run(self):
                pass

        with pytest.raises(BlockValidationError):
            block = NoInfoBlock()
            validate(block)

    def test_duplicate_port_ids(self):
        class DuplicatePortIdBlock(BaseBlock):
            def __init__(self):
                self.info = BlockInfo('com.test.block')
                self.port_1 = InputPort('port', type=str)
                self.port_2 = OutputPort('port', type=str)

            def run(self):
                pass

        with pytest.raises(BlockValidationError):
            block = DuplicatePortIdBlock()
            validate(block)

    def test_duplicate_params(self):
        class DuplicateParamBlock(BaseBlock):
            def __init__(self):
                self.info = BlockInfo('com.test.block')
                self.param_1 = Param('param', type=str)
                self.param_2 = Param('param', type=str)

            def run(self):
                pass

        with pytest.raises(BlockValidationError):
            block = DuplicateParamBlock()
            validate(block)
