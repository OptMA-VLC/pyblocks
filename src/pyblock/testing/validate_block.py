import inspect
import sys
from typing import List

from src.pyblock.block.base_block import BaseBlock
from src.pyblock.block.block_info import BlockInfo
from src.pyblock.block.params.param import Param
from src.pyblock.block.ports.input_port import InputPort
from src.pyblock.block.ports.output_port import OutputPort


def validate(block: BaseBlock):
    _validate_block_info(block)
    _validate_unique_ports(block)
    _validate_unique_params(block)


class BlockValidationError(Exception):
    pass


def _validate_block_info(block):
    correct_info_text = ""
    "To provide the required block information, set the property self.info in your initializer:\n"
    "class MyBlock(BaseBlock):\n"
    "    def __init__(self):\n"
    "        self.info = BlockInfo(\n"
    "            distribution_id='com.my_org.my_block_distribution_id'\n"
    "            ...\n"
    "        )\n"

    try:
        info = block.info
    except AttributeError:
        raise BlockValidationError(
            "Block information was not provided." + correct_info_text
        )

    if not isinstance(info, BlockInfo):
        raise BlockValidationError(
            f"Block information, determined by 'self.info' must be of type '{BlockInfo.__name__}' but"
            f"an object of type '{type(info).__name__}' was found.\n" + correct_info_text
        )


def _validate_unique_ports(block: BaseBlock):
    inputs = _find_attributes(block, matching_type=InputPort)
    outputs = _find_attributes(block, matching_type=OutputPort)

    ids = [port.id for port in inputs] + [port.id for port in outputs]
    seen_ids = []

    for port_id in ids:
        if port_id in seen_ids:
            raise BlockValidationError(
                f"Two ports (inputs or outputs) have the id '{port_id}'. Port id's must be unique."
            )
        else:
            seen_ids.append(port_id)


def _validate_unique_params(block):
    params = _find_attributes(block, matching_type=Param)

    ids = [param.id for param in params]
    seen_ids = []

    for param_id in ids:
        if param_id in seen_ids:
            raise BlockValidationError(
                f"Two parameters have the same id '{param_id}'. Parameter ids must be unique."
            )
        else:
            seen_ids.append(param_id)


def _find_attributes(obj: object, matching_type=object) -> List:
    def check_is_attr(x):
        return not inspect.isroutine(x)

    members = inspect.getmembers(obj, check_is_attr)

    result = []
    for (_, attr) in members:
        if isinstance(attr, matching_type):
            result.append(attr)

    return result
