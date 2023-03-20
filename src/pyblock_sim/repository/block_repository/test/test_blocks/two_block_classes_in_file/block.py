from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo


class FirstBlock(BaseBlock):
    def get_info(self):
        super().__init__(BlockInfo(
            distribution_id='com.pyblock.two_block_classes.first_block',
            name='Test Block',
            description='',
        ))

    def run(self):
        print('Hello Block!')


class SecondBlock(BaseBlock):
    def __init__(self):
        super().__init__(BlockInfo(
            distribution_id='com.pyblock.two_block_classes.second_block',
            name='Test Block',
            description='',
        ))

    def run(self):
        print('Hello Block!')

