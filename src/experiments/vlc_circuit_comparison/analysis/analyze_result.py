import math
from typing import List, Dict

from matplotlib import pyplot as plt

import utils
from sweep_result.load_result import load_result
from sweep_result.data_types.sweep_result import SweepResult


def extract_results(sweep_result: SweepResult, min_time=-math.inf) -> Dict:
    ambient_light = []
    rx_outputs = []
    rx_inputs = []

    for iteration_result in sweep_result.iterations:
        ambient_light.append(iteration_result.parameter_value)
        rx_outputs.append(iteration_result.get_signal('ltspice_rx::signal_out[V(Saida)]'))
        rx_inputs.append(iteration_result.get_signal('photodetector::output_current'))

    rx_inputs = [utils.slice_time_signal(out, min_time=min_time) for out in rx_inputs]
    rx_outputs = [utils.slice_time_signal(out, min_time=min_time) for out in rx_outputs]

    return {
        'ambient_light': ambient_light,
        'rx_inputs': rx_inputs,
        'rx_outputs': rx_outputs
    }


# start
basic_circuit_result = load_result('../basic_circuit/sweep_result/data.pkl')
adaptative_circuit_result = load_result('../adaptative_circuit/sweep_result/data.pkl')

basic_results = extract_results(basic_circuit_result, min_time=0.002)
adaptative_results = extract_results(adaptative_circuit_result, min_time=0.002)

#
signal_gen_out = adaptative_circuit_result.get_signals('ltspice_tx::signal_out[I(D1)]')

plt.plot(signal_gen_out[0].time, signal_gen_out[0].signal)
plt.show()

#
utils.plot_outputs(basic_results['ambient_light'], adaptative_results['rx_outputs'])

plt.subplot(1, 2, 1)
utils.plot_min_max_voltages(basic_results['ambient_light'], basic_results['rx_outputs'])
plt.subplot(1, 2, 2)
utils.plot_min_max_voltages(adaptative_results['ambient_light'], adaptative_results['rx_outputs'])
plt.show()

# for i, _ in enumerate(distances):
#     signal = rx_outputs[i]
#     distance = distances[i]
#     plt.plot(signal.time, signal.signal, label=f'RX Output @ d = {distance}m')
#
# plt.legend()
# plt.show()
