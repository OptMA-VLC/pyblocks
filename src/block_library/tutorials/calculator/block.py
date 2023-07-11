from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.parameter import Parameter
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort


class CalculatorBlock(BaseBlock):
    def __init__(self):
        # define metadata
        self.info = BlockInfo(
            distribution_id='com.pyblocks.tutorials.calculator',
            name='Arithmetic Calculator',
            description="This simple arithmetic calculator shows how to implement a custom block"
        )

        #define inputs and outputs
        self.input_a = InputPort(port_id='a')
        self.input_b = InputPort(port_id='b')
        self.output = OutputPort(port_id='output')

        #define parameters
        self.operation = Parameter(param_id='operation', default='+')

    def run(self):
        in_a = self.input_a.signal
        in_b = self.input_b.signal
        operation = self.operation.value

        if operation == '+':
            result = in_a + in_b
        elif operation == '-':
            result = in_a - in_b
        elif operation == '*':
            result = in_a * in_b
        elif operation == '/':
            result = in_a / in_b
        else:
            raise ValueError(
                f"Invalid value '{operation}' for parameter 'operation'."
                f"Valid values are: '+', '-', '*' and '/'"
            )

        self.output.signal = result
