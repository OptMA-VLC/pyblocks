from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo


class SimpleTestBlock(BaseBlock):
    def __init__(self):
        super().__init__(BlockInfo(
            distribution_id='com.pyblock.simple_test_block',
            name='Test Block',
            description='',
        ))

    def run(self):
        print('Hello Block!')
