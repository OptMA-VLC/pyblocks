import pathlib

import pytest

from src.meow_sim.repository.block_repository.block_repository import BlockRepository
from src.meow_sim.repository.block_repository.block_repository_exceptions import NoBlockPyFile, \
    NoBlockClassFound, MultipleBlockClassesInFile


class TestBlockRepository:
    def test_ok(self, tmp_path):
        block_path = (tmp_path / 'my_block')
        block_path.mkdir()

        _create_block_py(
            path=block_path,
            content=f'''
{_import_base_block}
{_block_class_definition('com.test.block', class_name='MyBlock')}
'''
        )

        print('\nShould create BlockAdapter from files in block folder...  ', end='')
        BlockRepository()._get_class_from_path(block_path)
        print('Ok')

    def test_missing_block_py_file(self, tmp_path):
        block_path = tmp_path / 'my_block'
        block_path.mkdir()

        with pytest.raises(NoBlockPyFile):
            BlockRepository()._get_class_from_path(block_path)

    def test_no_block_class(self, tmp_path):
        block_path = tmp_path / 'my_block'
        block_path.mkdir()
        _create_block_py(
            path=block_path,
            content=f'''
{_import_base_block}
{_block_class_definition('com.test.block', base_class='object')}
'''
        )

        with pytest.raises(NoBlockClassFound) as ex_info:
            BlockRepository()._get_class_from_path(block_path)

    def test_more_than_one_block_class(self, tmp_path):
        block_path = tmp_path / 'my_block'
        block_path.mkdir()
        _create_block_py(block_path, f'''
{_import_base_block}
{_block_class_definition('com.test.block', class_name='Block1')}
{_block_class_definition('com.test.block', class_name='Block2')}
        ''')

        with pytest.raises(MultipleBlockClassesInFile) as ex_info:
            BlockRepository()._get_class_from_path(block_path)


def _create_block_py(path: pathlib.Path, content: str):
    with (path / 'block.py').open(mode='w') as block_py:
        block_py.write(content)


def _block_class_definition(dist_name, class_name='Block', base_class='BaseBlock'):
    return f'''
from src.bdk.base_block import BaseBlock
from src.bdk.block_info import BlockInfo
    
class {class_name}({base_class}):
    def get_info(self):
        return BlockInfo(
            distribution_name='{dist_name}',
            name='Test Block',
            description='',
            params=[]
        )
    def validate_inputs(self, inputs):
        pass

    def run(self, inputs, params):
        print('Hello Block!')
'''

_import_base_block = 'from src.bdk.base_block import BaseBlock\n'
