import pytest

from src.pyblock.block.params.parameter import Parameter


class TestParam:
    def test_set_get_value(self):
        param = Parameter(param_id='my_param', type=str)

        param.value = 'my_str'
        assert param.value == 'my_str'

    def test_is_error_when_reading_before_assignment_and_no_default_exists(self):
        param = Parameter(param_id='my_param', type=str)
        with pytest.raises(ValueError):
            val = param.value

    def test_default_value(self):
        param = Parameter(param_id='my_param', type=str, default='default_str')

        assert param.value == 'default_str'
        param.value = 'user_str'
        assert param.value == 'user_str'

    # def test_reject_default_value_not_matching_type(self):
    #     with pytest.raises(ValueError):
    #         param = Param(param_id='my_param', type=int, default='default_str')

    # def test_reject_assigning_value_not_matching_type(self):
    #     param = Param(param_id='my_int_param', type=int)
    #
    #     with pytest.raises(ValueError):
    #         param.value = 'wrong_type'
    #
    # def test_lists(self):
    #     param = Param(param_id='my_list_param', param_type=List[str])
    #
    #     param.value = ['a', 'b']
    #     assert param.value[0] == 'a'
    #     assert param.value[1] == 'b'
    #
    #     with pytest.raises(ValueError):
    #         param.value = ['a', 1]
