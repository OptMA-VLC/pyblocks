from src.meow_sim.simul_plan.data_structures import SimulPlan, BlockDescription
from src.meow_sim.simul_plan.plan_problem import Severity
from src.meow_sim.simul_plan.plan_validator import PlanValidator


class TestPlanValidator:
    def test_duplicate_block_id_ok(self):
        config = SimulPlan(
            blocks=[
                BlockDescription(instance_of='', block_id='id_1'),
                BlockDescription(instance_of='', block_id='id_2')
            ],
            connections=[]
        )

        problems = PlanValidator.validate(config)

        assert len(problems) == 0

    def test_duplicate_block_id_error(self):
        config = SimulPlan(
            blocks=[
                BlockDescription(instance_of='', block_id='repeated_id'),
                BlockDescription(instance_of='', block_id='repeated_id')
            ],
            connections=[]
        )

        problems = PlanValidator.validate(config)

        assert len(problems) == 1
        assert problems[0].severity == Severity.ERROR
