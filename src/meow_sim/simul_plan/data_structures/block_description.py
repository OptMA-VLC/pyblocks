from dataclasses import dataclass, field
from typing import List

from .param_description import ParamDescription


@dataclass
class BlockDescription:
    instance_of: str
    block_id: str
    params: List[ParamDescription] = field(default_factory=list)
