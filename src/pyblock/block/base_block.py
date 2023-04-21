from abc import abstractmethod, ABC

from .block_info import BlockInfo


class BaseBlock(ABC):
    info: BlockInfo

    @abstractmethod
    def run(self):
        pass

    def __repr__(self):
        return f"<Block of type '{self.info.distribution_id}' at {id(self)}>"
