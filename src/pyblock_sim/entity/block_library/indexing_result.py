from enum import Enum
from pathlib import Path
from typing import List

from src.pyblock.block.block_distribution_id import BlockDistributionId


class IndexingResult:
    indexed_path: Path
    items: List['ResultItem']

    def __init__(self, indexed_path: Path):
        self.indexed_path = indexed_path
        self.items = []

    def append(self, item: 'ResultItem'):
        self.items.append(item)

    def __str__(self):
        s = f"Block Result for '{self.indexed_path.resolve()}'\n"
        for (idx, item) in enumerate(self.items):
            s += f"    [{idx}] {item.path.stem} - {item.outcome}\n"
        return s


class ResultItem:
    class ResultType(Enum):
        SUCCESS = 'success'
        FAILED = 'fail'
        SKIPPED = 'skipped'

    path: Path
    outcome: 'ResultItem.ResultType'
    distribution_id: BlockDistributionId
    exception: Exception

    @classmethod
    def success(cls, path: Path, id: BlockDistributionId) -> 'ResultItem':
        res = ResultItem()
        res.outcome = ResultItem.ResultType.SUCCESS
        res.path = path
        res.distribution_id = id
        return res

    @classmethod
    def failed(cls, path: Path, exception: Exception) -> 'ResultItem':
        res = ResultItem()
        res.outcome = ResultItem.ResultType.FAILED
        res.path = path
        res.exception = exception
        return res

    @classmethod
    def skipped(cls, path: Path) -> 'ResultItem':
        res = ResultItem()
        res.outcome = ResultItem.ResultType.SKIPPED
        res.path = path
        return res
