from dataclasses import dataclass, field
from typing import List

from .param_description import ParamDescription
from ..param_bundle import ParamBundle


@dataclass
class BlockDescription:
    instance_of: str
    id: str
    params: ParamBundle = field(default_factory=ParamBundle)
