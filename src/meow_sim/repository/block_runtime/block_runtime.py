from typing import List

from src.meow_sim.entity.block_id import BlockId
from src.meow_sim.entity.param_bundle import ParamBundle
from src.meow_sim.entity.port import Port
from src.meow_sim.repository.block_adapter.block_adapter import BlockAdapter


class BlockRuntimeView:
    state: str
    params: ParamBundle
    ports: List[Port]


class BlockRuntime:
    def get_view(self, block_id: BlockId) -> BlockRuntimeView:
        pass

    def load(self, adapter: BlockAdapter):
        pass

    def apply_params(self, block_id: BlockId):
        pass

    def run(self, block_id: BlockId, inputs: InputBundle):
        pass
