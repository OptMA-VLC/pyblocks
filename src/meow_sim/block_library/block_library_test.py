import pathlib

from src.meow_sim.block_library.block_library import BlockLibrary


class TestBlockDirValidation:
    def test_ok(self, tmp_path):
        block_path = (tmp_path/'my_block')
        block_path.mkdir()
        block_py = (block_path/'block.py').open(mode='w')
        block_py.write('# file content here!')

        assert BlockLibrary.is_block_dir(block_path) is True

    def test_missing_block_py_file(self, tmp_path):
        block_path = tmp_path/'my_block'
        block_path.mkdir()

        assert BlockLibrary.is_block_dir(block_path) is False
