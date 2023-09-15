import math
from typing import List

from matplotlib import pyplot as plt

from sweep_result.data_types.time_signal import TimeSignal


def slice_time_signal(signal: TimeSignal, min_time=-math.inf, max_time=math.inf) -> TimeSignal:
    result = TimeSignal()
    result.time = []
    result.signal = []
    for i, time in enumerate(signal.time):
        if min_time < time < max_time:
            result.time.append(signal.time[i])
            result.signal.append(signal.signal[i])

    return result


def plot_min_max_voltages(param_values: List, rx_outputs: List):
    min_list = []
    max_list = []
    vpp_list = []

    for time_signal in rx_outputs:
        min_val = min(time_signal.signal)
        max_val = max(time_signal.signal)
        min_list.append(min_val)
        max_list.append(max_val)
        vpp_list.append(max_val - min_val)

    param_micro = [p*1e6 for p in param_values]

    plt.plot(param_micro, min_list, 'o-b', markersize=3, linewidth=1, label='Min Voltage')
    plt.plot(param_micro, vpp_list, 'o-k', markersize=3, linewidth=1, label='Peak-to-Peak Voltage')
    plt.plot(param_micro, max_list, 'o-r', markersize=3, linewidth=1, label='Max Voltage')
    plt.legend()
    plt.xlabel('Ambient Radiant Flux (µW)')
    plt.ylabel('Output Voltage (V)')
    plt.xscale('log')


def plot_outputs(param_values: List, signals: List):
    for i, _ in enumerate(signals):
        signal = signals[i]
        param_value = param_values[i]
        plt.plot(signal.time, signal.signal, label=f'param = {param_value}')

    # plt.ylim(bottom=0)
    plt.legend()
    plt.show()
