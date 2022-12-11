from src.meow_sim.config.config_problem import Severity
from src.meow_sim.config.config_validator import ConfigValidator
from src.meow_sim.data_structures.config import Config, BlockDescription


class TestConfigValidator:
    def test_duplicate_block_id_ok(self):
        config = Config(
            blocks=[
                BlockDescription(id='id_1', path=''),
                BlockDescription(id='id_2', path='')
            ],
            connections=[]
        )

        problems = ConfigValidator.validate(config)

        assert len(problems) == 0

    def test_duplicate_block_id_error(self):
        config = Config(
            blocks=[
                BlockDescription(id='repeated_id', path=''),
                BlockDescription(id='repeated_id', path='')
            ],
            connections=[]
        )

        problems = ConfigValidator.validate(config)

        assert len(problems) == 1
        assert problems[0].severity == Severity.ERROR
