import pickle
from pathlib import Path
from typing import List, Dict, Any, Union

from .data_types.sweep_result import SweepResult, IterationResult
from .data_types.time_signal import TimeSignal


def load_result(path: Union[Path, str] = None) -> SweepResult:
    if isinstance(path, str):
        path = Path(path)
    if path is None:
        path = Path(__file__).parent / 'data.pkl'

    if not path.resolve().exists():
        raise IOError(f'Could not find data file to load parameter sweep results at {path.resolve()}')

    with open(path, 'rb') as f:
        result_dict = pickle.load(f)

    result = SweepResult()
    result.target_block = result_dict['target_block']
    result.target_param = result_dict['target_param']
    result.param_values = result_dict['param_values']
    result.iterations = _unpack_iterations(result_dict)

    return result


def _unpack_iterations(result_dict: Dict) -> List[IterationResult]:
    iterations_dicts = result_dict['iterations']
    iterations = []

    for iter_dict in iterations_dicts:
        iteration = IterationResult()
        iteration.iteration_number = iter_dict['iteration_number']
        iteration.parameter_value = iter_dict['param_value']
        iteration.signals = _unpack_signals(iter_dict['signals'])

        iterations.append(iteration)

    return iterations


def _unpack_signals(signals_list: List[Dict]) -> Dict[str, Any]:
    signals = {}
    for signal_dict in signals_list:
        _type = signal_dict['_type']
        signal_name = signal_dict['name']
        signal_value = None

        if _type == 'TimeSignal':
            signal_value = TimeSignal()
            signal_value.time = signal_dict['time']
            signal_value.signal = signal_dict['signal']
        else:
            signal_value = signal_dict['value']

        signals[signal_name] = signal_value

    return signals
