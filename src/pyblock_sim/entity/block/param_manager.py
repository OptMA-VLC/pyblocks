from logging import Logger
from typing import List

from src.pyblock_sim.entity.block.parameter_entity import ParameterEntity
from src.pyblock_sim.util.logger_provider import LoggerProvider


class ParameterManager:
    _block_params: List[ParameterEntity]
    _user_params: List[ParameterEntity]
    _logger: Logger

    def __init__(self, logger=None):
        self._block_params = []
        self._user_params = []

        if logger is None:
            self._logger = LoggerProvider.get_logger()
        else:
            self._logger = logger

    def set_block_params(self, params: List[ParameterEntity]):
        self._block_params = params

    def set_user_params(self, params: List[ParameterEntity]):
        self._user_params = []
        block_param_ids = [p.param_id for p in self._block_params]

        for param in params:
            if param.param_id in block_param_ids:
                self._user_params.append(param)
            else:
                self._logger.warning(
                    f"The provided parameter '{param.param_id}' does "
                    f"not match any parameter made available by the block"
                )

    def get_params(self) -> List[ParameterEntity]:
        return self._user_params
