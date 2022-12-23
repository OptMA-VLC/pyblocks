from src.bdk.base_block import BaseBlock
from src.blocks.string_print.implementation import StringPrintImpl


class StringPrint(BaseBlock):
    def get_info(self):
        pass

    def validate_inputs(self, inputs):
        pass

    def run(self, inputs, params):
        StringPrintImpl.print('Hello Block!')
