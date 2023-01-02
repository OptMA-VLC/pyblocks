import pathlib

import pytest

from src.meow_sim.block_library.block_adapter import BlockAdapter
from src.meow_sim.block_library.block_exceptions import BlockExceptions


class TestBlockDirLoading:
    def test_ok(self, tmp_path):
        block_path = (tmp_path / 'my_block')
        block_path.mkdir()
        _create_block_py(block_path, f'''
{_import_base_block}
{_block_class_definition(class_name='MyBlock')}
        ''')

        print('\nCreate BlockAdapter from files in block folder')
        BlockAdapter(block_path)
        print('Ok')

    def test_missing_block_py_file(self, tmp_path):
        block_path = tmp_path / 'my_block'
        block_path.mkdir()

        with pytest.raises(BlockExceptions.NoBlockPyFile):
            BlockAdapter(block_path)

    def test_no_block_class(self, tmp_path):
        block_path = tmp_path / 'my_block'
        block_path.mkdir()
        _create_block_py(block_path, f'''
{_import_base_block}
{_block_class_definition(base_class='object')}
        ''')

        with pytest.raises(BlockExceptions.LoadBlockClassFailed) as ex_info:
            BlockAdapter(block_path)
        assert 'No class' in str(ex_info.value)

    def test_more_than_one_block_class(self, tmp_path):
        block_path = tmp_path / 'my_block'
        block_path.mkdir()
        _create_block_py(block_path, f'''
{_import_base_block}
{_block_class_definition(class_name='Block1')}
{_block_class_definition(class_name='Block2')}
        ''')

        with pytest.raises(BlockExceptions.LoadBlockClassFailed) as ex_info:
            BlockAdapter(block_path)
        assert 'More than one' in str(ex_info.value)


def _create_block_py(path: pathlib.Path, content: str):
    with (path / 'block.py').open(mode='w') as block_py:
        block_py.write(content)


def _block_class_definition(class_name='Block', base_class='BaseBlock'):
    return '''
class {0}({1}):
    def get_info(self):
        pass

    def validate_inputs(self, inputs):
        pass

    def run(self, inputs, params):
        print('Hello Block!')
'''.format(class_name, base_class)


_import_base_block = 'from src.bdk.base_block import BaseBlock\n'
