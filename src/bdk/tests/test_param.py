import pytest

from src.bdk.params.parameter import Parameter


class TestParam:
    def test_set_get_value(self):
        param = Parameter(param_id='my_param', param_type=str)

        param.value = 'my_str'
        assert param.value == 'my_str'

    def test_is_error_when_reading_before_assignment_and_no_default_exists(self):
        param = Parameter(param_id='my_param', param_type=str)
        with pytest.raises(ValueError):
            val = param.value

    def test_default_value(self):
        param = Parameter(param_id='my_param', param_type=str, default='default_str')

        assert param.value == 'default_str'
        param.value = 'user_str'
        assert param.value == 'user_str'

    def test_reject_default_value_not_matching_type(self):
        with pytest.raises(ValueError):
            param = Parameter(param_id='my_param', param_type=int, default='default_str')

    def test_reject_assigning_value_not_matching_type(self):
        param = Parameter(param_id='my_int_param', param_type=int)

        with pytest.raises(ValueError):
            param.value = 'wrong_type'

