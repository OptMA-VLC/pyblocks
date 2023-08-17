from numbers import Number
from typing import Dict, List

from src.pyblock import TimeSignal
from src.pyblock_sim.entity.parameter_sweep.param_sweep_result_entity import ParamSweepResultEntity
from src.pyblock_sim.repository.signal_repository.signal_repository import SignalRepository


class SweepResultSerializer:
    @staticmethod
    def result_to_dict(result: ParamSweepResultEntity):
        for param in result.param_values:
            if not SweepResultSerializer._is_basic_type(param):
                TypeError(f'Cannot convert parameter value {param} because it is not of a builtin type')

        sweep_result_dict = {
            'param_values': result.param_values,
            'target_block': result.target_block,
            'target_param': result.target_param,
            'iterations': None
        }

        iterations = []
        for iteration in result.iteration_results:
            iteration_dict = {
                'param_value': iteration.parameter_value,
                'iteration_number': iteration.iteration_number,
                'signals': SweepResultSerializer._serialize_signal_repo(iteration.signal_repo)
            }
            iterations.append(iteration_dict)

        sweep_result_dict['iterations'] = iterations

        return sweep_result_dict

    @staticmethod
    def _serialize_signal_repo(signal_repo: SignalRepository) -> List[Dict]:
        serialized_signals = []
        for signal_selector in signal_repo.list_signals():
            signal = signal_repo.get_by_selector(signal_selector)
            signal_serialized = SweepResultSerializer._serialize_signal(str(signal_selector), signal)
            serialized_signals.append(signal_serialized)

        return serialized_signals

    @staticmethod
    def _serialize_signal(sig_name, signal):
        serialized_simple = {
            '_type': type(signal).__name__,
            'name': sig_name,
            'value': signal
        }

        if isinstance(signal, (str, Number)):
            return serialized_simple
        elif isinstance(signal, list):
            if len(signal) == 0:
                return serialized_simple

            if isinstance(signal[0], (str, Number)):
                return serialized_simple
            else:
                raise TypeError(
                    f"Can't serialize signal {sig_name} because it is a "
                    f"list of elements of type {type(signal[0]).__name__}"
                )
        elif isinstance(signal, TimeSignal):
            return {
                '_type': type(signal).__name__,
                'name': sig_name,
                'time': signal.time.tolist(),
                'signal': signal.wave.tolist()
            }
        else:
            raise TypeError(f"Can't serialize signal of type {type(signal).__name__}")

    @staticmethod
    def _is_basic_type(obj):
        return isinstance(obj, (str, Number))
