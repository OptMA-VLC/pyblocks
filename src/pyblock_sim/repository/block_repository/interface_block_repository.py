import pathlib
from abc import ABC, abstractmethod
from typing import List

from src.pyblock.block.block_distribution_id import BlockDistributionId
from src.pyblock_sim.entity.block.interface_block_runtime import IBlockRuntime
from src.pyblock_sim.entity.block_library.indexing_result import IndexingResult


class IBlockRepository(ABC):
    @abstractmethod
    def index_blocks(self, block_library_path: pathlib.Path) -> IndexingResult:
        pass

    @abstractmethod
    def list_blocks(self) -> List[BlockDistributionId]:
        pass

    @abstractmethod
    def is_block_known(self, distribution_id: BlockDistributionId) -> bool:
        pass

    @abstractmethod
    def get_runtime(self, distribution_id: BlockDistributionId) -> IBlockRuntime:
        pass
