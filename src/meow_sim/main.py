from src.meow_sim.block_library.block_library import BlockLibrary
from src.meow_sim.logger import logger

from src.meow_sim.simul_plan.plan_loader import PlanLoader
from src.meow_sim.simul_plan.plan_validator import PlanValidator


def main():
    logger.info("Meow!  :cat:\n")

    plan = PlanLoader.load()
    logger.info("[green]Loaded simulation plan![/green]", ':white_check_mark:')

    logger.info("Validating plan...")
    errors = PlanValidator.validate(plan)

    block_lib = BlockLibrary()


if __name__ == "__main__":
    main()
