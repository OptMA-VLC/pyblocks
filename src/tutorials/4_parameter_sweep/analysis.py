# analysis.py
from matplotlib import pyplot as plt

# we import the load_result function to load the result object from 'data.pkl'
from sweep_result.load_result import load_result

# load the simulation result
result = load_result('./sweep_1_data.pkl')

# print the result object to see information such as number of iterations
print(result)

# The result object has an array of iterations
for iteration_result in result.iterations:
    # You can print to view the available signals
    print(iteration_result)

    # You can get a signal using the selector string
    output_signal = iteration_result.get_signal('low_pass_filter::output')

    # Add the signal to a plot
    # Since the signal 'low_pass_filter::output' is a TimeSignal, we can access
    # the .time and .signal arrays to plot them
    plt.plot(
        output_signal.time, output_signal.signal,
        label=f'f_cutoff = {iteration_result.parameter_value}Hz'
    )

# We need to plot the input signal too
input_signal = result.iterations[0].get_signal('signal_generator::signal_out')
plt.plot(input_signal.time, input_signal.signal, '--k', label=f'Input')

# Show the plot
plt.legend()
plt.show()
