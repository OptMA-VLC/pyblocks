from src.bdk.base_block import BaseBlock
from src.bdk.block_info import BlockInfo
from src.blocks.string_print.implementation import StringPrintImpl


class StringPrint(BaseBlock):
    def get_info(self):
        return BlockInfo(
            distribution_name='br.ufmg.optma.string_print',
            name='String Printer',
            description='',
            params=[]
        )

    def validate_inputs(self, inputs):
        pass

    def run(self, inputs, params):
        StringPrintImpl.print('Hello Block!')
