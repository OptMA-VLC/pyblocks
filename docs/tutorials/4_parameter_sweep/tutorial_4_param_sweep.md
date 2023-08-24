# Tutorial 4: Parameter Sweep

In this tutorial you will learn:
- How to create a Parameter Sweep simulation
- How to extract and analyze the resulting data

### Parameter Sweep

In this type of simulation, we want to vary the value of one parameter in a block.
In this tutorial we will be using a simulation with two blocks: a signal
generator connected to a low-pass filter. We will use the project file to specify 
a list of values for the cutoff frequency.

We start the tutorial assuming a folder with a project file:

```
/4_parameter_sweep
  /project.json
```

The content of the project file describes two blocks: `signal_generator` and `low_pass_filter`.
The signal generator creates a square wave at 1kHz with sample frequency 10kHZ (that is, 10 
samples per cycle) and duration of 5ms (5 cycles). The low pass filter has its cutoff frequency
controlled by the parameter `f_cutoff`

```json
{
  "blocks": [
    {
      "distribution_id": "com.pyblocks.signal.signal_generator",
      "instance_id": "signal_generator",
      "parameters": [
        {
          "param_id": "duration", "value": 0.005
        }, {
          "param_id": "frequency", "value": 1000
        }, {
          "param_id": "sample_frequency", "value": 10000
        }
      ]
    },
    {
      "distribution_id": "com.pyblocks.signal.low_pass",
      "instance_id": "low_pass_filter",
      "parameters": [
        {
          "param_id": "f_cutoff", "value": 100
        }
      ]
    }
  ],
  "connections": [
    {
      "from": "signal_generator::signal_out",
      "to": "low_pass_filter::input"
    }
  ],
  "commands": [
    {
      "command": "parameter_sweep",
      "parameters": [
        {
          "param_id": "target_block_instance_id", "value": "low_pass_filter"
        }, {
          "param_id": "target_param_id", "value": "f_cutoff"
        }, {
          "param_id": "sweep_values", "value": [ 10, 100, 1000 ]
        }, {
          "param_id": "output_dir", "value": "."
        }
      ]
    }
  ]
}
```

We use the command `parameter_sweep` to run a series of simulations. A target 
block instance id and parameter id must be provided. Each value provided by 
`sweep_values` will be assigned to this parameter, the simulation will be run and
the results will be saved. Each run of the simulation is called an iteration of the
sweep.

In the parameter `output_dir`, we specify `.` to tell the simulator to save the
results in the same directory as the project file. Running the parameter sweep will
produce the following file structure:

```
/4_parameter_sweep
  /project.json
  /sweep_result
    /...
    /load_result.py
    /data.pkl
```

The parameter sweep saves **all** signals of every iteration in the `data.pkl` file.
The `load_result.py` is a file to help you load and interact with the result. The other
files in this folder support the operation of `load_result.py`. Create an additional file
in the `4_parameter_sweep` folder called `analysis.py` with the content:

```python
# analysis.py
from matplotlib import pyplot as plt

# we import the load_result function to load the result object from 'data.pkl'
from sweep_result.load_result import load_result

# load the simulation result
result = load_result()

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
```

The comments in the file explain how the signals in the parameter sweep result can 
be accessed and manipulated.

When the parameter sweep runs again, the contents of the `sweep_result` folder will be
replaced. If we wish to retain a result, we can move (and rename) `data.pkl` out of the 
`sweep_result` folder, giving the following file structure:

```
/4_parameter_sweep
  /project.json
  /sweep_result
    /...
  /analysis.py
  /sweep_1_data.pkl
  /...
  /sweep_n_data.pkl
```

In our analysis file, we modify the call to `load_result` and pass the path to the 
desired .pkl file as a parameter:

```python
result_1 = load_result('./sweep_1_data.pkl')
```
