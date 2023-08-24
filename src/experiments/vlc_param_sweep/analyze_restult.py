import plots
from sweep_result.load_result import load_result

result = load_result()

target_signal = 'ltspice_rx::signal_out[V(Saida)]'
rx_outputs = result.get_signals(target_signal)

# plots.plot_voltages(result.param_values, rx_outputs)
plots.plot_outputs(result.param_values, rx_outputs)

