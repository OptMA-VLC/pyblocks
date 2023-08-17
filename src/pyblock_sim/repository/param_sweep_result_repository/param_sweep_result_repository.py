import pickle
import shutil
from pathlib import Path

from src.pyblock_sim.entity.parameter_sweep.param_sweep_result_entity import ParamSweepResultEntity
from src.pyblock_sim.repository.param_sweep_result_repository.sweep_result_serializer import SweepResultSerializer


class ParamSweepResultRepository:
    def save_result(self, sweep_result: ParamSweepResultEntity, path: Path):
        if not path.is_dir():
            raise NotADirectoryError(
                f'The specified save directory for parameter sweep result does '
                f'not exist (Path: {path})'
            )

        serialized_result = SweepResultSerializer.result_to_dict(sweep_result)

        result_loader_origin_path = Path(__file__).parent/'sweep_result_template'
        result_loader_destination_path = path/'sweep_result'

        if result_loader_destination_path.exists():
            shutil.rmtree(result_loader_destination_path)
        shutil.copytree(result_loader_origin_path, result_loader_destination_path)

        with open(path/'sweep_result'/'data.pkl', 'wb') as f:
            pickle.dump(serialized_result, f)
