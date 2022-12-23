from collections import Counter
from typing import List

from .plan_problem import PlanProblem, Severity
from .data_structures import BlockDescription, SimulPlan


class PlanValidator:
    @staticmethod
    def validate(config: SimulPlan) -> List[PlanProblem]:
        report = list()
        report += PlanValidator._check_duplicate_block_ids(config.blocks)

        # check_duplicate_port_ids()
        # check_duplicate_connection_ids()
        #
        # check_connections()
        #
        # check_block_paths_exist()

        return report

    @staticmethod
    def _check_duplicate_block_ids(blocks: List[BlockDescription]) -> List[PlanProblem]:
        ids: [str] = list(map(lambda b: b.block_id, blocks))
        count = Counter(ids).items()
        problems = []

        for (block_id, cnt) in count:
            if cnt > 1:
                problems.append(PlanProblem(
                    severity=Severity.ERROR,
                    message=f"Block id '{block_id}' is used by {cnt} blocks. Block id's must be unique."
                ))

        return problems
