from src.meow_sim.config_manager import ConfigManager

from src.meow_sim.config.config_loader import ConfigLoader
from src.meow_sim.config.config_validator import ConfigValidator
from src.meow_sim.logger import logger


def main():
    logger.info("Meow!  :cat:\n")

    config = ConfigLoader.load()
    logger.info("[green]Loaded config![/green]", ':white_check_mark:')

    logger.info("Validating config...")
    errors = ConfigValidator.validate(config)


if __name__ == "__main__":
    main()
