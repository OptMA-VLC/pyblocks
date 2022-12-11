from typing import List

from src.meow_sim.config.config_problem import ConfigProblem
from src.meow_sim.data_structures.config import BlockDescription, Config


class ConfigValidator:
    @staticmethod
    def validate(config: Config) -> List[ConfigProblem]:
        report = list()
        report.append(
            ConfigValidator._check_duplicate_block_ids(config.blocks)
        )
        # check_duplicate_port_ids()
        # check_duplicate_connection_ids()
        #
        # check_connections()
        #
        # check_block_paths_exist()
        return report

    @staticmethod
    def _check_duplicate_block_ids(blocks: List[BlockDescription]):
        pass
