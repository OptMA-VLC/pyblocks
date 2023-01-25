from src.bdk.base_block import BaseBlock
from src.bdk.block_info import BlockInfo


class StringSource(BaseBlock):
    def get_info(self):
        return BlockInfo(
            distribution_name='br.ufmg.optma.string_source',
            name='String Data Source',
            description='',
        )

    def validate_inputs(self, inputs):
        pass

    def run(self, inputs, params):
        pass
