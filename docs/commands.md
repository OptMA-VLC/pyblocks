# Commands

## Block Help

This command will make the simulator print a help text for the block

#### Example Usage:
```json
{
  "command": "block_help",
  "parameters": [
    {
      "param_id": "distribution_id",
      "value": "com.pyblocks.integrations.ltspice"
    }
  ]
},
```
- - - 

## Simulate

Runs a simulation on the block diagram described in the `blocks` and `connections` sections.
This command must be run before other commands that operate on signals (ex: `plot`, `save`) are called.

#### Example Usage:
```json
{
"command": "simulate"
}
```

- - -
## Plot

Creates a simple plot containing the signals specified by the parameter `signals`. 
The signals must be of the type `TimeSignal`. If the optional parameter `save_path` 
is provided an image of the plot is saved to a file.

```
{
  "command": "plot",
  "parameters": [
    {
      "param_id": "signals",
      "value": [
        "my_block::my_signal_1",
        "my_block_2::my_signal_2"
      ]
    }, {
      "param_id": "save_path",
      "value": "./my_plot.png"
    }
  ]
}
```
- - -

## Save

Saves the list of signals specified in the `signals` parameter 
to a csv file specified in the `save_path` parameter. Signals can
be lists/arrays or `TimeSignal`s and will be saved as columns in
the csv file.

```
{
  "command": "save",
  "parameters": [
    {
      "param_id": "signals",
      "value": [
        "my_block::my_signal_1",
        "my_block_2::my_signal_2"
      ]
    }, {
      "param_id": "save_path",
      "value": "./my_signals.csv"
    }
  ]
}
```

