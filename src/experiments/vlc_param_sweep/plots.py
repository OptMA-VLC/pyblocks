from typing import List

from matplotlib import pyplot as plt


def plot_voltages(param_values: List, rx_outputs: List):
    min_list = []
    max_list = []
    vpp_list = []

    for time_signal in rx_outputs:
        min_val = min(time_signal.signal)
        max_val = max(time_signal.signal)
        min_list.append(min_val)
        max_list.append(max_val)
        vpp_list.append(max_val - min_val)

    plt.plot(param_values, min_list, 'o-b', markersize=3, linewidth=1, label='Min Voltage')
    plt.plot(param_values, vpp_list, 'o-k', markersize=3, linewidth=1, label='Peak-to-Peak Voltage')
    plt.plot(param_values, max_list, 'o-r', markersize=3, linewidth=1, label='Max Voltage')
    plt.legend()
    plt.xlabel('Channel Gain (dB)')
    plt.ylabel('Voltage (V)')
    plt.show()

def plot_outputs(param_values: List, signals: List):
    for i, _ in enumerate(signals):
        signal = signals[i]
        param_value = param_values[i]
        plt.plot(signal.time, signal.signal, label=f'RX Output @ gain = {param_value}dB')

    plt.legend()
    plt.show()
