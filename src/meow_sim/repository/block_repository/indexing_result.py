from enum import Enum
from pathlib import Path
from typing import List

from src.bdk.block_distribution_id import BlockDistributionId


class IndexingResult:
    indexed_path: Path
    items: List['ResultItem']

    def __init__(self, indexed_path: Path):
        self.indexed_path = indexed_path
        self.items = []

    def append(self, item: 'ResultItem'):
        self.items.append(item)


class ResultItem:
    class ResultType(Enum):
        SUCCESS = 'success'
        FAILED = 'fail'
        SKIPPED = 'skipped'

    path: Path
    type: 'ResultItem.ResultType'
    block_id: BlockDistributionId
    exception: Exception

    @classmethod
    def success(cls, path: Path, id: BlockDistributionId) -> 'ResultItem':
        res = ResultItem()
        res.type = ResultItem.ResultType.SUCCESS
        res.path = path
        res.block_id = id
        return res

    @classmethod
    def failed(cls, path: Path, exception: Exception) -> 'ResultItem':
        res = ResultItem()
        res.type = ResultItem.ResultType.FAILED
        res.path = path
        res.exception = exception
        return res

    @classmethod
    def skipped(cls, path: Path) -> 'ResultItem':
        res = ResultItem()
        res.type = ResultItem.ResultType.SKIPPED
        res.path = path
        return res
