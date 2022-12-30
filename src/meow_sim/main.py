from src.meow_sim.block_library.block_library import BlockLibrary
from src.meow_sim.logger import logger

from src.meow_sim.simul_plan.plan_loader import PlanLoader
from src.meow_sim.simul_plan.plan_validator import PlanValidator


def main():
    logger.info('Meow!  :cat:\n')

    logger.info('Loading block library...')
    block_lib = BlockLibrary()
    block_lib.load_from_dir(BlockLibrary.BLOCK_PATH)
    logger.info(f'Block library loaded. Found [green]{len(block_lib)}[/green] blocks.')

    logger.info('Loading simulation plan...', end=' ')
    plan = PlanLoader.load()
    logger.info('[green]OK[/green]', no_tag=True)

    logger.info('Validating plan...', end=' ')
    validation_errors = PlanValidator.validate(plan)
    logger.info('[green]OK[/green]', no_tag=True)

    logger.warn('TODO: Build simulation graph')
    logger.warn('TODO: simulate')


if __name__ == "__main__":
    main()
