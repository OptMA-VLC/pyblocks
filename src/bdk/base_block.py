import inspect
from abc import abstractmethod, ABC
from typing import List

from .block_info import BlockInfo
from .params.parameter import Parameter
from .ports.input import Input
from .ports.output import Output


class BaseBlock(ABC):
    block_info: BlockInfo
    params: List[Parameter]
    inputs: List[Input]
    outputs: List[Output]

    def __init__(self, block_info: BlockInfo):
        self.block_info = block_info

        self.params = self._get_class_attributes(matching_type=Parameter)
        self.inputs = self._get_class_attributes(matching_type=Input)
        self.outputs = self._get_class_attributes(matching_type=Output)

    @abstractmethod
    def run(self):
        pass

    def __str__(self):
        s = '------------------------------------------------------------\n'
        s += f'Block "{self.block_info.name}" @{id(self)}\n\n'
        s += 'Params:\n'
        for p in self.params:
            s += f'  - {p.id} ({p.type.__name__})\n'
        s += 'Inputs:\n'
        for i in self.inputs:
            s += f'  - {i.id} ({i.type.__name__})\n'
        s += 'Outputs:\n'
        for o in self.outputs:
            s += f'  - {o.id} ({o.type.__name__})\n'
        s += '------------------------------------------------------------\n'
        return s

    def _get_class_attributes(self, matching_type=object) -> List:
        def check_is_attr(x):
            return not inspect.isroutine(x)

        members = inspect.getmembers(self, check_is_attr)

        result = []
        for (_, attr) in members:
            if isinstance(attr, matching_type):
                result.append(attr)

        return result


def _assert_required_fields(self):
    pass
    # if self.block_info is None:
    #     raise NotImplementedError('Block class must set the \'block_info\' class property')
    #
    # if not isinstance(self.block_info, BlockInfo):
    #     raise TypeError(
    #         f'Required property \'self.block_info\' must be a {BlockInfo} object but is of type {self.block_info.__class__}'
    #     )
    #
    # if not isinstance(self.params, ParamBundle):
    #     raise TypeError(
    #         f'Required property \'self.params\' must be a {ParamBundle} object but is of type {self.params.__class__}'
    #     )
    #
    # if not isinstance(self.inputs, PortBundle):
    #     raise TypeError(
    #         f'Required property \'self.inputs\' must be a {PortBundle} object but is of type {self.inputs.__class__}'
    #     )
    #
    # if not isinstance(self.outputs, PortBundle):
    #     raise TypeError(
    #         f'Required property \'self.outputs\' must be a {PortBundle} object but is of type {self.outputs.__class__}'
    #     )

