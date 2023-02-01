from abc import abstractmethod, ABC
from typing import List

from .block_info import BlockInfo
from .params.parameter import Parameter
from .ports.PortBundle import PortBundle
from .signals.input_bundle import InputBundle
from .signals.output_bundle import OutputBundle
from ..meow_sim.entity.param_bundle import ParamBundle


class BaseBlock(ABC):
    block_info: BlockInfo
    params: ParamBundle
    inputs: PortBundle
    outputs: PortBundle

    def __init__(self):
        _assert_required_fields(self)

    @abstractmethod
    def run(self):
        pass


def _assert_required_fields(self):
    if self.block_info is None:
        raise NotImplementedError('Block class must set the \'block_info\' class property')

    if not isinstance(self.block_info, BlockInfo):
        raise TypeError(
            f'Required property \'self.block_info\' must be a {BlockInfo} object but is of type {self.block_info.__class__}'
        )

    if not isinstance(self.params, ParamBundle):
        raise TypeError(
            f'Required property \'self.params\' must be a {ParamBundle} object but is of type {self.params.__class__}'
        )

    if not isinstance(self.inputs, PortBundle):
        raise TypeError(
            f'Required property \'self.inputs\' must be a {PortBundle} object but is of type {self.inputs.__class__}'
        )

    if not isinstance(self.outputs, PortBundle):
        raise TypeError(
            f'Required property \'self.outputs\' must be a {PortBundle} object but is of type {self.outputs.__class__}'
        )

