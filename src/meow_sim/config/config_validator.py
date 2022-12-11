from collections import Counter
from typing import List

from src.meow_sim.config.config_problem import ConfigProblem, Severity
from src.meow_sim.data_structures.config import BlockDescription, Config


class ConfigValidator:
    @staticmethod
    def validate(config: Config) -> List[ConfigProblem]:
        report = list()
        report += ConfigValidator._check_duplicate_block_ids(config.blocks)

        # check_duplicate_port_ids()
        # check_duplicate_connection_ids()
        #
        # check_connections()
        #
        # check_block_paths_exist()

        return report

    @staticmethod
    def _check_duplicate_block_ids(blocks: List[BlockDescription]) -> List[ConfigProblem]:
        ids: [str] = list(map(lambda b: b.id, blocks))
        count = Counter(ids).items()
        problems = []

        for (block_id, cnt) in count:
            if cnt > 1:
                problems.append(ConfigProblem(
                    severity=Severity.ERROR,
                    message=f"Block id '{block_id}' is used by {cnt} blocks. Block id's must be unique."
                ))

        return problems
