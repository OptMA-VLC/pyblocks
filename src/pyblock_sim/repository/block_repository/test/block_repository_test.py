import pathlib

from src.pyblock_sim.repository.block_repository.block_repository import BlockRepository
from src.pyblock_sim.repository.block_repository.indexing_result import IndexingResult, ResultItem


class TestBlockRepository:
    def test_indexing(self, tmp_path):
        indexing_result = BlockRepository().index_dir(self._discover_block_path())

        self._assert_indexing_result(indexing_result, 'simple_test_block', ResultItem.ResultType.SUCCESS)
        self._assert_indexing_result(indexing_result, 'no_block_file', ResultItem.ResultType.FAILED)
        self._assert_indexing_result(indexing_result, 'no_block_class', ResultItem.ResultType.FAILED)
        self._assert_indexing_result(indexing_result, 'two_block_classes_in_file', ResultItem.ResultType.FAILED)

    def _assert_indexing_result(self, result: IndexingResult, path_stem: str, outcome: ResultItem.ResultType):
        for item in result.items:
            if item.path.stem == path_stem:
                assert item.outcome == outcome
                return

        raise KeyError(f"IndexingResult does not contain block for folder '{path_stem}'")

    def _discover_block_path(self) -> pathlib.Path:
        cwd = pathlib.Path.cwd().stem
        if pathlib.Path.cwd().stem == 'test':
            return pathlib.Path('./test_blocks')
        elif pathlib.Path.cwd().stem == 'pyblocks-sim':
            return pathlib.Path('./src/pyblock_sim/repository/block_repository/test/test_blocks')
        else:
            raise RuntimeError(f"{self.__class__.__name__}: Can't infer the path with test blocks")
